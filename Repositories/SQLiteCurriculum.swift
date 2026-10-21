import Foundation

extension SQLiteContentRepository {
    func curriculumIDs(level: LearningLevel, kind: String, after: String) async throws -> [ContentID] {
        guard ["vocabulary","grammar","listening","lesson"].contains(kind) else { throw GrammarError.invalidState }
        // Content membership is queried in bounded pages, never copied into preferences.
        let actual = kind
        return try db.query("SELECT id FROM content_items WHERE is_active=1 AND level=? AND kind=? AND id>? AND (?!='lesson' OR NOT EXISTS(SELECT 1 FROM lesson_items li JOIN content_items typed ON typed.id=li.content_id WHERE li.lesson_id=content_items.id AND typed.kind IN ('grammar','listening'))) ORDER BY id LIMIT 200",[.text(level.rawValue),.text(actual),.text(after),.text(kind)]).map { ContentID(rawValue:try $0.text("id")) }
    }
    func curriculumProduction(level: LearningLevel, after: String) async throws -> [(ContentID,String)] {
        try db.query("SELECT DISTINCT v.id,v.headword FROM vocabulary v JOIN content_items i ON i.id=v.id JOIN content_links l ON l.target_id=v.id JOIN questions q ON q.id=l.source_id JOIN content_items qi ON qi.id=q.id WHERE i.is_active=1 AND qi.is_active=1 AND i.level=? AND v.id>? AND l.relation='question_target' AND q.question_type='text_input' AND json_extract(q.rubric_json,'$.production')=1 ORDER BY v.id LIMIT 30",[.text(level.rawValue),.text(after)]).map { (ContentID(rawValue:try $0.text("id")),try $0.text("headword")) }
    }
    func diagnosticItems() async throws -> [DiagnosticItem] {
        var items: [DiagnosticItem] = []
        // Reuse active authored quizzes. No diagnostic result is a learning completion.
        let allCourses = try await courses()
        for course in allCourses {
            for lesson in course.lessons {
                let steps = try await lessonSteps(for:lesson.id)
                for step in steps where step.kind == .quiz && !step.requiresListening && step.skill == "hangul" {
                    if items.count < 2 { items.append(DiagnosticItem(id:step.id,area:"hangul",prompt:step.title,korean:step.symbol.isEmpty ? nil : step.symbol,choices:step.choices,correct:step.correctChoiceID,accepted:[],audio:nil)) }
                }
                if items.count == 2 { break }
            }
            if items.count == 2 { break }
        }
        let words = try await vocabulary(matching:VocabularyQuery(level:.intro),after:nil,limit:8)
        var options: [Vocabulary] = []
        for word in words where !options.contains(where: { $0.meaning == word.meaning }) { options.append(word) }
        if options.count >= 4 {
            let candidates = Array(options.prefix(4))
            for word in candidates.prefix(2) {
                items.append(DiagnosticItem(id:word.id,area:"vocabulary",prompt:"この単語の意味を選んでください",korean:word.headword,choices:candidates.map { QuizChoice(id:$0.id.rawValue,text:$0.meaning) },correct:word.id.rawValue,accepted:[],audio:nil))
            }
        }
        let grammar = try await grammarLessons(level:.intro,after:-1,limit:2)
        for lesson in grammar {
            let ids = try await grammarIDs(lesson:lesson.id)
            if let id = ids.first {
                let card = try await grammarCard(id:id)
                if let q = card.questions.first {
                items.append(DiagnosticItem(id:q.id,area:"grammar",prompt:q.prompt,korean:q.korean,choices:q.choices,correct:q.correctID,accepted:[],audio:nil))
                }
            }
        }
        // Expanding later levels must not change the difficulty of placement checks.
        let production = try await curriculumProduction(level:.intro,after:"")
        if let first = production.first {
            let questions = try await productionQuestions(id:first.0)
            if let q = questions.first {
            items.append(DiagnosticItem(id:q.id,area:"production",prompt:q.prompt,korean:q.korean,choices:[],correct:nil,accepted:q.accepted,audio:nil))
            }
        }
        let listening = try await listeningQuestions(level:.intro,ids:nil)
        if let q = listening.first(where: { !$0.choices.isEmpty }) {
            items.append(DiagnosticItem(id:q.id,area:"listening",prompt:q.prompt,korean:nil,choices:q.choices,correct:q.correctID,accepted:[],audio:q.audio))
        }
        return items
    }
}
extension SQLiteProgressRepository {
    private func readCurriculum<T: Decodable>(_ key: String, as: T.Type) throws -> T? {
        guard let text = try db.query("SELECT value FROM user_metadata WHERE key=?",[.text(key)]).first?.text("value") else { return nil }
        return try JSONDecoder().decode(T.self,from:Data(text.utf8))
    }
    private func writeCurriculum<T: Encodable>(_ value: T,key: String) throws {
        let text = String(decoding:try JSONEncoder().encode(value),as:UTF8.self)
        try db.execute("INSERT INTO user_metadata(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",[.text(key),.text(text)])
    }
    func curriculumProfile() async throws -> CurriculumProfile? {
        let value = try readCurriculum("curriculum.profile.v1",as:CurriculumProfile.self)
        guard value == nil || value?.version == 1 else { throw GrammarError.invalidState }
        return value
    }
    func saveCurriculumProfile(_ value: CurriculumProfile) async throws {
        guard value.version == 1 else { throw GrammarError.invalidState }
        try writeCurriculum(value,key:"curriculum.profile.v1")
    }
    func diagnosticSession() async throws -> DiagnosticSession? {
        let value = try readCurriculum("curriculum.diagnostic.v1",as:DiagnosticSession.self)
        try value?.validate(); return value
    }
    func beginDiagnostic(items: [DiagnosticItem], version: Int, restart: Bool) async throws -> DiagnosticSession {
        try db.transaction {
            if !restart, let old = try readCurriculum("curriculum.diagnostic.v1",as:DiagnosticSession.self) { try old.validate(); return old }
            guard !items.isEmpty, items.count <= 10 else { throw GrammarError.changedContent }
            var s = DiagnosticSession(id:UUID(),contentVersion:version,items:items)
            let seed = UInt64.random(in:0...UInt64.max)
            for i in s.items.indices { s.items[i].choices = QuizOptions.ordered(s.items[i].choices,seed:seed,contentID:s.items[i].id) }
            try s.validate(); try writeCurriculum(s,key:"curriculum.diagnostic.v1"); return s
        }
    }
    func answerDiagnostic(id: UUID,revision: Int,answer: String?) async throws -> DiagnosticSession {
        try db.transaction {
            guard var s = try readCurriculum("curriculum.diagnostic.v1",as:DiagnosticSession.self), s.id == id else { throw VocabularyStudyError.staleState }
            try s.answer(answer,expectedRevision:revision)
            try s.validate(); try writeCurriculum(s,key:"curriculum.diagnostic.v1"); return s
        }
    }
    func curriculumResume() async throws -> CurriculumRoute? {
        // Latest committed activity across modules. Default Codable dates use the 2001 epoch.
        // Legacy production snapshots fall back to their latest persisted learning event.
        // No progress snapshot is rewritten.
        guard let r = try db.query("""
        SELECT kind,target,level FROM (
          SELECT 'vocabulary' AS kind,v.id AS target,v.level,1 AS priority,s.updated_at AS recent
          FROM vocabulary_sessions s JOIN vocabulary_sets v ON v.id=s.set_id WHERE s.status='active'
          UNION ALL SELECT 'grammar',lesson_id,NULL,2,updated_at FROM grammar_sessions WHERE status='active'
          UNION ALL SELECT 'production',scope_id,NULL,3,COALESCE(json_extract(state_json,'$.updatedAt')+978307200,(SELECT MAX(occurred_at) FROM study_events e WHERE e.content_id=production_sessions.scope_id AND e.session_id=production_sessions.id),0) FROM production_sessions WHERE completed=0
          UNION ALL SELECT 'listening',scope,NULL,4,COALESCE(json_extract(state_json,'$.updatedAt')+978307200,0) FROM listening_sessions WHERE completed=0
          UNION ALL SELECT 'lesson',lesson_id,NULL,5,updated_at FROM lesson_sessions WHERE status='active'
          UNION ALL SELECT CASE WHEN skill IN ('vocabulary_practice','grammar_practice') THEN 'practice' ELSE 'review' END,CASE WHEN skill IN ('vocabulary_practice','grammar_practice') THEN id ELSE skill END,NULL,6,updated_at FROM review_sessions WHERE status='active'
        ) ORDER BY recent DESC,priority,target LIMIT 1
        """).first else { return nil }
        let levelText = r["level"]?.string
        return CurriculumRoute(kind:try r.text("kind"),target:try r.text("target"),level:levelText.flatMap { LearningLevel(rawValue:$0) })
    }
    func curriculumCounts(ids: [ContentID], kind: String) async throws -> (Int,Int) {
        guard !ids.isEmpty else { return (0,0) }
        guard ids.count <= 200 else { throw GrammarError.invalidState }
        let slots = Array(repeating:"?",count:ids.count).joined(separator:",")
        let values: [SQLValue] = ids.map { .text($0.rawValue) }
        let sql: String
        switch kind {
        case "vocabulary": sql = "SELECT COUNT(DISTINCT i.content_id) AS n FROM vocabulary_set_items i JOIN vocabulary_sets s ON s.id=i.set_id WHERE s.completed_count>0 AND i.content_id IN (\(slots))"
        case "grammar": sql = "SELECT COUNT(DISTINCT content_id) AS n FROM srs_state WHERE skill='grammar' AND content_id IN (\(slots))"
        case "listening": sql = "SELECT COUNT(DISTINCT a.item_id) AS n FROM listening_attempts a JOIN listening_sessions s ON s.id=a.session_id WHERE s.completed=1 AND a.attempt=0 AND a.item_id IN (\(slots))"
        case "lesson": sql = "SELECT COUNT(*) AS n FROM lesson_progress WHERE completed_count>0 AND lesson_id IN (\(slots))"
        default: throw GrammarError.invalidState
        }
        let done = try db.query(sql,values).first?.integer("n") ?? 0
        let stable = try db.query("SELECT COUNT(*) AS n FROM srs_state WHERE skill=? AND json_extract(state_json,'$.stage')>=4 AND content_id IN (\(slots))",[.text(kind)] + values).first?.integer("n") ?? 0
        return (min(done,ids.count),min(stable,ids.count))
    }
}
