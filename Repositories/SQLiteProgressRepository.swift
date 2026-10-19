import Foundation

actor SQLiteProgressRepository: ProgressRepository {
    let db: SQLiteConnection
    init(url: URL, schema: String, datasetID: String) throws {
        let connection = try SQLiteConnection(url: url, readOnly: false)
        if try !connection.query("SELECT 1 FROM sqlite_master WHERE type='table' AND name='user_metadata'").isEmpty,
           let existing = try connection.query("SELECT value FROM user_metadata WHERE key='dataset_id'").first {
            guard try existing.text("value") == datasetID else { throw DatabaseError.invalidData("Progress dataset mismatch") }
        }
        try UserDatabaseMigration.migrate(connection, schema: schema)
        if let existing = try connection.query("SELECT value FROM user_metadata WHERE key='dataset_id'").first {
            guard try existing.text("value") == datasetID else { throw DatabaseError.invalidData("Progress dataset mismatch") }
        } else {
            try connection.execute("INSERT INTO user_metadata(key,value) VALUES('dataset_id',?)", [.text(datasetID)])
        }
        db = connection
    }
    func favoriteIDs() async throws -> Set<ContentID> {
        Set(try db.query("SELECT content_id FROM favorites").map { ContentID(rawValue: try $0.text("content_id")) })
    }
    func setFavorite(_ id: ContentID, enabled: Bool) async throws {
        if enabled {
            try db.execute("INSERT INTO favorites(content_id,created_at) VALUES(?,?) ON CONFLICT(content_id) DO NOTHING",
                           [.text(id.rawValue), .real(Date().timeIntervalSince1970)])
        } else { try db.execute("DELETE FROM favorites WHERE content_id=?", [.text(id.rawValue)]) }
    }
    /// UUID idempotency + atomic event, counters and daily aggregate. No SRS scheduling here.
    func record(_ event: StudyEvent) async throws {
        try db.transaction { try recordInTransaction(event) }
    }
    func recordInTransaction(_ event: StudyEvent) throws {
        guard event.durationMilliseconds >= 0, event.contentRevision > 0, event.contentVersion > 0 else {
            throw DatabaseError.invalidData("Invalid study event")
        }
        let day = try StudyDay.key(for: event.occurredAt, timeZoneID: event.timeZoneID)
        let timestamp = event.occurredAt.timeIntervalSince1970
        let studied = event.outcome == .skipped ? 0 : 1
        let correct = event.outcome == .correct ? 1 : 0
        let incorrect = event.outcome == .incorrect ? 1 : 0
        if try !db.query("SELECT id FROM study_events WHERE id=?", [.text(event.id.uuidString)]).isEmpty { return }
        try db.execute("""
        INSERT INTO study_events(id,content_id,content_revision,occurred_at,local_day,time_zone,skill,outcome,duration_ms,session_id,content_version)
        VALUES(?,?,?,?,?,?,?,?,?,?,?)
        """, [.text(event.id.uuidString), .text(event.contentID.rawValue), .integer(Int64(event.contentRevision)),
              .real(timestamp), .text(day), .text(event.timeZoneID), .text(event.skill), .text(event.outcome.rawValue),
              .integer(Int64(event.durationMilliseconds)), event.sessionID.map { .text($0.uuidString) } ?? .null,
              .integer(Int64(event.contentVersion))])
        try db.execute("""
        INSERT INTO item_progress(content_id,first_seen_at,last_seen_at,study_count,correct_count,incorrect_count)
        VALUES(?,?,?,?,?,?) ON CONFLICT(content_id) DO UPDATE SET
        first_seen_at=MIN(first_seen_at,excluded.first_seen_at),last_seen_at=MAX(last_seen_at,excluded.last_seen_at),
        study_count=study_count+excluded.study_count,correct_count=correct_count+excluded.correct_count,
        incorrect_count=incorrect_count+excluded.incorrect_count
        """, [.text(event.contentID.rawValue), .real(timestamp), .real(timestamp), .integer(Int64(studied)), .integer(Int64(correct)), .integer(Int64(incorrect))])
        try db.execute("""
        INSERT INTO daily_statistics(local_day,time_zone,study_count,correct_count,incorrect_count,duration_ms)
        VALUES(?,?,?,?,?,?) ON CONFLICT(local_day,time_zone) DO UPDATE SET
        study_count=study_count+excluded.study_count,correct_count=correct_count+excluded.correct_count,
        incorrect_count=incorrect_count+excluded.incorrect_count,duration_ms=duration_ms+excluded.duration_ms
        """, [.text(day), .text(event.timeZoneID), .integer(Int64(studied)), .integer(Int64(correct)), .integer(Int64(incorrect)), .integer(Int64(event.durationMilliseconds))])
    }
    func summary(now: Date) async throws -> LearningSummary {
        guard let row = try db.query("""
        SELECT COALESCE(SUM(study_count),0) AS studied,COALESCE(SUM(correct_count),0) AS correct,
        COALESCE(SUM(incorrect_count),0) AS incorrect,
        (SELECT COUNT(*) FROM favorites) AS favorites,
        (SELECT COUNT(DISTINCT content_id) FROM srs_state WHERE due_at<=?) AS due FROM item_progress
        """, [.real(now.timeIntervalSince1970)]).first else { return .empty }
        return LearningSummary(studyCount: try row.integer("studied"), correctCount: try row.integer("correct"),
                               incorrectCount: try row.integer("incorrect"), favoriteCount: try row.integer("favorites"), dueCount: try row.integer("due"))
    }
    func beginLesson(_ lessonID: ContentID, steps: [ContentID], contentVersion: Int, restart: Bool) async throws -> LessonSession {
        guard !steps.isEmpty, steps.count <= 200, Set(steps).count == steps.count, contentVersion > 0 else { throw LessonError.invalidSession }
        return try db.transaction {
            if let row = try db.query("SELECT * FROM lesson_sessions WHERE lesson_id=? AND status='active'", [.text(lessonID.rawValue)]).first {
                let current = try decodeSession(row)
                if !restart {
                    guard current.contentVersion <= contentVersion, current.stepIDs == steps else { throw LessonError.contentChanged }
                    // An unrelated content release must not abandon an unchanged lesson.
                    // Keep the cursor and immutable results; new actions use the current release.
                    try db.execute("UPDATE lesson_sessions SET content_version=? WHERE id=?", [.integer(Int64(contentVersion)), .text(current.id.uuidString)])
                    return try readSession(current.id)
                }
                try db.execute("UPDATE lesson_sessions SET status='abandoned',updated_at=? WHERE id=?", [.real(Date().timeIntervalSince1970), .text(current.id.uuidString)])
            }
            let id = UUID()
            let seed = Int64.random(in: 0...Int64.max)
            let json = String(decoding: try JSONEncoder().encode(steps.map(\.rawValue)), as: UTF8.self)
            let now = Date().timeIntervalSince1970
            try db.execute("INSERT INTO lesson_sessions(id,lesson_id,content_version,seed,step_ids_json,current_content_id,status,started_at,updated_at) VALUES(?,?,?,?,?,?,'active',?,?)",
                [.text(id.uuidString), .text(lessonID.rawValue), .integer(Int64(contentVersion)), .integer(seed), .text(json), .text(steps[0].rawValue), .real(now), .real(now)])
            try db.execute("INSERT INTO lesson_progress(lesson_id,status,started_at,last_content_id) VALUES(?,'started',?,?) ON CONFLICT(lesson_id) DO UPDATE SET last_content_id=excluded.last_content_id",
                [.text(lessonID.rawValue), .real(now), .text(steps[0].rawValue)])
            return try readSession(id)
        }
    }
    func lessonResults(sessionID: UUID) async throws -> [LessonStepResult] {
        try db.query("SELECT content_id,outcome,selected_choice_id FROM lesson_step_results WHERE session_id=?", [.text(sessionID.uuidString)]).map { row in
            guard let outcome = StudyOutcome(rawValue: try row.text("outcome")) else { throw LessonError.invalidSession }
            return LessonStepResult(contentID: ContentID(rawValue: try row.text("content_id")), outcome: outcome, selectedChoiceID: row["selected_choice_id"]?.string)
        }
    }
    /// Saves the immutable answer, event and all counters together. Cursor stays on feedback until Next.
    func submitStep(sessionID: UUID, event: StudyEvent, selectedChoiceID: String?) async throws {
        try db.transaction {
            let session = try readSession(sessionID)
            guard !session.completed, session.currentID == event.contentID, event.sessionID == sessionID,
                  event.contentVersion == session.contentVersion,
                  (event.outcome == .viewed && selectedChoiceID == nil) ||
                  ((event.outcome == .correct || event.outcome == .incorrect) && selectedChoiceID?.isEmpty == false) else { throw LessonError.invalidSession }
            if try !db.query("SELECT content_id FROM lesson_step_results WHERE session_id=? AND content_id=?", [.text(sessionID.uuidString), .text(event.contentID.rawValue)]).isEmpty { return }
            // A reused event UUID must not silently attach a different event to this result.
            guard try db.query("SELECT id FROM study_events WHERE id=?", [.text(event.id.uuidString)]).isEmpty else { throw LessonError.invalidSession }
            try recordInTransaction(event)
            try db.execute("INSERT INTO lesson_step_results(session_id,content_id,event_id,outcome,selected_choice_id) VALUES(?,?,?,?,?)",
                [.text(sessionID.uuidString), .text(event.contentID.rawValue), .text(event.id.uuidString), .text(event.outcome.rawValue), selectedChoiceID.map(SQLValue.text) ?? .null])
            try db.execute("UPDATE lesson_sessions SET updated_at=? WHERE id=?", [.real(event.occurredAt.timeIntervalSince1970), .text(sessionID.uuidString)])
        }
    }
    func advanceLesson(sessionID: UUID) async throws -> LessonSession {
        try db.transaction {
            let session = try readSession(sessionID)
            if session.completed { return session }
            guard let index = session.stepIDs.firstIndex(of: session.currentID),
                  try !db.query("SELECT content_id FROM lesson_step_results WHERE session_id=? AND content_id=?", [.text(sessionID.uuidString), .text(session.currentID.rawValue)]).isEmpty else { throw LessonError.invalidSession }
            let now = Date().timeIntervalSince1970
            if index + 1 == session.stepIDs.count {
                try db.execute("UPDATE lesson_sessions SET status='completed',updated_at=?,completed_at=? WHERE id=?", [.real(now), .real(now), .text(sessionID.uuidString)])
                try db.execute("UPDATE lesson_progress SET status='completed',completed_at=?,completed_count=completed_count+1,last_content_id=? WHERE lesson_id=?",
                    [.real(now), .text(session.currentID.rawValue), .text(session.lessonID.rawValue)])
            } else {
                let next = session.stepIDs[index + 1]
                try db.execute("UPDATE lesson_sessions SET current_content_id=?,updated_at=? WHERE id=?", [.text(next.rawValue), .real(now), .text(sessionID.uuidString)])
                try db.execute("UPDATE lesson_progress SET last_content_id=? WHERE lesson_id=?", [.text(next.rawValue), .text(session.lessonID.rawValue)])
            }
            return try readSession(sessionID)
        }
    }
    func lessonProgress() async throws -> [LessonProgress] {
        try db.query("SELECT p.lesson_id,p.completed_count,EXISTS(SELECT 1 FROM lesson_sessions s WHERE s.lesson_id=p.lesson_id AND s.status='active') AS active FROM lesson_progress p").map {
            LessonProgress(lessonID: ContentID(rawValue: try $0.text("lesson_id")), completedCount: try $0.integer("completed_count"), hasActiveSession: try $0.integer("active") == 1)
        }
    }
    private func readSession(_ id: UUID) throws -> LessonSession {
        guard let row = try db.query("SELECT * FROM lesson_sessions WHERE id=? AND status!='abandoned'", [.text(id.uuidString)]).first else { throw LessonError.invalidSession }
        return try decodeSession(row)
    }
    private func decodeSession(_ row: SQLRow) throws -> LessonSession {
        guard let id = UUID(uuidString: try row.text("id")) else { throw LessonError.invalidSession }
        let steps = try JSONDecoder().decode([String].self, from: Data(try row.text("step_ids_json").utf8)).map { ContentID(rawValue: $0) }
        let current = ContentID(rawValue: try row.text("current_content_id"))
        let seed = try row.integer("seed")
        guard !steps.isEmpty, Set(steps).count == steps.count, steps.contains(current), seed >= 0 else { throw LessonError.invalidSession }
        return LessonSession(id: id, lessonID: ContentID(rawValue: try row.text("lesson_id")), contentVersion: try row.integer("content_version"), seed: UInt64(seed), stepIDs: steps, currentID: current, completed: try row.text("status") == "completed")
    }

}
