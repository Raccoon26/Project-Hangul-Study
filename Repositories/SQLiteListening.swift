import Foundation

extension SQLiteContentRepository {
    func listeningBatches(level: LearningLevel, after: Int) async throws -> [(Int,Int)] {
        guard try db.query("PRAGMA user_version").first?.integer("user_version") == 4 else { return [] }
        return try db.query("SELECT l.learning_order/20 AS batch,COUNT(*) AS n FROM listening_items l JOIN content_items i ON i.id=l.id WHERE i.is_active=1 AND i.level=? AND l.learning_order/20>? GROUP BY l.learning_order/20 ORDER BY batch LIMIT 30",[.text(level.rawValue),.integer(Int64(after))]).map { (try $0.integer("batch"),try $0.integer("n")) }
    }
    func listeningBatchIDs(level: LearningLevel, batch: Int) async throws -> [ContentID] {
        guard batch >= 0, batch < Int.max/20 else { throw GrammarError.invalidState }
        return try db.query("SELECT l.id FROM listening_items l JOIN content_items i ON i.id=l.id WHERE i.is_active=1 AND i.level=? AND l.learning_order>=? AND l.learning_order<? ORDER BY l.learning_order,l.id LIMIT 20",[.text(level.rawValue),.integer(Int64(batch*20)),.integer(Int64((batch+1)*20))]).map { ContentID(rawValue:try $0.text("id")) }
    }
    func listeningQuestions(level: LearningLevel?, ids: [ContentID]?) async throws -> [ListeningQuestion] {
        guard try db.query("PRAGMA user_version").first?.integer("user_version") == 4 else { return [] }
        if let ids = ids { guard !ids.isEmpty, ids.count <= 20 else { return [] } }
        var sql = """
        SELECT q.*,l.id AS item_id,l.source_example_id,l.audio_mode,e.korean,e.japanese,
        i.revision,i.level,m.relative_path,m.sha256
        FROM listening_items l JOIN content_items i ON i.id=l.id
        JOIN examples e ON e.id=l.source_example_id JOIN content_items ei ON ei.id=e.id
        JOIN questions q ON q.listening_id=l.id JOIN content_items qi ON qi.id=q.id
        LEFT JOIN media_assets m ON m.id=l.audio_asset_id
        WHERE i.is_active=1 AND ei.is_active=1 AND qi.is_active=1
        """
        var values: [SQLValue] = []
        if let level = level { sql += " AND i.level=?"; values.append(.text(level.rawValue)) }
        if let ids = ids {
            sql += " AND l.id IN (" + Array(repeating:"?",count:ids.count).joined(separator:",") + ")"
            values += ids.map { .text($0.rawValue) }
        }
        sql += " ORDER BY l.learning_order,l.id LIMIT 20"
        return try db.query(sql,values).map { row in
            struct Answer: Decodable { let correct_choice_ids: [String]?; let accepted: [String]? }
            struct Rubric: Decodable { let listening_task: ListeningTask }
            let a = try JSONDecoder().decode(Answer.self,from:Data(try row.text("answer_json").utf8))
            let r = try JSONDecoder().decode(Rubric.self,from:Data(try row.text("rubric_json").utf8))
            let qid = try row.text("id")
            let choices = try db.query("SELECT choice_id,text FROM question_choices WHERE question_id=? ORDER BY ordinal",[.text(qid)]).map { QuizChoice(id:try $0.text("choice_id"),text:try $0.text("text")) }
            let asset: RecordingAsset?
            if let path = row["relative_path"]?.string, let hash = row["sha256"]?.string { asset = RecordingAsset(relativePath:path,sha256:hash) } else { asset = nil }
            guard let level = LearningLevel(rawValue:try row.text("level")) else { throw GrammarError.changedContent }
            let question = ListeningQuestion(id:ContentID(rawValue:qid),itemID:ContentID(rawValue:try row.text("item_id")),revision:try row.integer("revision"),sourceID:ContentID(rawValue:try row.text("source_example_id")),level:level,task:r.listening_task,prompt:try row.text("prompt_ja"),transcript:try row.text("korean"),translation:try row.text("japanese"),explanation:try row.text("explanation_ja"),choices:choices,correctID:a.correct_choice_ids?.first,accepted:a.accepted ?? [],recordingRequired:try row.text("audio_mode") == "recorded_required",recording:asset)
            try question.validate(); return question
        }
    }
}
extension SQLiteProgressRepository {
    func activeListening(scope: String) async throws -> ListeningSession? { try readActiveListening(scope:scope) }
    private func readActiveListening(scope: String) throws -> ListeningSession? {
        guard let row = try db.query("SELECT state_json FROM listening_sessions WHERE scope=? AND completed=0",[.text(scope)]).first else { return nil }
        let s = try JSONDecoder().decode(ListeningSession.self,from:Data(try row.text("state_json").utf8)); try s.validate(); return s
    }
    func listeningDue(now: Date) async throws -> (Int,[ContentID]) {
        guard now.timeIntervalSince1970.isFinite else { throw ReviewError.invalidState }
        let count = try db.query("SELECT COUNT(*) AS n FROM srs_state WHERE skill='listening' AND algorithm=? AND algorithm_version=? AND due_at<=?",[.text(StepReviewScheduler.algorithm),.integer(Int64(StepReviewScheduler.version)),.real(now.timeIntervalSince1970)]).first?.integer("n") ?? 0
        let ids = try db.query("SELECT content_id FROM srs_state WHERE skill='listening' AND algorithm=? AND algorithm_version=? AND due_at<=? ORDER BY due_at,content_id LIMIT 20",[.text(StepReviewScheduler.algorithm),.integer(Int64(StepReviewScheduler.version)),.real(now.timeIntervalSince1970)]).map { ContentID(rawValue:try $0.text("content_id")) }
        return (count,ids)
    }
    func beginListening(scope: String, questions: [ListeningQuestion], version: Int, review: Bool) async throws -> ListeningSession {
        try db.transaction {
            if let s = try readActiveListening(scope:scope) { return s }
            var snapshot = questions
            let seed = UInt64.random(in: 0...UInt64.max)
            for index in snapshot.indices { snapshot[index].choices = QuizOptions.ordered(snapshot[index].choices,seed:seed,contentID:snapshot[index].id) }
            let now = Date()
            let s = ListeningSession(id:UUID(),scope:scope,questions:snapshot,contentVersion:version,isReview:review,startedAt:now,updatedAt:now)
            try s.validate(); try saveListening(s); return s
        }
    }
    private func saveListening(_ s: ListeningSession) throws {
        let json = String(decoding:try JSONEncoder().encode(s),as:UTF8.self)
        try db.execute("INSERT INTO listening_sessions(id,scope,state_json,completed) VALUES(?,?,?,?) ON CONFLICT(id) DO UPDATE SET state_json=excluded.state_json,completed=excluded.completed",[.text(s.id.uuidString),.text(s.scope),.text(json),.integer(s.completed ? 1 : 0)])
    }
    func updateListening(_ expected: ListeningSession, action: ListeningAction, now: Date) async throws -> ListeningSession {
        try db.transaction {
            guard let row = try db.query("SELECT state_json FROM listening_sessions WHERE id=?",[.text(expected.id.uuidString)]).first else { throw GrammarError.invalidState }
            var s = try JSONDecoder().decode(ListeningSession.self,from:Data(try row.text("state_json").utf8))
            guard s.revision == expected.revision, let q = s.current else { throw VocabularyStudyError.staleState }
            let retry = s.retrying
            try s.apply(action,at:now)
            switch action {
            case .played(let speed):
                try db.execute("INSERT INTO listening_plays VALUES(?,?,?,?,?) ON CONFLICT(session_id,question_id) DO UPDATE SET normal_count=normal_count+excluded.normal_count,slow_count=slow_count+excluded.slow_count,last_played_at=excluded.last_played_at",[.text(s.id.uuidString),.text(q.id.rawValue),.integer(speed == .normal ? 1 : 0),.integer(speed == .slow ? 1 : 0),.real(now.timeIntervalSince1970)])
            case .submit(let answer):
                guard let result = s.result else { throw GrammarError.invalidState }
                var due: SQLValue = .null
                if !retry {
                    let existing = try readSRS(q.itemID,skill:"listening")
                    let next: SRSState?
                    if let previous = existing {
                        if s.isReview {
                            next = try StepReviewScheduler.next(previous:previous,result:result == .correct ? .remembered : result == .spacing ? .unsure : .difficult,at:now,timeZoneID:TimeZone.current.identifier)
                        } else { next = nil }
                    } else { next = try StepReviewScheduler.initial(at:now,neededRepetition:result != .correct,timeZoneID:TimeZone.current.identifier) }
                    if let next = next {
                        due = .real(next.nextReviewAt.timeIntervalSince1970)
                        try db.execute("INSERT INTO srs_state(content_id,skill,algorithm,algorithm_version,state_json,due_at,last_review_at,updated_at) VALUES(?,'listening',?,?,?,?,?,?) ON CONFLICT(content_id,skill) DO UPDATE SET state_json=excluded.state_json,due_at=excluded.due_at,last_review_at=excluded.last_review_at,updated_at=excluded.updated_at",[.text(q.itemID.rawValue),.text(StepReviewScheduler.algorithm),.integer(Int64(StepReviewScheduler.version)),.text(try encodeSRS(next)),due,next.lastReviewedAt.map { .real($0.timeIntervalSince1970) } ?? .null,.real(now.timeIntervalSince1970)])
                    }
                }
                try db.execute("INSERT INTO listening_attempts VALUES(?,?,?,?,?,?,?,?,?,?)",[.text(s.id.uuidString),.text(q.id.rawValue),.integer(retry ? 1 : 0),.text(q.itemID.rawValue),.text(q.task.rawValue),.text(answer),.text(result.rawValue),.integer(s.isReview ? 1 : 0),.real(now.timeIntervalSince1970),due])
                try recordInTransaction(StudyEvent(id:UUID(),contentID:q.itemID,contentRevision:q.revision,contentVersion:s.contentVersion,occurredAt:now,timeZoneID:TimeZone.current.identifier,skill:retry ? "listening_retry" : "listening_"+q.task.rawValue,outcome:result == .correct ? .correct : .incorrect,durationMilliseconds:0,sessionID:s.id))
            case .next: break
            }
            try saveListening(s); return s
        }
    }
}
