import Foundation

extension SQLiteProgressRepository {
    func isFavorite(_ ref: LookupReference) async throws -> Bool {
        try !db.query("SELECT 1 FROM favorites WHERE content_id=? AND content_type=?",[.text(ref.contentID.rawValue),.text(ref.kind.rawValue)]).isEmpty
    }
    func setFavorite(_ ref: LookupReference, enabled: Bool) async throws {
        guard UUID(uuidString:ref.contentID.rawValue) != nil else { throw GrammarError.invalidState }
        if enabled {
            try db.execute("INSERT INTO favorites(content_id,created_at,content_type) VALUES(?,?,?) ON CONFLICT(content_id) DO NOTHING",[.text(ref.contentID.rawValue),.real(Date().timeIntervalSince1970),.text(ref.kind.rawValue)])
        } else {
            try db.execute("DELETE FROM favorites WHERE content_id=? AND content_type=?",[.text(ref.contentID.rawValue),.text(ref.kind.rawValue)])
        }
    }
    func savedReferences(list: SavedList, kind: LookupKind?, offset: Int, now: Date) async throws -> [LookupReference] {
        let filter = kind?.rawValue ?? ""
        let rows: [SQLRow]
        switch list {
        case .favorites:
            rows = try db.query("SELECT content_id,content_type FROM favorites WHERE (?='' OR content_type=?) ORDER BY created_at DESC,content_id LIMIT 30 OFFSET ?",[.text(filter),.text(filter),.integer(Int64(max(0,offset)))])
        case .recent:
            rows = try db.query("SELECT content_id,content_type FROM recent_content WHERE (?='' OR content_type=?) ORDER BY viewed_at DESC,content_id LIMIT 30 OFFSET ?",[.text(filter),.text(filter),.integer(Int64(max(0,offset)))])
        case .difficult:
            // Recent repeated difficulty, not a permanent label from one historical error.
            rows = try db.query("""
            SELECT content_id,skill AS content_type FROM srs_state
            WHERE skill IN ('vocabulary','grammar') AND (?='' OR skill=?)
            AND algorithm=? AND algorithm_version=? AND last_review_at>=? AND last_review_at<=?
            AND json_extract(state_json,'$.failureCount')>=2
            AND json_extract(state_json,'$.consecutiveSuccesses')<2
            AND json_extract(state_json,'$.stage')<4
            AND json_extract(state_json,'$.lastResult') IN ('difficult','unsure')
            ORDER BY last_review_at DESC,content_id LIMIT 30 OFFSET ?
            """,[.text(filter),.text(filter),.text(StepReviewScheduler.algorithm),.integer(Int64(StepReviewScheduler.version)),.real(now.addingTimeInterval(-30*86400).timeIntervalSince1970),.real(now.timeIntervalSince1970),.integer(Int64(max(0,offset)))])
        }
        return try rows.map {
            guard let kind = LookupKind(rawValue:try $0.text("content_type")) else { throw GrammarError.invalidState }
            return LookupReference(contentID:ContentID(rawValue:try $0.text("content_id")),kind:kind)
        }
    }
    func rememberLookup(_ ref: LookupReference, now: Date) async throws {
        try db.transaction {
            try db.execute("INSERT INTO recent_content(content_id,content_type,viewed_at) VALUES(?,?,?) ON CONFLICT(content_id,content_type) DO UPDATE SET viewed_at=excluded.viewed_at",[.text(ref.contentID.rawValue),.text(ref.kind.rawValue),.real(now.timeIntervalSince1970)])
            try db.execute("DELETE FROM recent_content WHERE rowid NOT IN (SELECT rowid FROM recent_content ORDER BY viewed_at DESC,content_id LIMIT 30)")
        }
    }
    func beginLookupPractice(ids: [ContentID], kind: LookupKind, now: Date) async throws -> ReviewSession {
        guard !ids.isEmpty, ids.count <= 20, Set(ids).count == ids.count else { throw ReviewError.invalidState }
        return try db.transaction {
            let skill = kind.rawValue + "_practice"
            if let row = try db.query("SELECT id FROM review_sessions WHERE skill=? AND status='active'",[.text(skill)]).first {
                guard let id = UUID(uuidString:try row.text("id")) else { throw ReviewError.invalidState }
                return try readReviewSession(id)
            }
            let id = UUID(), stamp = now.timeIntervalSince1970
            try db.execute("INSERT INTO review_sessions(id,skill,status,started_at,updated_at) VALUES(?,?,'active',?,?)",[.text(id.uuidString),.text(skill),.real(stamp),.real(stamp)])
            for (ordinal,contentID) in ids.enumerated() {
                try db.execute("INSERT INTO review_items(session_id,content_id,ordinal) VALUES(?,?,?)",[.text(id.uuidString),.text(contentID.rawValue),.integer(Int64(ordinal))])
            }
            return try readReviewSession(id)
        }
    }
}
