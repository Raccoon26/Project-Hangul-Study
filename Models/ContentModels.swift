import Foundation

/// Permanent UUID from authored content, never a row offset or a hash of Korean text.
struct ContentID: RawRepresentable, Hashable, Codable, Sendable {
    let rawValue: String
}
struct ContentMetadata: Sendable {
    let datasetID: String
    let contentVersion: Int
    let isFixture: Bool
}
struct Vocabulary: Identifiable, Hashable, Sendable {
    let id: ContentID
    let headword: String
    let meaning: String
    let partOfSpeech: String
    let sortKey: String
    let level: LearningLevel
    let difficulty: Int?
    let pronunciation: String?
    let hasBatchim: Bool?
    let irregularType: String?
    let learningPriority: Int?
    let topikLevel: Int?
}
struct VocabularyCursor: Sendable {
    let sortKey: String
    let id: ContentID
}
struct Example: Identifiable, Sendable {
    let id: ContentID
    let korean: String
    let japanese: String
    var learningPoint: String? = nil
}
struct Course: Identifiable, Sendable {
    let id: ContentID
    let title: String
    let description: String
    let lessons: [Lesson]
}
struct Lesson: Identifiable, Sendable {
    let id: ContentID
    let title: String
    let itemCount: Int
}
