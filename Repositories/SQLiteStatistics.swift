import Foundation

extension SQLiteProgressRepository {
    func statistics(now: Date, timeZone: TimeZone) async throws -> LearningStatistics {
        // One read transaction gives a consistent snapshot across counters and sessions.
        try db.transaction {
            var windows: [ActivityWindow] = []
            for days in [1,7,30] {
                let bounds: [SQLValue] = [.real(StatisticsCalendar.start(days:days,now:now,timeZone:timeZone).timeIntervalSince1970),.real(now.timeIntervalSince1970)]
                let rows = try db.query("""
                SELECT COUNT(CASE WHEN outcome!='skipped' THEN 1 END) AS actions,
                COUNT(CASE WHEN outcome='correct' THEN 1 END) AS correct,
                COUNT(CASE WHEN outcome='incorrect' THEN 1 END) AS incorrect,
                COUNT(CASE WHEN skill GLOB 'production_*' AND skill NOT GLOB 'production_retry_*' AND outcome='correct' THEN 1 END) AS pc,
                COUNT(CASE WHEN skill GLOB 'production_*' AND skill NOT GLOB 'production_retry_*' AND outcome='incorrect' THEN 1 END) AS pw,
                COUNT(CASE WHEN skill GLOB 'listening_*' AND skill!='listening_retry' AND outcome='correct' THEN 1 END) AS lc,
                COUNT(CASE WHEN skill GLOB 'listening_*' AND skill!='listening_retry' AND outcome='incorrect' THEN 1 END) AS lw
                FROM study_events WHERE occurred_at>=? AND occurred_at<=?
                """,bounds)
                guard let row = rows.first else { throw DatabaseError.invalidData("Missing statistics aggregate") }
                let reviews = try db.query("""
                SELECT
                (SELECT COUNT(*) FROM review_items i JOIN review_sessions s ON s.id=i.session_id
                 WHERE s.skill IN ('vocabulary','grammar') AND i.reviewed_at>=? AND i.reviewed_at<=?) +
                (SELECT COUNT(*) FROM listening_attempts WHERE is_review=1 AND attempt=0 AND occurred_at>=? AND occurred_at<=?) AS value
                """,bounds+bounds).first?.integer("value") ?? 0
                windows.append(ActivityWindow(days:days,actions:try row.integer("actions"),correct:try row.integer("correct"),incorrect:try row.integer("incorrect"),reviews:reviews,
                    productionCorrect:try row.integer("pc"),productionWrong:try row.integer("pw"),listeningCorrect:try row.integer("lc"),listeningWrong:try row.integer("lw")))
            }
            let row = try db.query("""
            SELECT
            (SELECT COUNT(DISTINCT content_id) FROM study_events WHERE skill IN ('vocabulary_pass','vocabulary_review','vocabulary_practice') OR skill GLOB 'production_*') AS seen,
            (SELECT COUNT(DISTINCT i.content_id) FROM vocabulary_set_items i JOIN vocabulary_sets s ON s.id=i.set_id WHERE s.completed_count>0) AS passed,
            (SELECT COUNT(DISTINCT content_id) FROM study_events WHERE skill GLOB 'grammar*') AS grammar
            """).first
            let states = try db.query("""
            SELECT skill,COUNT(CASE WHEN json_extract(state_json,'$.stage')<4 THEN 1 END) AS learning,
            COUNT(CASE WHEN json_extract(state_json,'$.stage')>=4 THEN 1 END) AS stable
            FROM srs_state WHERE skill IN ('vocabulary','grammar') AND algorithm=? AND algorithm_version=? GROUP BY skill
            """,[.text(StepReviewScheduler.algorithm),.integer(Int64(StepReviewScheduler.version))])
            let word = try states.first { try $0.text("skill") == "vocabulary" }
            let grammar = try states.first { try $0.text("skill") == "grammar" }
            return LearningStatistics(windows:windows,seenWords:try row?.integer("seen") ?? 0,passedWords:try row?.integer("passed") ?? 0,
                reviewingWords:try word?.integer("learning") ?? 0,stableWords:try word?.integer("stable") ?? 0,studiedGrammar:try row?.integer("grammar") ?? 0,
                reviewingGrammar:try grammar?.integer("learning") ?? 0,stableGrammar:try grammar?.integer("stable") ?? 0)
        }
    }
    func unseenVocabulary(in ids: [ContentID]) async throws -> Int {
        guard ids.count <= 200, Set(ids).count == ids.count else { throw ReviewError.invalidState }
        guard !ids.isEmpty else { return 0 }
        let slots = Array(repeating:"?",count:ids.count).joined(separator:",")
        let count = try db.query("SELECT COUNT(DISTINCT content_id) AS n FROM study_events WHERE content_id IN (\(slots)) AND (skill IN ('vocabulary_pass','vocabulary_review','vocabulary_practice') OR skill GLOB 'production_*')",ids.map { .text($0.rawValue) }).first?.integer("n") ?? 0
        return ids.count-count
    }
    func maintenanceWords(now: Date, limit: Int) async throws -> [ContentID] {
        // Scheduled items belong exclusively to SRS. Never pull future-due items forward.
        // Do not interrupt the membership of an active round; lookup views are not learning.
        try db.query("""
        SELECT p.content_id FROM item_progress p
        WHERE p.last_seen_at<=? AND EXISTS(SELECT 1 FROM study_events e WHERE e.content_id=p.content_id AND e.skill IN ('vocabulary_pass','vocabulary_review','vocabulary_practice'))
        AND NOT EXISTS(SELECT 1 FROM srs_state s WHERE s.content_id=p.content_id AND s.skill='vocabulary')
        AND NOT EXISTS(SELECT 1 FROM vocabulary_set_items i JOIN vocabulary_sessions s ON s.set_id=i.set_id WHERE i.content_id=p.content_id AND s.status='active')
        ORDER BY p.last_seen_at,p.content_id LIMIT ?
        """,[.real(now.addingTimeInterval(-30*86400).timeIntervalSince1970),.integer(Int64(min(20,max(1,limit))))]).map { ContentID(rawValue:try $0.text("content_id")) }
    }
}
