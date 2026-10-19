import Foundation

/// Legacy DEV-01 adapter contract retained for compatibility.
/// DEV-06 uses StepReviewScheduler with ReviewRating; self-assessment must not
/// be flattened into quiz correct/incorrect StudyOutcome.
struct ReviewState: Codable, Sendable {
    let algorithm: String
    let version: Int
    let payloadJSON: String
    let dueAt: Date?
}
protocol ReviewScheduling: Sendable {
    func nextState(previous: ReviewState?, outcome: StudyOutcome, at date: Date) throws -> ReviewState
}
