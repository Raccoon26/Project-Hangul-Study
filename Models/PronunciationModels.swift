import Foundation

struct PronunciationExample: Identifiable, Sendable {
    let id: ContentID
    let spelling: String
    let reading: String
    let meaning: String
}
struct PronunciationContent: Sendable {
    let id: ContentID
    let title: String
    let ruleType: String
    let spelling: String
    let readings: [String]
    let explanation: String
    let context: String
    let showComposition: Bool
    let examples: [PronunciationExample]
}
