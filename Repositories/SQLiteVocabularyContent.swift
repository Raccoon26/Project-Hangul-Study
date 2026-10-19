import Foundation

extension SQLiteContentRepository {
    func vocabularyCount(level: LearningLevel) async throws -> Int {
        try db.query("SELECT COUNT(*) AS count FROM vocabulary v JOIN content_items i ON i.id=v.id WHERE i.is_active=1 AND i.level=?", [.text(level.rawValue)]).first?.integer("count") ?? 0
    }
    func vocabularyCard(id: ContentID) async throws -> VocabularyCard {
        try readVocabularyCard(id: id)
    }
    // Shared by dictionary/rounds and authored vocabulary lessons. No copied text.
    func readVocabularyCard(id: ContentID) throws -> VocabularyCard {
        guard let row = try db.query("SELECT v.headword,v.part_of_speech,i.revision FROM vocabulary v JOIN content_items i ON i.id=v.id WHERE v.id=? AND i.is_active=1", [.text(id.rawValue)]).first,
              let pos = PartOfSpeech(rawValue: try row.text("part_of_speech")) else { throw VocabularyStudyError.missingContent }
        let meanings = try db.query("SELECT m.* FROM meanings m JOIN content_items i ON i.id=m.id WHERE m.vocabulary_id=? AND i.is_active=1 ORDER BY m.ordinal,m.id LIMIT 10", [.text(id.rawValue)]).map { meaning -> VocabularyMeaning in
            let meaningID = try meaning.text("id")
            let example = try db.query("SELECT e.id,e.korean,e.japanese FROM examples e JOIN vocabulary_examples ve ON ve.example_id=e.id JOIN content_items i ON i.id=e.id WHERE ve.meaning_id=? AND i.is_active=1 ORDER BY e.id LIMIT 1", [.text(meaningID)]).first.map {
                Example(id: ContentID(rawValue: try $0.text("id")), korean: try $0.text("korean"), japanese: try $0.text("japanese"))
            }
            let exampleAudio = try example.map { try vocabularyAudio(id: $0.id, text: $0.korean) }
            return VocabularyMeaning(id: ContentID(rawValue: meaningID), text: try meaning.text("meaning_ja"),
                usage: meaning["usage_ja"]?.string, nuance: meaning["nuance_ja"]?.string, example: example, exampleAudio: exampleAudio)
        }
        guard !meanings.isEmpty else { throw VocabularyStudyError.missingContent }
        let notes = try db.query("SELECT n.id,n.title_ja,n.explanation_ja FROM learner_notes n JOIN content_links l ON l.target_id=n.id JOIN content_items i ON i.id=n.id WHERE l.source_id=? AND l.relation='learner_note' AND i.is_active=1 ORDER BY n.id LIMIT 10", [.text(id.rawValue)]).map {
            VocabularyNote(id: ContentID(rawValue: try $0.text("id")), title: try $0.text("title_ja"), text: try $0.text("explanation_ja"))
        }
        let headword = try row.text("headword")
        return VocabularyCard(id: id, revision: try row.integer("revision"), headword: headword,
                              audio: try vocabularyAudio(id: id, text: headword),
                              partOfSpeech: pos.japaneseName, meanings: meanings, notes: notes)
    }
    private func vocabularyAudio(id: ContentID, text: String) throws -> LearningAudio {
        // Respect authored recorded-required/tts policy whenever present; otherwise
        // real lexical entries and sentences use the shared runtime TTS safety policy.
        if let authored = try readAudio(id) { return authored }
        return LearningAudio(source: .systemTTS, usage: .wordSentence, text: text, asset: nil)
    }
}
