import Foundation

extension SQLiteProgressRepository {
    func resumableVocabularySet(level: LearningLevel) async throws -> VocabularyStudySet? {
        guard let row = try db.query("SELECT s.set_id FROM vocabulary_sessions s JOIN vocabulary_sets v ON v.id=s.set_id WHERE v.level=? AND s.status='active' ORDER BY s.updated_at DESC,s.id LIMIT 1", [.text(level.rawValue)]).first else { return nil }
        guard let id = UUID(uuidString: try row.text("set_id")) else { throw VocabularyStudyError.invalidState }
        return try readVocabularySet(id)
    }
    func vocabularySets(level: LearningLevel, after number: Int, limit: Int) async throws -> [VocabularyStudySet] {
        try db.query("SELECT id FROM vocabulary_sets WHERE level=? AND ordinal>? ORDER BY ordinal LIMIT ?",
            [.text(level.rawValue), .integer(Int64(max(0, number))), .integer(Int64(min(max(1, limit), 50)))]).map {
                guard let id = UUID(uuidString: try $0.text("id")) else { throw VocabularyStudyError.invalidState }
                return try readVocabularySet(id)
            }
    }
    func assignedVocabularyIDs(in ids: [ContentID]) async throws -> Set<ContentID> {
        guard !ids.isEmpty, ids.count <= 100 else { throw VocabularyStudyError.invalidState }
        let placeholders = Array(repeating: "?", count: ids.count).joined(separator: ",")
        return Set(try db.query("SELECT content_id FROM vocabulary_set_items WHERE content_id IN (\(placeholders))",
            ids.map { .text($0.rawValue) }).map { ContentID(rawValue: try $0.text("content_id")) })
    }
    func createVocabularySet(level: LearningLevel, ids: [ContentID]) async throws -> VocabularyStudySet {
        guard !ids.isEmpty, ids.count <= 25, Set(ids).count == ids.count else { throw VocabularyStudyError.invalidState }
        return try db.transaction {
            let id = UUID()
            let ordinal = try db.query("SELECT COALESCE(MAX(ordinal),0)+1 AS next FROM vocabulary_sets WHERE level=?", [.text(level.rawValue)]).first?.integer("next") ?? 1
            try db.execute("INSERT INTO vocabulary_sets(id,level,ordinal,created_at) VALUES(?,?,?,?)",
                [.text(id.uuidString), .text(level.rawValue), .integer(Int64(ordinal)), .real(Date().timeIntervalSince1970)])
            for (index, contentID) in ids.enumerated() {
                // Global content_id UNIQUE rejects allocation races and reordering duplicates.
                try db.execute("INSERT INTO vocabulary_set_items(set_id,content_id,ordinal) VALUES(?,?,?)",
                    [.text(id.uuidString), .text(contentID.rawValue), .integer(Int64(index))])
            }
            return try readVocabularySet(id)
        }
    }
    func curriculumVocabularySet(id: UUID) async throws -> VocabularyStudySet { try readVocabularySet(id) }
    private func readVocabularySet(_ id: UUID) throws -> VocabularyStudySet {
        guard let row = try db.query("SELECT *,EXISTS(SELECT 1 FROM vocabulary_sessions WHERE set_id=vocabulary_sets.id AND status='active') AS active FROM vocabulary_sets WHERE id=?", [.text(id.uuidString)]).first,
              let level = LearningLevel(rawValue: try row.text("level")) else { throw VocabularyStudyError.invalidState }
        let ids = try db.query("SELECT content_id FROM vocabulary_set_items WHERE set_id=? ORDER BY ordinal", [.text(id.uuidString)]).map { ContentID(rawValue: try $0.text("content_id")) }
        guard !ids.isEmpty, ids.count <= 25 else { throw VocabularyStudyError.invalidState }
        return VocabularyStudySet(id: id, level: level, number: try row.integer("ordinal"), vocabularyIDs: ids,
            completedCount: try row.integer("completed_count"), hasActiveSession: try row.integer("active") == 1)
    }
    func beginVocabularySet(_ setID: UUID, contentVersion: Int, restart: Bool) async throws -> VocabularySession {
        try db.transaction {
            let set = try readVocabularySet(setID)
            if let active = try db.query("SELECT state_json FROM vocabulary_sessions WHERE set_id=? AND status='active'", [.text(setID.uuidString)]).first {
                // An in-progress attempt always wins; never destroy it with an accidental restart.
                let saved = try decodeVocabularySession(active)
                return try readVocabularySession(saved.id)
            }
            if !restart, let previous = try db.query("SELECT state_json FROM vocabulary_sessions WHERE set_id=? ORDER BY updated_at DESC,id LIMIT 1", [.text(setID.uuidString)]).first {
                let saved = try decodeVocabularySession(previous)
                return try readVocabularySession(saved.id)
            }
            let state = try VocabularyPassEngine.start(setID: setID, ids: set.vocabularyIDs,
                contentVersion: contentVersion, seed: UInt64.random(in: 0...UInt64.max))
            try db.execute("INSERT INTO vocabulary_sessions(id,set_id,state_json,revision,status,updated_at) VALUES(?,?,?,?,'active',?)",
                [.text(state.id.uuidString), .text(setID.uuidString), .text(try encodeVocabularySession(state)),
                 .integer(Int64(state.revision)), .real(state.updatedAt.timeIntervalSince1970)])
            try beginVocabularyRound(state)
            return state
        }
    }
    func vocabularySession(_ id: UUID) async throws -> VocabularySession { try readVocabularySession(id) }
    private func readVocabularySession(_ id: UUID) throws -> VocabularySession {
        guard let row = try db.query("SELECT * FROM vocabulary_sessions WHERE id=?", [.text(id.uuidString)]).first else { throw VocabularyStudyError.invalidState }
        let state = try decodeVocabularySession(row)
        guard state.id == id, state.setID.uuidString == (try row.text("set_id")),
              state.revision == (try row.integer("revision")),
              state.completed == ((try row.text("status")) == "completed") else { throw VocabularyStudyError.invalidState }
        guard state.vocabularyIDs == (try readVocabularySet(state.setID)).vocabularyIDs else { throw VocabularyStudyError.invalidState }
        return state
    }
    private func decodeVocabularySession(_ row: SQLRow) throws -> VocabularySession {
        let state = try JSONDecoder().decode(VocabularySession.self, from: Data(try row.text("state_json").utf8))
        try state.validate()
        return state
    }
    private func encodeVocabularySession(_ state: VocabularySession) throws -> String {
        String(decoding: try JSONEncoder().encode(state), as: UTF8.self)
    }
    private func beginVocabularyRound(_ state: VocabularySession) throws {
        // Legacy pass tables now track real passes. pass_number is cumulative per set;
        // state.round is the round within this particular attempt.
        let number = try db.query("SELECT COALESCE(MAX(pass_number),0)+1 AS next FROM learning_passes WHERE scope_content_id=?", [.text(state.setID.uuidString)]).first?.integer("next") ?? 1
        try db.execute("INSERT INTO learning_passes(id,scope_content_id,started_at,pass_number) VALUES(?,?,?,?)",
            [.text(state.passID.uuidString), .text(state.setID.uuidString), .real(state.updatedAt.timeIntervalSince1970), .integer(Int64(number))])
        for id in state.order {
            try db.execute("INSERT INTO pass_items(pass_id,content_id) VALUES(?,?)", [.text(state.passID.uuidString), .text(id.rawValue)])
        }
    }
    private func vocabularyEvent(_ kind: String, state: VocabularySession, contentID: ContentID? = nil) throws {
        try db.execute("INSERT INTO vocabulary_events(id,session_id,content_id,round,kind,occurred_at) VALUES(?,?,?,?,?,?)",
            [.text(UUID().uuidString), .text(state.id.uuidString), contentID.map { .text($0.rawValue) } ?? .null,
             .integer(Int64(state.round)), .text(kind), .real(state.updatedAt.timeIntervalSince1970)])
    }
    func updateVocabularySession(_ id: UUID, expectedRevision: Int, action: VocabularyAction) async throws -> VocabularySession {
        try db.transaction {
            let previous = try readVocabularySession(id)
            guard previous.revision == expectedRevision else { throw VocabularyStudyError.staleState }
            let state = try VocabularyPassEngine.applying(action, to: previous)
            if state == previous { return state }
            switch action {
            case .expose(let contentRevision, let contentVersion):
                guard let contentID = previous.currentID else { throw VocabularyStudyError.invalidState }
                try recordInTransaction(StudyEvent(id: UUID(), contentID: contentID, contentRevision: contentRevision,
                    contentVersion: contentVersion, occurredAt: state.updatedAt, timeZoneID: TimeZone.current.identifier,
                    skill: "vocabulary_pass", outcome: .viewed, durationMilliseconds: 0, sessionID: state.id))
                try vocabularyEvent("exposure", state: state, contentID: contentID)
            case .decide(let decision):
                guard let contentID = previous.currentID else { throw VocabularyStudyError.invalidState }
                try vocabularyEvent(decision.rawValue, state: state, contentID: contentID)
                try db.execute("UPDATE pass_items SET completed_at=? WHERE pass_id=? AND content_id=?",
                    [.real(state.updatedAt.timeIntervalSince1970), .text(state.passID.uuidString), .text(contentID.rawValue)])
                if decision == .known {
                    try db.execute("UPDATE item_progress SET completed_passes=completed_passes+1 WHERE content_id=?", [.text(contentID.rawValue)])
                }
                if state.currentID == nil {
                    try vocabularyEvent("round_completed", state: state)
                    try db.execute("UPDATE learning_passes SET completed_at=? WHERE id=?", [.real(state.updatedAt.timeIntervalSince1970), .text(state.passID.uuidString)])
                }
                if state.completed {
                    try enrollVocabularyReview(state, timeZoneID: TimeZone.current.identifier)
                    try vocabularyEvent("set_completed", state: state)
                    try db.execute("UPDATE vocabulary_sets SET completed_count=completed_count+1 WHERE id=?", [.text(state.setID.uuidString)])
                }
            case .nextRound: try beginVocabularyRound(state)
            case .reveal: break
            }
            try db.execute("UPDATE vocabulary_sessions SET state_json=?,revision=?,status=?,updated_at=? WHERE id=?",
                [.text(try encodeVocabularySession(state)), .integer(Int64(state.revision)), .text(state.completed ? "completed" : "active"),
                 .real(state.updatedAt.timeIntervalSince1970), .text(id.uuidString)])
            return state
        }
    }
}
