import Foundation

enum StudyOutcome: String, Codable, Sendable { case correct, incorrect, viewed, skipped }
struct StudyEvent: Sendable {
    let id: UUID
    let contentID: ContentID
    let contentRevision: Int
    let contentVersion: Int
    let occurredAt: Date
    let timeZoneID: String
    let skill: String
    let outcome: StudyOutcome
    let durationMilliseconds: Int
    let sessionID: UUID?
}
struct LearningSummary: Sendable {
    let studyCount: Int
    let correctCount: Int
    let incorrectCount: Int
    let favoriteCount: Int
    let dueCount: Int
    static let empty = LearningSummary(studyCount: 0, correctCount: 0, incorrectCount: 0, favoriteCount: 0, dueCount: 0)
}
