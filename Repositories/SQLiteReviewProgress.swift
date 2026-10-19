import Foundation

extension SQLiteProgressRepository {
    func configureReviewContentVersion(_ version: Int) async throws {
        guard version > 0 else { throw ReviewError.invalidState }
        try db.execute("INSERT INTO user_metadata(key,value) VALUES('review.content-version.v1',?) ON CONFLICT(key) DO UPDATE SET value=excluded.value WHERE value!=excluded.value", [.text(String(version))])
    }
    private func deferredReviewIDs(_ id: UUID) throws -> [String] {
        guard let value = try db.query("SELECT value FROM user_metadata WHERE key=?", [.text("review.deferred.v1." + id.uuidString)]).first?.text("value") else { return [] }
        let ids = try JSONDecoder().decode([String].self, from:Data(value.utf8))
        guard ids.count <= 30, Set(ids).count == ids.count else { throw ReviewError.invalidState }
        return ids
    }
    /// Explicit recovery for unavailable content, never a recall rating or SRS mutation.
    func deferUnavailableReview(sessionID: UUID, contentID: ContentID, contentVersion: Int, now: Date) async throws -> ReviewSession {
        try db.transaction {
            guard contentVersion > 0, now.timeIntervalSince1970.isFinite else { throw ReviewError.invalidState }
            let session = try readReviewSession(sessionID)
            var ids = try deferredReviewIDs(sessionID)
            if ids.contains(contentID.rawValue) { return session }
            guard session.currentID == contentID, !session.completed else { throw ReviewError.staleCard }
            ids.append(contentID.rawValue)
            let json = String(decoding:try JSONEncoder().encode(ids),as:UTF8.self)
            try db.execute("INSERT INTO user_metadata(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", [.text("review.deferred.v1." + sessionID.uuidString), .text(json)])
            // Exclude only from new queues for this release. A content update retries it.
            try db.execute("INSERT INTO user_metadata(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", [.text("review.unavailable.v1." + session.skill + "." + contentID.rawValue), .text(String(contentVersion))])
            let completed = session.completedCount + ids.count == session.ids.count
            try db.execute("UPDATE review_sessions SET status=?,updated_at=?,completed_at=? WHERE id=?", [.text(completed ? "completed" : "active"), .real(now.timeIntervalSince1970), completed ? .real(now.timeIntervalSince1970) : .null, .text(sessionID.uuidString)])
            return try readReviewSession(sessionID)
        }
    }
    /// Called inside the pass-completion transaction. Repeated learning never resets an existing schedule.
    func enrollVocabularyReview(_ session: VocabularySession, timeZoneID: String) throws {
        guard let completedAt = session.completedAt else { throw ReviewError.invalidState }
        for id in session.vocabularyIDs {
            let repeated = try !db.query("SELECT 1 FROM vocabulary_events WHERE session_id=? AND content_id=? AND kind='learn' LIMIT 1",
                [.text(session.id.uuidString), .text(id.rawValue)]).isEmpty
            let state = try StepReviewScheduler.initial(at: completedAt, neededRepetition: repeated, timeZoneID: timeZoneID)
            try db.execute("INSERT INTO srs_state(content_id,skill,algorithm,algorithm_version,state_json,due_at,last_review_at,updated_at) VALUES(?,'vocabulary',?,?,?,?,NULL,?) ON CONFLICT(content_id,skill) DO NOTHING",
                [.text(id.rawValue), .text(StepReviewScheduler.algorithm), .integer(Int64(StepReviewScheduler.version)),
                 .text(try encodeSRS(state)), .real(state.nextReviewAt.timeIntervalSince1970), .real(completedAt.timeIntervalSince1970)])
        }
        try db.execute("INSERT INTO srs_enrolled_passes(session_id) VALUES(?) ON CONFLICT(session_id) DO NOTHING", [.text(session.id.uuidString)])
    }
    func backfillVocabularyReviews(timeZoneID: String) async throws {
        // Existing DEV-05 completed attempts also enroll. Small batches bound memory and allow cancellation.
        while true {
            try Task.checkCancellation()
            let rows = try db.query("SELECT state_json FROM vocabulary_sessions s WHERE status='completed' AND NOT EXISTS(SELECT 1 FROM srs_enrolled_passes e WHERE e.session_id=s.id) ORDER BY updated_at,id LIMIT 50")
            if rows.isEmpty { return }
            try db.transaction {
                for row in rows {
                    let session = try JSONDecoder().decode(VocabularySession.self, from: Data(try row.text("state_json").utf8))
                    try session.validate()
                    try enrollVocabularyReview(session, timeZoneID: timeZoneID)
                }
            }
            await Task.yield()
        }
    }
    func encodeSRS(_ state: SRSState) throws -> String {
        String(decoding: try JSONEncoder().encode(state), as: UTF8.self)
    }
    func reviewState(for id: ContentID, skill: String) async throws -> SRSState? { try readSRS(id, skill: skill) }
    func readSRS(_ id: ContentID, skill: String) throws -> SRSState? {
        guard let row = try db.query("SELECT * FROM srs_state WHERE content_id=? AND skill=?", [.text(id.rawValue), .text(skill)]).first else { return nil }
        guard try row.text("algorithm") == StepReviewScheduler.algorithm,
              try row.integer("algorithm_version") == StepReviewScheduler.version else { throw ReviewError.invalidState }
        let state = try JSONDecoder().decode(SRSState.self, from: Data(try row.text("state_json").utf8))
        try state.validate()
        guard case .real(let due)? = row["due_at"], abs(due - state.nextReviewAt.timeIntervalSince1970) < 0.001 else { throw ReviewError.invalidState }
        return state
    }
    func reviewSummary(now: Date, timeZoneID: String) async throws -> ReviewSummary {
        let calendar = try StepReviewScheduler.calendar(timeZoneID: timeZoneID)
        let start = calendar.startOfDay(for: now)
        guard let end = calendar.date(byAdding: .day, value: 1, to: start) else { throw ReviewError.invalidState }
        let due = try db.query("SELECT COUNT(*) AS n FROM srs_state WHERE skill='vocabulary' AND algorithm=? AND algorithm_version=? AND due_at<=? AND NOT EXISTS(SELECT 1 FROM user_metadata unavailable WHERE unavailable.key='review.unavailable.v1.vocabulary.'||srs_state.content_id AND unavailable.value=COALESCE((SELECT value FROM user_metadata WHERE key='review.content-version.v1'),'0'))",
            [.text(StepReviewScheduler.algorithm), .integer(Int64(StepReviewScheduler.version)), .real(now.timeIntervalSince1970)]).first?.integer("n") ?? 0
        let overdue = try db.query("SELECT COUNT(*) AS n FROM srs_state WHERE skill='vocabulary' AND algorithm=? AND algorithm_version=? AND due_at<? AND NOT EXISTS(SELECT 1 FROM user_metadata unavailable WHERE unavailable.key='review.unavailable.v1.vocabulary.'||srs_state.content_id AND unavailable.value=COALESCE((SELECT value FROM user_metadata WHERE key='review.content-version.v1'),'0'))",
            [.text(StepReviewScheduler.algorithm), .integer(Int64(StepReviewScheduler.version)), .real(start.timeIntervalSince1970)]).first?.integer("n") ?? 0
        let completed = try db.query("SELECT COUNT(*) AS n FROM review_items r JOIN review_sessions s ON s.id=r.session_id WHERE s.skill='vocabulary' AND r.reviewed_at>=? AND r.reviewed_at<?", [.real(start.timeIntervalSince1970), .real(end.timeIntervalSince1970)]).first?.integer("n") ?? 0
        let active = try !db.query("SELECT 1 FROM review_sessions WHERE skill='vocabulary' AND status='active' LIMIT 1").isEmpty
        return ReviewSummary(due: due, overdue: overdue, completedToday: completed, hasActiveSession: active)
    }
    func beginReview(now: Date, limit: Int = 20) async throws -> ReviewSession {
        try db.transaction {
            if let active = try db.query("SELECT id FROM review_sessions WHERE skill='vocabulary' AND status='active'").first {
                guard let id = UUID(uuidString: try active.text("id")) else { throw ReviewError.invalidState }
                return try readReviewSession(id)
            }
            let ids = try db.query("SELECT content_id FROM srs_state WHERE skill='vocabulary' AND algorithm=? AND algorithm_version=? AND due_at<=? AND NOT EXISTS(SELECT 1 FROM user_metadata unavailable WHERE unavailable.key='review.unavailable.v1.vocabulary.'||srs_state.content_id AND unavailable.value=COALESCE((SELECT value FROM user_metadata WHERE key='review.content-version.v1'),'0')) ORDER BY due_at,content_id LIMIT ?",
                [.text(StepReviewScheduler.algorithm), .integer(Int64(StepReviewScheduler.version)), .real(now.timeIntervalSince1970), .integer(Int64(min(max(limit, 1), 30)))]).map { try $0.text("content_id") }
            guard !ids.isEmpty else { throw ReviewError.nothingDue }
            let id = UUID(), stamp = now.timeIntervalSince1970
            try db.execute("INSERT INTO review_sessions(id,skill,status,started_at,updated_at) VALUES(?,'vocabulary','active',?,?)", [.text(id.uuidString), .real(stamp), .real(stamp)])
            for (index, contentID) in ids.enumerated() {
                try db.execute("INSERT INTO review_items(session_id,content_id,ordinal) VALUES(?,?,?)", [.text(id.uuidString), .text(contentID), .integer(Int64(index))])
            }
            return try readReviewSession(id)
        }
    }
    func reviewSession(_ id: UUID) async throws -> ReviewSession { try readReviewSession(id) }
    func readReviewSession(_ id: UUID) throws -> ReviewSession {
        guard let row = try db.query("SELECT * FROM review_sessions WHERE id=?", [.text(id.uuidString)]).first else { throw ReviewError.invalidState }
        let items = try db.query("SELECT * FROM review_items WHERE session_id=? ORDER BY ordinal LIMIT 31", [.text(id.uuidString)])
        guard !items.isEmpty, items.count <= 30 else { throw ReviewError.invalidState }
        let deferred = Set(try deferredReviewIDs(id))
        let pending = try Set(items.filter { $0["result"]?.string == nil }.map { try $0.text("content_id") })
        guard deferred.isSubset(of:pending) else { throw ReviewError.invalidState }
        let current = items.first { row in
            guard let itemID = row["content_id"]?.string else { return false }
            return row["result"]?.string == nil && !deferred.contains(itemID)
        }
        let completed = try row.text("status") == "completed"
        guard completed == (current == nil) else { throw ReviewError.invalidState }
        let storedSkill = try row.text("skill")
        let practice = storedSkill.hasSuffix("_practice")
        let skill = practice ? String(storedSkill.dropLast(9)) : storedSkill
        return ReviewSession(id: id, skill: skill, isPractice:practice, ids: try items.map { ContentID(rawValue: try $0.text("content_id")) },
            completedCount: items.filter { $0["result"]?.string != nil }.count,
            currentID: try current.map { ContentID(rawValue: try $0.text("content_id")) },
            exposed: current?["exposed_at"] != .null && current != nil,
            revealed: current?["revealed_at"] != .null && current != nil, completed: completed, deferredCount: deferred.count)
    }
    func exposeReview(sessionID: UUID, contentID: ContentID, contentRevision: Int, contentVersion: Int, now: Date, timeZoneID: String) async throws -> ReviewSession {
        try db.transaction {
            let session = try readReviewSession(sessionID)
            guard session.currentID == contentID else { throw ReviewError.staleCard }
            if session.exposed { return session }
            let event = StudyEvent(id: UUID(), contentID: contentID, contentRevision: contentRevision, contentVersion: contentVersion,
                occurredAt: now, timeZoneID: timeZoneID, skill: session.skill + (session.isPractice ? "_practice" : "_review"), outcome: .viewed, durationMilliseconds: 0, sessionID: sessionID)
            try recordInTransaction(event)
            try db.execute("UPDATE review_items SET exposed_at=?,study_event_id=? WHERE session_id=? AND content_id=?",
                [.real(now.timeIntervalSince1970), .text(event.id.uuidString), .text(sessionID.uuidString), .text(contentID.rawValue)])
            try db.execute("UPDATE review_sessions SET updated_at=? WHERE id=?", [.real(now.timeIntervalSince1970), .text(sessionID.uuidString)])
            return try readReviewSession(sessionID)
        }
    }
    func revealReview(sessionID: UUID, contentID: ContentID, now: Date) async throws -> ReviewSession {
        try db.transaction {
            let session = try readReviewSession(sessionID)
            guard session.currentID == contentID, session.exposed else { throw ReviewError.staleCard }
            if session.skill == "grammar" {
                guard try !db.query("SELECT 1 FROM grammar_review_questions WHERE session_id=? AND content_id=? AND selected_choice IS NOT NULL", [.text(sessionID.uuidString), .text(contentID.rawValue)]).isEmpty else { throw ReviewError.staleCard }
            }
            if session.revealed { return session }
            try db.execute("UPDATE review_items SET revealed_at=? WHERE session_id=? AND content_id=?", [.real(now.timeIntervalSince1970), .text(sessionID.uuidString), .text(contentID.rawValue)])
            try db.execute("UPDATE review_sessions SET updated_at=? WHERE id=?", [.real(now.timeIntervalSince1970), .text(sessionID.uuidString)])
            return try readReviewSession(sessionID)
        }
    }
    func submitReview(sessionID: UUID, contentID: ContentID, rating: ReviewRating, now: Date, timeZoneID: String) async throws -> ReviewSession {
        try db.transaction {
            let session = try readReviewSession(sessionID)
            // A retry of a committed answer cannot answer the next card or double-count.
            if let answered = try db.query("SELECT result FROM review_items WHERE session_id=? AND content_id=?", [.text(sessionID.uuidString), .text(contentID.rawValue)]).first,
               answered["result"]?.string != nil { return session }
            guard session.currentID == contentID, session.revealed else { throw ReviewError.staleCard }
            let existing = try readSRS(contentID,skill:session.skill)
            guard session.isPractice || existing != nil else { throw ReviewError.staleCard }
            let previous = try existing ?? StepReviewScheduler.initial(at:now,neededRepetition:true,timeZoneID:timeZoneID)
            if session.skill == "grammar", rating == .remembered {
                guard try !db.query("SELECT 1 FROM grammar_review_questions WHERE session_id=? AND content_id=? AND correct=1", [.text(sessionID.uuidString), .text(contentID.rawValue)]).isEmpty else { throw ReviewError.staleCard }
            }
            let next: SRSState
            if session.isPractice { next = previous }
            else { next = try StepReviewScheduler.next(previous:previous,result:rating,at:now,timeZoneID:timeZoneID) }
            let day = try StudyDay.key(for: now, timeZoneID: timeZoneID)
            if !session.isPractice { try db.execute("UPDATE srs_state SET state_json=?,due_at=?,last_review_at=?,updated_at=? WHERE content_id=? AND skill=?",
                [.text(try encodeSRS(next)), .real(next.nextReviewAt.timeIntervalSince1970), .real(now.timeIntervalSince1970),
                 .real(now.timeIntervalSince1970), .text(contentID.rawValue), .text(session.skill)]) }
            try db.execute("UPDATE review_items SET result=?,reviewed_at=?,next_due_at=?,previous_stage=?,next_stage=?,time_zone=?,local_day=? WHERE session_id=? AND content_id=?",
                [.text(rating.rawValue), .real(now.timeIntervalSince1970), .real(next.nextReviewAt.timeIntervalSince1970),
                 .integer(Int64(previous.stage)), .integer(Int64(next.stage)), .text(timeZoneID), .text(day), .text(sessionID.uuidString), .text(contentID.rawValue)])
            let ungraded = try db.query("SELECT COUNT(*) AS n FROM review_items WHERE session_id=? AND result IS NULL", [.text(sessionID.uuidString)]).first?.integer("n") ?? 0
            let remaining = ungraded - session.deferredCount
            try db.execute("UPDATE review_sessions SET status=?,updated_at=?,completed_at=? WHERE id=?",
                [.text(remaining == 0 ? "completed" : "active"), .real(now.timeIntervalSince1970), remaining == 0 ? .real(now.timeIntervalSince1970) : .null, .text(sessionID.uuidString)])
            return try readReviewSession(sessionID)
        }
    }
}
