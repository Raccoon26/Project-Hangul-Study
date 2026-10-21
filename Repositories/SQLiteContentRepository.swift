import Foundation

actor SQLiteContentRepository: ContentRepository {
    let db: SQLiteConnection
    private let schemaVersion: Int
    private let info: ContentMetadata
    init(url: URL, allowFixture: Bool) throws {
        let connection = try SQLiteConnection(url: url, readOnly: true)
        info = try ContentPackageValidator.validate(connection, allowFixture: allowFixture)
        schemaVersion = try connection.query("PRAGMA user_version").first?.integer("user_version") ?? 0
        db = connection
    }
    func metadata() async throws -> ContentMetadata { info }
    func vocabulary(after cursor: VocabularyCursor?, limit: Int) async throws -> [Vocabulary] {
        try await vocabulary(matching: VocabularyQuery(), after: cursor, limit: limit)
    }
    func vocabulary(matching query: VocabularyQuery, after cursor: VocabularyCursor?, limit: Int) async throws -> [Vocabulary] {
        let pageSize = min(max(limit, 1), 100)
        var sql = """
        SELECT v.id,v.headword,v.part_of_speech,v.sort_key,
        COALESCE((SELECT m.meaning_ja FROM meanings m JOIN content_items mi ON mi.id=m.id
        WHERE m.vocabulary_id=v.id AND mi.is_active=1 ORDER BY m.ordinal LIMIT 1),'') AS meaning, i.level,i.difficulty,v.reading,v.has_batchim,v.irregular_type,v.learning_priority,v.topik_level
        FROM vocabulary v JOIN content_items i ON i.id=v.id WHERE i.is_active=1
        """
        var values: [SQLValue] = []
        if let level = query.level {
            sql += " AND i.level=?"
            values.append(.text(level.rawValue))
        }
        if let rawPrefix = query.prefix {
            let prefix = rawPrefix.precomposedStringWithCanonicalMapping
                .trimmingCharacters(in: .whitespacesAndNewlines).lowercased()
            if !prefix.isEmpty {
                sql += " AND v.id IN (SELECT vocabulary_id FROM vocabulary_search WHERE term>=? AND term<?)"
                values.append(.text(prefix))
                values.append(.text(prefix + "\u{10FFFF}"))
            }
        }
        if let cursor = cursor {
            sql += " AND (v.sort_key>? OR (v.sort_key=? AND v.id>?))"
            values.append(contentsOf: [.text(cursor.sortKey), .text(cursor.sortKey), .text(cursor.id.rawValue)])
        }
        sql += " ORDER BY v.sort_key,v.id LIMIT ?"
        values.append(.integer(Int64(pageSize)))
        return try db.query(sql, values).map { row in
            guard let level = LearningLevel(rawValue: try row.text("level")),
                  let pos = PartOfSpeech(rawValue: try row.text("part_of_speech")) else {
                throw DatabaseError.invalidData("Unknown content taxonomy")
            }
            return Vocabulary(id: ContentID(rawValue: try row.text("id")), headword: try row.text("headword"),
                       meaning: try row.text("meaning"), partOfSpeech: pos.japaneseName, sortKey: try row.text("sort_key"), level: level,
                       difficulty: row["difficulty"]?.int, pronunciation: row["reading"]?.string,
                       hasBatchim: (row["has_batchim"]?.int).map { $0 == 1 }, irregularType: row["irregular_type"]?.string,
                       learningPriority: row["learning_priority"]?.int, topikLevel: row["topik_level"]?.int)
        }
    }
    func examples(for id: ContentID) async throws -> [Example] {
        try db.query("""
        SELECT DISTINCT e.id,e.korean,e.japanese FROM examples e
        JOIN vocabulary_examples ve ON ve.example_id=e.id JOIN meanings m ON m.id=ve.meaning_id
        JOIN content_items i ON i.id=e.id JOIN content_items mi ON mi.id=m.id
        WHERE m.vocabulary_id=? AND i.is_active=1 AND mi.is_active=1 ORDER BY e.id LIMIT 100
        """, [.text(id.rawValue)]).map {
            Example(id: ContentID(rawValue: try $0.text("id")), korean: try $0.text("korean"), japanese: try $0.text("japanese"))
        }
    }
    func courses() async throws -> [Course] {
        try db.query("SELECT c.* FROM courses c JOIN content_items i ON i.id=c.id WHERE i.is_active=1 AND NOT EXISTS(SELECT 1 FROM lessons l JOIN lesson_items li ON li.lesson_id=l.id JOIN content_items typed ON typed.id=li.content_id WHERE l.course_id=c.id AND typed.kind IN ('grammar','listening')) ORDER BY c.ordinal,c.id").map { row in
            let courseID = try row.text("id")
            let lessons = try db.query("""
            SELECT l.id,l.title_ja,(SELECT COUNT(*) FROM lesson_items li JOIN content_items ci ON ci.id=li.content_id
            WHERE li.lesson_id=l.id AND ci.is_active=1) AS item_count FROM lessons l
            JOIN content_items i ON i.id=l.id WHERE l.course_id=? AND i.is_active=1 ORDER BY l.ordinal,l.id
            """, [.text(courseID)]).map {
                Lesson(id: ContentID(rawValue: try $0.text("id")), title: try $0.text("title_ja"), itemCount: try $0.integer("item_count"))
            }
            return Course(id: ContentID(rawValue: courseID), title: try row.text("title_ja"), description: try row.text("description_ja"), lessons: lessons)
        }
    }
    func lessonSteps(for lessonID: ContentID) async throws -> [LessonStep] {
        let rows = try db.query("""
        SELECT i.id,i.kind,i.revision,h.symbol,h.name_ko,h.category,h.explanation_ja AS character_explanation,
        n.title_ja,n.explanation_ja AS note_explanation,q.question_type,q.prompt_ko,q.prompt_ja,
        q.explanation_ja AS answer_explanation,q.answer_json
        FROM lesson_items li JOIN content_items i ON i.id=li.content_id
        LEFT JOIN hangul h ON h.id=i.id LEFT JOIN learner_notes n ON n.id=i.id LEFT JOIN questions q ON q.id=i.id
        WHERE li.lesson_id=? AND i.is_active=1 ORDER BY li.ordinal LIMIT 201
        """, [.text(lessonID.rawValue)])
        guard !rows.isEmpty, rows.count <= 200 else { throw DatabaseError.invalidData("Invalid lesson size") }
        return try rows.map { row in
            let id = ContentID(rawValue: try row.text("id"))
            let revision = try row.integer("revision")
            switch try row.text("kind") {
            case "hangul":
                let category = try row.text("category")
                let label = ["consonant": "子音", "vowel": "母音", "final": "パッチム", "syllable": "文字の組み立て"][category] ?? "ハングル"
                return LessonStep(id: id, revision: revision, kind: .character, symbol: try row.text("symbol"),
                    title: try row.text("name_ko"), category: label, explanation: try row.text("character_explanation"), choices: [], correctChoiceID: nil)
            case "note":
                return LessonStep(id: id, revision: revision, kind: .explanation, symbol: "", title: try row.text("title_ja"),
                    category: "", explanation: try row.text("note_explanation"), choices: [], correctChoiceID: nil)
            case "vocabulary":
                let card = try readVocabularyCard(id: id)
                let meanings = card.meanings.map { meaning in
                    ([meaning.text, meaning.usage, meaning.nuance].compactMap { $0 }
                        + (meaning.example.map { [$0.korean, $0.japanese] } ?? [])).joined(separator: "\n")
                }
                let notes = card.notes.map { $0.title + "\n" + $0.text }
                var step = LessonStep(id: id, revision: revision, kind: .explanation,
                    symbol: card.headword, title: card.partOfSpeech, category: "単語・意味と例文",
                    explanation: (meanings + notes).joined(separator: "\n\n"), choices: [], correctChoiceID: nil)
                step.audio = card.audio
                // Reading a lesson is exposure; rounds and SRS keep their own state.
                step.skill = "vocabulary_preview"
                return step
            case "pronunciation":
                guard let pronunciation = try readPronunciation(id) else { throw DatabaseError.invalidData("Missing pronunciation presentation") }
                var step = LessonStep(id: id, revision: revision, kind: .pronunciation, symbol: pronunciation.spelling,
                    title: pronunciation.title, category: "発音・パッチム", explanation: pronunciation.explanation,
                    choices: [], correctChoiceID: nil)
                step.pronunciation = pronunciation; step.audio = try readAudio(id); step.skill = "pronunciation"
                return step
            case "question":
                guard try row.text("question_type") == "multiple_choice" else { throw DatabaseError.invalidData("Unsupported lesson question") }
                struct Answer: Decodable { let correct_choice_ids: [String] }
                let answer = try JSONDecoder().decode(Answer.self, from: Data(try row.text("answer_json").utf8))
                let choices = try db.query("SELECT choice_id,text FROM question_choices WHERE question_id=? ORDER BY ordinal", [.text(id.rawValue)]).map {
                    QuizChoice(id: try $0.text("choice_id"), text: try $0.text("text"))
                }
                guard answer.correct_choice_ids.count == 1, choices.count >= 2,
                      Set(choices.map(\.id)).count == choices.count,
                      choices.contains(where: { $0.id == answer.correct_choice_ids[0] }) else { throw DatabaseError.invalidData("Invalid single-choice question") }
                var step = LessonStep(id: id, revision: revision, kind: .quiz, symbol: row["prompt_ko"]?.string ?? "",
                    title: try row.text("prompt_ja"), category: "確認", explanation: try row.text("answer_explanation"),
                    choices: choices, correctChoiceID: answer.correct_choice_ids[0])
                if schemaVersion >= 3 {
                    if let audioRow = try db.query("SELECT audio_content_id FROM audio_questions WHERE question_id=?", [.text(id.rawValue)]).first {
                        step.audio = try readAudio(ContentID(rawValue: try audioRow.text("audio_content_id")))
                        guard step.audio != nil else { throw DatabaseError.invalidData("Missing listening audio policy") }
                        step.requiresListening = true
                    }
                    let pronunciationTargets = try db.query("SELECT 1 FROM content_links cl JOIN pronunciation_rules p ON p.id=cl.target_id WHERE cl.source_id=? AND cl.relation='question_target' LIMIT 1", [.text(id.rawValue)])
                    if !pronunciationTargets.isEmpty { step.skill = "pronunciation" }
                }
                return step
            default: throw DatabaseError.invalidData("Unsupported lesson item")
            }
        }
    }

    func pronunciationRule(for id: ContentID) async throws -> PronunciationContent? { try readPronunciation(id) }
    private func readPronunciation(_ id: ContentID) throws -> PronunciationContent? {
        guard schemaVersion >= 3 else { return nil }
        guard let row = try db.query("""
        SELECT r.id,r.title_ja,r.rule_type,r.explanation_ja,p.spelling_ko,p.readings_json,p.context_ja,p.show_composition
        FROM pronunciation_rules r JOIN pronunciation_presentations p ON p.rule_id=r.id
        JOIN content_items i ON i.id=r.id WHERE r.id=? AND i.is_active=1
        """, [.text(id.rawValue)]).first else { return nil }
        let readings = try JSONDecoder().decode([String].self, from: Data(try row.text("readings_json").utf8))
        guard !readings.isEmpty, readings.allSatisfy({ !$0.isEmpty }) else { throw DatabaseError.invalidData("Invalid pronunciation readings") }
        let examples = try db.query("""
        SELECT e.id,p.spelling_ko,p.pronunciation_ko,e.japanese FROM pronunciation_examples p
        JOIN examples e ON e.id=p.example_id JOIN content_items i ON i.id=e.id
        WHERE p.rule_id=? AND i.is_active=1 ORDER BY p.spelling_ko,e.id LIMIT 20
        """, [.text(id.rawValue)]).map {
            PronunciationExample(id: ContentID(rawValue: try $0.text("id")), spelling: try $0.text("spelling_ko"),
                reading: try $0.text("pronunciation_ko"), meaning: try $0.text("japanese"))
        }
        return PronunciationContent(id: id, title: try row.text("title_ja"), ruleType: try row.text("rule_type"), spelling: try row.text("spelling_ko"),
            readings: readings, explanation: try row.text("explanation_ja"), context: try row.text("context_ja"),
            showComposition: try row.integer("show_composition") == 1, examples: examples)
    }
    func readAudio(_ id: ContentID) throws -> LearningAudio? {
        guard schemaVersion >= 3 else { return nil }
        guard let row = try db.query("""
        SELECT a.mode,a.usage,a.tts_text,m.relative_path,m.sha256 FROM content_audio a
        LEFT JOIN media_assets m ON m.id=a.asset_id WHERE a.content_id=?
        """, [.text(id.rawValue)]).first else { return nil }
        guard let usage = LearningAudio.Usage(rawValue: try row.text("usage")) else { throw DatabaseError.invalidData("Invalid audio usage") }
        let asset: RecordingAsset?
        if let path = row["relative_path"]?.string, let hash = row["sha256"]?.string {
            asset = RecordingAsset(relativePath: path, sha256: hash)
        } else { asset = nil }
        let mode = try row.text("mode")
        guard ["tts", "recorded_required"].contains(mode) else { throw DatabaseError.invalidData("Invalid audio source") }
        let audio = LearningAudio(source: mode == "tts" ? .systemTTS : .verifiedRecording, usage: usage,
            text: row["tts_text"]?.string, asset: asset)
        if audio.source == .systemTTS && !AudioPolicy.permitsTTS(audio) { throw DatabaseError.invalidData("Unsafe TTS content") }
        return audio
    }

}
