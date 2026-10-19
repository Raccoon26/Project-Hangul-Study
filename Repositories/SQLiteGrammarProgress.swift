import Foundation

extension SQLiteProgressRepository {
    func grammarStatuses(ids: [ContentID]) async throws -> [GrammarLessonStatus] {
        guard ids.count <= 30 else { throw GrammarError.invalidState }
        return try ids.map { id in
            let row = try db.query("SELECT SUM(status='completed') AS n,MAX(status='active') AS active FROM grammar_sessions WHERE lesson_id=?", [.text(id.rawValue)]).first ?? [:]
            return GrammarLessonStatus(lessonID: id, completed: row["n"]?.int ?? 0, active: row["active"]?.int == 1)
        }
    }
    func beginGrammar(lesson: ContentID, ids: [ContentID], contentVersion: Int, restart: Bool) async throws -> GrammarSession {
        try db.transaction {
            if let row = try db.query("SELECT state_json FROM grammar_sessions WHERE lesson_id=? AND status='active'", [.text(lesson.rawValue)]).first {
                // Active attempts always resume. Restart only creates a new attempt after completion.
                return try decodeGrammar(row)
            }
            if !restart, let row = try db.query("SELECT state_json FROM grammar_sessions WHERE lesson_id=? ORDER BY updated_at DESC LIMIT 1", [.text(lesson.rawValue)]).first { return try decodeGrammar(row) }
            let now = Date()
            let state = GrammarSession(id: UUID(), lessonID: lesson, ids: ids, contentVersion: contentVersion,
                seed: UInt64.random(in: 0...UInt64(Int64.max)), startedAt: now, updatedAt: now, order: ids)
            try state.validate()
            try db.execute("INSERT INTO grammar_sessions(id,lesson_id,state_json,revision,status,updated_at) VALUES(?,?,?,0,'active',?)",
                [.text(state.id.uuidString), .text(lesson.rawValue), .text(try encodeGrammar(state)), .real(now.timeIntervalSince1970)])
            return state
        }
    }
    private func encodeGrammar(_ state: GrammarSession) throws -> String { String(decoding: try JSONEncoder().encode(state), as: UTF8.self) }
    private func decodeGrammar(_ row: SQLRow) throws -> GrammarSession {
        let state = try JSONDecoder().decode(GrammarSession.self, from: Data(try row.text("state_json").utf8))
        try state.validate(); return state
    }
    func grammarSession(id: UUID) async throws -> GrammarSession {
        guard let row = try db.query("SELECT state_json FROM grammar_sessions WHERE id=?", [.text(id.uuidString)]).first else { throw GrammarError.invalidState }
        return try decodeGrammar(row)
    }
    func updateGrammar(id: UUID, revision: Int, action: GrammarAction, contentRevision: Int, contentVersion: Int) async throws -> GrammarSession {
        try db.transaction {
            guard let row = try db.query("SELECT state_json FROM grammar_sessions WHERE id=?", [.text(id.uuidString)]).first else { throw GrammarError.invalidState }
            let before = try decodeGrammar(row)
            guard before.revision == revision else { throw VocabularyStudyError.staleState }
            let now = Date(), next = try GrammarLearning.apply(action, to: before, now: now)
            if next == before { return next }
            var outcome: StudyOutcome?
            switch action {
            case .expose: outcome = .viewed
            case .answer(let choice): outcome = before.question?.isCorrect(choice) == true ? .correct : .incorrect
            default: break
            }
            if let outcome = outcome, let contentID = before.currentID {
                try recordInTransaction(StudyEvent(id: UUID(), contentID: contentID, contentRevision: contentRevision,
                    contentVersion: contentVersion, occurredAt: now, timeZoneID: TimeZone.current.identifier,
                    skill: "grammar", outcome: outcome, durationMilliseconds: 0, sessionID: id))
            }
            if next.completed {
                for contentID in next.ids {
                    let state = try StepReviewScheduler.initial(at: now, neededRepetition: next.repeated.contains(contentID), timeZoneID: TimeZone.current.identifier)
                    try db.execute("INSERT INTO srs_state(content_id,skill,algorithm,algorithm_version,state_json,due_at,updated_at) VALUES(?,'grammar',?,?,?,?,?) ON CONFLICT(content_id,skill) DO NOTHING",
                        [.text(contentID.rawValue), .text(StepReviewScheduler.algorithm), .integer(Int64(StepReviewScheduler.version)),
                         .text(try encodeSRS(state)), .real(state.nextReviewAt.timeIntervalSince1970), .real(now.timeIntervalSince1970)])
                    try db.execute("UPDATE item_progress SET completed_passes=completed_passes+1 WHERE content_id=?", [.text(contentID.rawValue)])
                }
            }
            try db.execute("UPDATE grammar_sessions SET state_json=?,revision=?,status=?,updated_at=? WHERE id=?",
                [.text(try encodeGrammar(next)), .integer(Int64(next.revision)), .text(next.completed ? "completed" : "active"), .real(now.timeIntervalSince1970), .text(id.uuidString)])
            return next
        }
    }
    func grammarReviewSummary(now: Date) async throws -> ReviewSummary {
        let row = try db.query("SELECT COUNT(*) AS n FROM srs_state WHERE skill='grammar' AND algorithm=? AND algorithm_version=? AND due_at<=?",
            [.text(StepReviewScheduler.algorithm), .integer(Int64(StepReviewScheduler.version)), .real(now.timeIntervalSince1970)]).first
        let active = try !db.query("SELECT 1 FROM review_sessions WHERE skill='grammar' AND status='active' LIMIT 1").isEmpty
        let start = try StepReviewScheduler.calendar(timeZoneID: TimeZone.current.identifier).startOfDay(for: now)
        let overdue = try db.query("SELECT COUNT(*) AS n FROM srs_state WHERE skill='grammar' AND algorithm=? AND algorithm_version=? AND due_at<?", [.text(StepReviewScheduler.algorithm), .integer(Int64(StepReviewScheduler.version)), .real(start.timeIntervalSince1970)]).first?.integer("n") ?? 0
        let done = try db.query("SELECT COUNT(*) AS n FROM review_items r JOIN review_sessions s ON s.id=r.session_id WHERE s.skill='grammar' AND r.reviewed_at>=? AND r.reviewed_at<=?", [.real(start.timeIntervalSince1970), .real(now.timeIntervalSince1970)]).first?.integer("n") ?? 0
        return ReviewSummary(due: try row?.integer("n") ?? 0, overdue: overdue, completedToday: done, hasActiveSession: active)
    }
    func beginGrammarReview(now: Date) async throws -> ReviewSession {
        try db.transaction {
            if let row = try db.query("SELECT id FROM review_sessions WHERE skill='grammar' AND status='active'").first {
                guard let id = UUID(uuidString: try row.text("id")) else { throw ReviewError.invalidState }
                return try readReviewSession(id)
            }
            let ids = try db.query("SELECT content_id FROM srs_state WHERE skill='grammar' AND algorithm=? AND algorithm_version=? AND due_at<=? ORDER BY due_at,content_id LIMIT 20",
                [.text(StepReviewScheduler.algorithm), .integer(Int64(StepReviewScheduler.version)), .real(now.timeIntervalSince1970)])
            guard !ids.isEmpty else { throw ReviewError.nothingDue }
            let id = UUID(), stamp = now.timeIntervalSince1970
            try db.execute("INSERT INTO review_sessions(id,skill,status,started_at,updated_at) VALUES(?,'grammar','active',?,?)", [.text(id.uuidString), .real(stamp), .real(stamp)])
            for (index,row) in ids.enumerated() {
                try db.execute("INSERT INTO review_items(session_id,content_id,ordinal) VALUES(?,?,?)", [.text(id.uuidString), .text(try row.text("content_id")), .integer(Int64(index))])
            }
            return try readReviewSession(id)
        }
    }
    func prepareGrammarReview(sessionID: UUID, contentID: ContentID, question: GrammarQuestion) async throws -> GrammarReviewQuestion {
        try db.transaction {
            let session = try readReviewSession(sessionID)
            guard session.skill == "grammar", session.currentID == contentID else { throw ReviewError.staleCard }
            try question.validate()
            let json = String(decoding: try JSONEncoder().encode(question), as: UTF8.self)
            try db.execute("INSERT INTO grammar_review_questions(session_id,content_id,question_json) VALUES(?,?,?) ON CONFLICT(session_id,content_id) DO NOTHING", [.text(sessionID.uuidString), .text(contentID.rawValue), .text(json)])
            return try readGrammarReview(sessionID, contentID)
        }
    }
    private func readGrammarReview(_ sessionID: UUID, _ contentID: ContentID) throws -> GrammarReviewQuestion {
        guard let row = try db.query("SELECT * FROM grammar_review_questions WHERE session_id=? AND content_id=?", [.text(sessionID.uuidString), .text(contentID.rawValue)]).first else { throw ReviewError.invalidState }
        let question = try JSONDecoder().decode(GrammarQuestion.self, from: Data(try row.text("question_json").utf8))
        try question.validate()
        let selected = row["selected_choice"]?.string
        guard selected == nil || question.choices.contains(where: { $0.id == selected }) else { throw GrammarError.invalidState }
        return GrammarReviewQuestion(question: question, selected: selected)
    }
    func answerGrammarReview(sessionID: UUID, contentID: ContentID, choice: String, contentRevision: Int, contentVersion: Int) async throws -> GrammarReviewQuestion {
        try db.transaction {
            let session = try readReviewSession(sessionID)
            guard session.skill == "grammar", session.currentID == contentID, session.exposed else { throw ReviewError.staleCard }
            let current = try readGrammarReview(sessionID, contentID)
            if current.selected != nil { return current }
            guard current.question.choices.contains(where: { $0.id == choice }) else { throw GrammarError.invalidState }
            let correct = current.question.isCorrect(choice), now = Date()
            try db.execute("UPDATE grammar_review_questions SET selected_choice=?,correct=? WHERE session_id=? AND content_id=?", [.text(choice), .integer(correct ? 1 : 0), .text(sessionID.uuidString), .text(contentID.rawValue)])
            try recordInTransaction(StudyEvent(id: UUID(), contentID: contentID, contentRevision: contentRevision, contentVersion: contentVersion,
                occurredAt: now, timeZoneID: TimeZone.current.identifier, skill: session.isPractice ? "grammar_quiz_practice" : "grammar_quiz_review", outcome: correct ? .correct : .incorrect,
                durationMilliseconds: 0, sessionID: sessionID))
            try db.execute("UPDATE review_items SET revealed_at=? WHERE session_id=? AND content_id=?", [.real(now.timeIntervalSince1970), .text(sessionID.uuidString), .text(contentID.rawValue)])
            try db.execute("UPDATE review_sessions SET updated_at=? WHERE id=?", [.real(now.timeIntervalSince1970), .text(sessionID.uuidString)])
            return try readGrammarReview(sessionID, contentID)
        }
    }
}
