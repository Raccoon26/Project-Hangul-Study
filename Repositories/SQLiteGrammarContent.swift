import Foundation

extension SQLiteContentRepository {
    func grammarLessons(level: LearningLevel, after: Int, limit: Int) async throws -> [GrammarLesson] {
        try db.query("""
        SELECT l.id,l.title_ja,l.ordinal,COUNT(*) AS n,c.title_ja AS course_title,
        (SELECT t.label_ja FROM item_tags it JOIN tags t ON t.id=it.tag_id
         JOIN content_items ti ON ti.id=t.id WHERE it.content_id=l.id
         AND t.namespace='data09_unit' AND ti.is_active=1 ORDER BY t.id LIMIT 1) AS unit_title
        FROM lessons l JOIN courses c ON c.id=l.course_id JOIN content_items co ON co.id=c.id
        JOIN content_items ci ON ci.id=l.id JOIN lesson_items li ON li.lesson_id=l.id
        JOIN grammar g ON g.id=li.content_id JOIN content_items gi ON gi.id=g.id
        WHERE ci.level=? AND ci.is_active=1 AND gi.is_active=1 AND co.is_active=1 AND l.ordinal>?
        GROUP BY l.id ORDER BY l.ordinal,l.id LIMIT ?
        """, [.text(level.rawValue), .integer(Int64(after)), .integer(Int64(min(max(limit,1),30)))]).map {
            GrammarLesson(id: ContentID(rawValue: try $0.text("id")), title: try $0.text("title_ja"), level: level,
                order: try $0.integer("ordinal"), count: try $0.integer("n"), courseTitle: $0["course_title"]?.string, unitTitle: $0["unit_title"]?.string)
        }
    }
    func grammarIDs(lesson: ContentID) async throws -> [ContentID] {
        let rows = try db.query("SELECT g.id FROM lesson_items li JOIN grammar g ON g.id=li.content_id JOIN content_items i ON i.id=g.id WHERE li.lesson_id=? AND i.is_active=1 ORDER BY li.ordinal LIMIT 21", [.text(lesson.rawValue)])
        guard !rows.isEmpty, rows.count <= 20 else { throw GrammarError.changedContent }
        return try rows.map { ContentID(rawValue: try $0.text("id")) }
    }
    func grammarSearch(level: LearningLevel, prefix: String, after: String, limit: Int) async throws -> [ContentID] {
        // Bounded keyset query; at 500 grammar entries the indexed level/ID filter bounds the scan.
        let term = prefix.precomposedStringWithCanonicalMapping.trimmingCharacters(in: .whitespacesAndNewlines)
        return try db.query("""
        SELECT g.id FROM grammar g JOIN content_items i ON i.id=g.id
        WHERE i.is_active=1 AND i.level=? AND g.id>? AND
        (?='' OR instr(g.pattern,?)>0 OR instr(g.meaning_ja,?)>0)
        ORDER BY g.id LIMIT ?
        """, [.text(level.rawValue), .text(after), .text(term), .text(term), .text(term), .integer(Int64(min(max(limit,1),50)))]).map { ContentID(rawValue: try $0.text("id")) }
    }
    func grammarCard(id: ContentID) async throws -> GrammarCard {
        guard let row = try db.query("SELECT g.*,i.revision FROM grammar g JOIN content_items i ON i.id=g.id WHERE g.id=? AND i.is_active=1", [.text(id.rawValue)]).first else { throw GrammarError.changedContent }
        let examples = try grammarExamples(id)
        let comparisons = try db.query("""
        SELECT g.id,g.pattern,g.meaning_ja,g.confusion_ja,g.explanation_ja FROM content_links l
        JOIN grammar g ON g.id=l.target_id JOIN content_items i ON i.id=g.id
        WHERE l.source_id=? AND l.relation IN ('similar_grammar','contrast_grammar') AND i.is_active=1 ORDER BY g.id LIMIT 6
        """, [.text(id.rawValue)]).map { r in
            GrammarComparison(id: ContentID(rawValue: try r.text("id")), pattern: try r.text("pattern"),
                meaning: r["meaning_ja"]?.string ?? "", difference: try (r["confusion_ja"]?.string ?? r.text("explanation_ja")),
                example: try grammarExamples(ContentID(rawValue: try r.text("id"))).first)
        }
        let questions = try db.query("""
        SELECT q.*,i.revision FROM content_links l JOIN questions q ON q.id=l.source_id
        JOIN content_items i ON i.id=q.id WHERE l.target_id=? AND l.relation='question_target'
        AND i.is_active=1 ORDER BY q.id LIMIT 21
        """, [.text(id.rawValue)]).map { r -> GrammarQuestion in
            struct Answer: Decodable { let correct_choice_ids: [String] }
            struct Rubric: Decodable { let grammar_task: String }
            let answer = try JSONDecoder().decode(Answer.self, from: Data(try r.text("answer_json").utf8))
            let rubric = try JSONDecoder().decode(Rubric.self, from: Data(try r.text("rubric_json").utf8))
            let qid = try r.text("id")
            let choices = try db.query("SELECT choice_id,text FROM question_choices WHERE question_id=? ORDER BY ordinal LIMIT 7", [.text(qid)]).map { QuizChoice(id: try $0.text("choice_id"), text: try $0.text("text")) }
            guard try r.text("question_type") == "multiple_choice", answer.correct_choice_ids.count == 1,
                  choices.count >= 2, choices.count <= 6, choices.contains(where: { $0.id == answer.correct_choice_ids[0] }) else { throw GrammarError.changedContent }
            return GrammarQuestion(id: ContentID(rawValue: qid), revision: try r.integer("revision"), prompt: try r.text("prompt_ja"),
                korean: r["prompt_ko"]?.string, explanation: try r.text("explanation_ja"), choices: choices,
                correctID: answer.correct_choice_ids[0], purpose: rubric.grammar_task)
        }
        let prerequisiteRows = try db.query("""
        SELECT g.id,g.pattern,g.meaning_ja,g.form_ko,g.explanation_ja FROM content_links l
        JOIN grammar g ON g.id=l.target_id JOIN content_items i ON i.id=g.id
        WHERE l.source_id=? AND l.relation='prerequisite' AND i.is_active=1
        ORDER BY g.id LIMIT 9
        """, [.text(id.rawValue)])
        guard prerequisiteRows.count <= 8 else { throw GrammarError.changedContent }
        let prerequisites = try prerequisiteRows.map { r in
            GrammarPrerequisite(id:ContentID(rawValue:try r.text("id")),pattern:try r.text("pattern"),
                meaning:try r.text("meaning_ja"),form:try r.text("form_ko"),explanation:try r.text("explanation_ja"))
        }
        let related = try await relatedLookup(LookupReference(contentID:id,kind:.grammar))
        let relatedWords = related.filter { $0.reference.kind == .vocabulary }
        guard !examples.isEmpty, !questions.isEmpty, questions.count <= 20 else { throw GrammarError.changedContent }
        return GrammarCard(id: id, revision: try row.integer("revision"), pattern: try row.text("pattern"),
            meaning: try row.text("meaning_ja"), explanation: try row.text("explanation_ja"), form: try row.text("form_ko"),
            constraints: row["usage_constraints_ja"]?.string, note: row["confusion_ja"]?.string,
            examples: examples, comparisons: comparisons, questions: questions, prerequisites: prerequisites, relatedWords: relatedWords)
    }
    private func grammarExamples(_ id: ContentID) throws -> [Example] {
        try db.query("""
        SELECT e.id,e.korean,e.japanese,e.learning_point_ja FROM grammar_examples ge JOIN examples e ON e.id=ge.example_id
        JOIN content_items i ON i.id=e.id WHERE ge.grammar_id=? AND i.is_active=1 ORDER BY e.id LIMIT 6
        """, [.text(id.rawValue)]).map { Example(id: ContentID(rawValue: try $0.text("id")), korean: try $0.text("korean"), japanese: try $0.text("japanese"), learningPoint: $0["learning_point_ja"]?.string) }
    }
}
