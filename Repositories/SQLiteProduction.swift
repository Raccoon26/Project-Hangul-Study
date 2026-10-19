import Foundation
extension SQLiteContentRepository {
    func productionVocabulary(after: String) async throws -> [(ContentID,String)] {
        try db.query("SELECT DISTINCT v.id,v.headword FROM vocabulary v JOIN content_links l ON l.target_id=v.id JOIN questions q ON q.id=l.source_id JOIN content_items i ON i.id=q.id JOIN content_items vi ON vi.id=v.id WHERE vi.is_active=1 AND l.relation='question_target' AND q.question_type='text_input' AND json_extract(q.rubric_json,'$.production')=1 AND i.is_active=1 AND v.id>? ORDER BY v.id LIMIT 30", [.text(after)]).map { (ContentID(rawValue:try $0.text("id")),try $0.text("headword")) }
    }
    func productionQuestions(id: ContentID) async throws -> [ProductionQuestion] {
        let rows = try db.query("SELECT q.*,(SELECT m.meaning_ja FROM meanings m JOIN content_items mi ON mi.id=m.id WHERE m.vocabulary_id=v.id AND mi.is_active=1 ORDER BY m.ordinal,m.id LIMIT 1) AS meaning_ja,v.headword,v.part_of_speech,v.irregular_type,i.revision,(SELECT revision FROM content_items WHERE id=v.id) AS vocabulary_revision FROM questions q JOIN content_links l ON l.source_id=q.id JOIN vocabulary v ON v.id=l.target_id JOIN content_items i ON i.id=q.id JOIN content_items vi ON vi.id=v.id WHERE vi.is_active=1 AND l.relation='question_target' AND v.id=? AND q.question_type='text_input' AND json_extract(q.rubric_json,'$.production')=1 AND i.is_active=1 ORDER BY q.id LIMIT 21", [.text(id.rawValue)])
        guard !rows.isEmpty, rows.count <= 20 else { throw GrammarError.changedContent }
        return try rows.map { row in
            struct Answer: Decodable { let accepted: [String] }
            struct Rubric: Decodable { let form: ConjugationForm; let spacing_warning: Bool; let overrides: [String:String]; let mode: String }
            let a = try JSONDecoder().decode(Answer.self,from:Data(try row.text("answer_json").utf8))
            let r = try JSONDecoder().decode(Rubric.self,from:Data(try row.text("rubric_json").utf8))
            let result = try ConjugationEngine.generate(lemma:row.text("headword"),partOfSpeech:row.text("part_of_speech"),irregular:row["irregular_type"]?.string,form:r.form,overrides:r.overrides)
            guard r.mode == "sentence" || a.accepted.contains(result.form) else { throw GrammarError.changedContent }
            return ProductionQuestion(id:ContentID(rawValue:try row.text("id")),revision:try row.integer("revision"),vocabularyID:id,vocabularyRevision:try row.integer("vocabulary_revision"),
                grammarID:try db.query("SELECT g.id FROM content_links l JOIN grammar g ON g.id=l.target_id WHERE l.source_id=? AND l.relation='prerequisite' LIMIT 1",[.text(row.text("id"))]).first.map { ContentID(rawValue:try $0.text("id")) },
                lemma:try row.text("headword"),meaning:try row.text("meaning_ja"),prompt:try row.text("prompt_ja"),korean:row["prompt_ko"]?.string,
                explanation:try row.text("explanation_ja"),accepted:a.accepted,form:r.form,generated:result.form,spacingWarning:r.spacing_warning)
        }
    }
}
extension SQLiteProgressRepository {
    func activeProduction(scope: ContentID) async throws -> ProductionSession? {
        guard let row = try db.query("SELECT state_json FROM production_sessions WHERE scope_id=? AND completed=0", [.text(scope.rawValue)]).first else { return nil }
        let session = try JSONDecoder().decode(ProductionSession.self, from:Data(try row.text("state_json").utf8))
        try session.validate(); return session
    }
    func beginProduction(scope: ContentID, questions: [ProductionQuestion], version: Int) async throws -> ProductionSession {
        try db.transaction {
            if let row = try db.query("SELECT state_json FROM production_sessions WHERE scope_id=? AND completed=0", [.text(scope.rawValue)]).first {
                let s = try JSONDecoder().decode(ProductionSession.self,from:Data(try row.text("state_json").utf8)); try s.validate(); return s
            }
            var s = ProductionSession(id:UUID(),scope:scope,questions:questions,contentVersion:version)
            s.updatedAt = Date()
            try s.validate(); try saveProduction(s); return s
        }
    }
    private func saveProduction(_ s: ProductionSession) throws {
        let json = String(decoding:try JSONEncoder().encode(s),as:UTF8.self)
        try db.execute("INSERT INTO production_sessions(id,scope_id,state_json,completed) VALUES(?,?,?,?) ON CONFLICT(id) DO UPDATE SET state_json=excluded.state_json,completed=excluded.completed", [.text(s.id.uuidString),.text(s.scope.rawValue),.text(json),.integer(s.completed ? 1 : 0)])
    }
    func updateProduction(_ expected: ProductionSession, answer: String?) async throws -> ProductionSession {
        try db.transaction {
            guard let row = try db.query("SELECT state_json FROM production_sessions WHERE id=?", [.text(expected.id.uuidString)]).first else { throw GrammarError.invalidState }
            var s = try JSONDecoder().decode(ProductionSession.self,from:Data(try row.text("state_json").utf8))
            try s.validate()
            guard s.revision == expected.revision, let q = s.current else { throw VocabularyStudyError.staleState }
            if let answer = answer {
                guard !s.studying, s.result == nil, !ProductionAnswer.normalize(answer).isEmpty, answer.count <= 500 else { throw GrammarError.invalidState }
                let result = ProductionAnswer.judge(answer,accepted:q.accepted,spacingWarning:q.spacingWarning)
                s.answer = answer; s.result = result
                if result != .correct && !s.retrying { s.retry.append(s.position) }
                try recordInTransaction(StudyEvent(id:UUID(),contentID:q.vocabularyID,contentRevision:q.vocabularyRevision,contentVersion:s.contentVersion,occurredAt:Date(),timeZoneID:TimeZone.current.identifier,skill:(s.retrying ? "production_retry_" : "production_")+q.form.rawValue,outcome:result == .correct ? .correct : .incorrect,durationMilliseconds:0,sessionID:s.id))
                // Existing vocabulary review can revisit this lemma; never reset an existing schedule.
                let state = try StepReviewScheduler.initial(at:Date(),neededRepetition:result != .correct,timeZoneID:TimeZone.current.identifier)
                try db.execute("INSERT INTO srs_state(content_id,skill,algorithm,algorithm_version,state_json,due_at,updated_at) VALUES(?,'vocabulary',?,?,?,?,?) ON CONFLICT(content_id,skill) DO NOTHING", [.text(q.vocabularyID.rawValue),.text(StepReviewScheduler.algorithm),.integer(Int64(StepReviewScheduler.version)),.text(try encodeSRS(state)),.real(state.nextReviewAt.timeIntervalSince1970),.real(Date().timeIntervalSince1970)])
            } else if s.studying { s.studying = false }
            else {
                guard s.result != nil else { throw GrammarError.invalidState }
                s.result = nil; s.answer = nil
                if s.retrying { s.position = s.retry.isEmpty ? s.questions.count : s.retry.removeFirst() }
                else {
                    s.position += 1
                    if s.position == s.questions.count && !s.retry.isEmpty { s.retrying = true; s.position = s.retry.removeFirst() }
                }
                s.studying = !s.retrying
            }
            s.revision += 1; s.updatedAt = Date(); try s.validate(); try saveProduction(s); return s
        }
    }
}
