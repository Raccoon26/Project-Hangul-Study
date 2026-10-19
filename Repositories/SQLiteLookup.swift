import Foundation

extension SQLiteContentRepository {
    func lookup(_ term: String, offset: Int) async throws -> [LookupEntry] {
        let term = term.precomposedStringWithCanonicalMapping.trimmingCharacters(in:.whitespacesAndNewlines).lowercased()
        guard !term.isEmpty, term.count <= 100, !term.contains("\0") else { return [] }
        // Literal substring matching: %, _ and quotes are data, never LIKE wildcards or SQL.
        let rows = try db.query("""
        WITH terms(id,term) AS (
          SELECT v.id,lower(v.headword) FROM vocabulary v
          UNION ALL SELECT m.vocabulary_id,lower(m.meaning_ja) FROM meanings m JOIN content_items mi ON mi.id=m.id WHERE mi.is_active=1
          UNION ALL SELECT id,lower(pattern) FROM grammar
          UNION ALL SELECT id,lower(meaning_ja) FROM grammar
          UNION ALL SELECT id,lower(explanation_ja) FROM grammar
        ), matches AS (
          SELECT t.id,MIN(CASE WHEN t.term=? THEN 0 WHEN instr(t.term,?)=1 THEN 1 ELSE 2 END) AS rank
          FROM terms t JOIN content_items ci ON ci.id=t.id WHERE ci.is_active=1 AND instr(t.term,?)>0 GROUP BY t.id
        )
        SELECT i.id,i.kind FROM matches m JOIN content_items i ON i.id=m.id LEFT JOIN vocabulary v ON v.id=i.id LEFT JOIN grammar g ON g.id=i.id
        ORDER BY m.rank,COALESCE(v.headword,g.pattern),i.id LIMIT 30 OFFSET ?
        """,[.text(term),.text(term),.text(term),.integer(Int64(max(0,offset)))])
        return try rows.compactMap { row in
            guard let kind = LookupKind(rawValue:try row.text("kind")) else { return nil }
            return try readLookup(LookupReference(contentID:ContentID(rawValue:try row.text("id")),kind:kind))
        }
    }
    func lookupEntry(_ reference: LookupReference) async throws -> LookupEntry? { try readLookup(reference) }
    private func readLookup(_ ref: LookupReference) throws -> LookupEntry? {
        guard let row = try db.query("""
        SELECT i.level,v.headword,v.part_of_speech,g.pattern,g.meaning_ja,
        (SELECT m.meaning_ja FROM meanings m JOIN content_items mi ON mi.id=m.id WHERE m.vocabulary_id=i.id AND mi.is_active=1 ORDER BY m.ordinal,m.id LIMIT 1) AS word_meaning
        FROM content_items i LEFT JOIN vocabulary v ON v.id=i.id LEFT JOIN grammar g ON g.id=i.id
        WHERE i.id=? AND i.kind=? AND i.is_active=1
        """,[.text(ref.contentID.rawValue),.text(ref.kind.rawValue)]).first,
              let level = LearningLevel(rawValue:try row.text("level")) else { return nil }
        let title = row[ref.kind == .vocabulary ? "headword" : "pattern"]?.string
        guard let title = title else { return nil }
        let meaning = row[ref.kind == .vocabulary ? "word_meaning" : "meaning_ja"]?.string ?? "意味の情報を確認できません"
        let posValue = row["part_of_speech"]?.string
        let pos = posValue.flatMap { PartOfSpeech(rawValue:$0) }
        return LookupEntry(reference:ref,title:title,meaning:meaning,subtitle:pos?.japaneseName ?? "文法",level:level)
    }
    func vocabularyDetail(id: ContentID) async throws -> VocabularyDetail {
        let card = try await vocabularyCard(id:id)
        guard let row = try db.query("SELECT headword,part_of_speech,irregular_type,reading FROM vocabulary WHERE id=?",[.text(id.rawValue)]).first else { throw VocabularyStudyError.missingContent }
        var overrides: [String:String] = [:]
        let rubrics = try db.query("SELECT q.rubric_json FROM content_links l JOIN questions q ON q.id=l.source_id JOIN content_items i ON i.id=q.id WHERE l.target_id=? AND l.relation='question_target' AND i.is_active=1 AND json_extract(q.rubric_json,'$.production')=1 ORDER BY q.id",[.text(id.rawValue)])
        struct Rubric: Decodable { let overrides: [String:String] }
        for r in rubrics {
            let values = try JSONDecoder().decode(Rubric.self,from:Data(try r.text("rubric_json").utf8)).overrides
            for (key,value) in values {
                if let old = overrides[key], old != value { throw GrammarError.changedContent }
                overrides[key] = value
            }
        }
        var forms: [DetailConjugation] = []
        for form in [ConjugationForm.present,.past,.future] {
            if let result = try? ConjugationEngine.generate(lemma:row.text("headword"),partOfSpeech:row.text("part_of_speech"),irregular:row["irregular_type"]?.string,form:form,overrides:overrides) {
                forms.append(DetailConjugation(form:form,result:result))
            }
        }
        let irregular = row["irregular_type"]?.string
        return VocabularyDetail(card:card,pronunciation:row["reading"]?.string,conjugations:forms,
            irregular:irregular != nil && irregular != "none",examples:try await examples(for:id))
    }
    func relatedLookup(_ ref: LookupReference) async throws -> [LookupEntry] {
        // Explicit lexical/grammar relations and shared examples; no inferred synonym labels.
        let rows = try db.query("""
        WITH related(id) AS (
          SELECT target_id FROM content_links WHERE source_id=? AND relation IN ('related_word','synonym','antonym','confusable','similar_grammar','contrast_grammar')
          UNION SELECT source_id FROM content_links WHERE target_id=? AND relation IN ('related_word','synonym','antonym','confusable','similar_grammar','contrast_grammar')
          UNION SELECT ge.grammar_id FROM vocabulary_examples ve JOIN meanings m ON m.id=ve.meaning_id JOIN grammar_examples ge ON ge.example_id=ve.example_id WHERE m.vocabulary_id=?
          UNION SELECT m.vocabulary_id FROM grammar_examples ge JOIN vocabulary_examples ve ON ve.example_id=ge.example_id JOIN meanings m ON m.id=ve.meaning_id WHERE ge.grammar_id=?
        ) SELECT i.id,i.kind FROM related r JOIN content_items i ON i.id=r.id
        WHERE i.is_active=1 AND i.kind IN ('vocabulary','grammar') AND i.id!=? ORDER BY i.kind,i.id LIMIT 20
        """,Array(repeating:.text(ref.contentID.rawValue),count:5))
        return try rows.compactMap { row in
            guard let kind = LookupKind(rawValue:try row.text("kind")) else { return nil }
            return try readLookup(LookupReference(contentID:ContentID(rawValue:try row.text("id")),kind:kind))
        }
    }
}
