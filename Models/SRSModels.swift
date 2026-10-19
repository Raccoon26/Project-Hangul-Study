import Foundation

enum ReviewRating: String, Codable, CaseIterable, Sendable {
    case difficult, unsure, remembered
    var title: String {
        switch self { case .difficult: return "難しい"; case .unsure: return "もう少し"; case .remembered: return "覚えた" }
    }
    var hint: String {
        switch self {
        case .difficult: return "ほとんど思い出せませんでした。明日また確認します"
        case .unsure: return "思い出せましたが、まだ不確かです。短めの間隔で確認します"
        case .remembered: return "確かに思い出せました。次の復習までの間隔を延ばします"
        }
    }
}
/// Generic scheduling state; the current UI exposes vocabulary only.
struct SRSState: Codable, Equatable, Sendable {
    var stage: Int
    var nextReviewAt: Date
    var lastReviewedAt: Date?
    var reviewCount: Int
    var consecutiveSuccesses: Int
    var failureCount: Int
    var lastResult: ReviewRating?
    let firstLearnedAt: Date
    var difficulty: Double?
    let neededRepetition: Bool
    var schedulingTimeZone: String
    func validate() throws {
        guard StepReviewScheduler.days.indices.contains(stage), reviewCount >= 0,
              consecutiveSuccesses >= 0, consecutiveSuccesses <= reviewCount,
              failureCount >= 0, failureCount <= reviewCount,
              TimeZone(identifier: schedulingTimeZone) != nil,
              nextReviewAt.timeIntervalSince1970.isFinite,
              firstLearnedAt.timeIntervalSince1970.isFinite,
              (difficulty.map({ $0.isFinite && (0...1).contains($0) }) ?? true),
              (lastReviewedAt.map({ $0.timeIntervalSince1970.isFinite }) ?? true),
              (reviewCount == 0 ? (lastResult == nil && lastReviewedAt == nil) : (lastResult != nil && lastReviewedAt != nil)) else { throw ReviewError.invalidState }
    }
}
struct ReviewSession: Identifiable, Sendable {
    let id: UUID
    let skill: String
    var isPractice: Bool = false
    let ids: [ContentID]
    let completedCount: Int
    let currentID: ContentID?
    let exposed: Bool
    let revealed: Bool
    let completed: Bool
}
struct ReviewSummary: Sendable {
    let due: Int
    let overdue: Int
    let completedToday: Int
    let hasActiveSession: Bool
    static let empty = ReviewSummary(due: 0, overdue: 0, completedToday: 0, hasActiveSession: false)
}
enum ReviewError: Error, LocalizedError, Equatable {
    case invalidState, staleCard, nothingDue
    var errorDescription: String? {
        switch self {
        case .invalidState: return "復習記録を確認できません。記録は削除せずに保存されています。"
        case .staleCard: return "復習記録が更新されています。読み直して続けてください。"
        case .nothingDue: return "今のところ、復習する単語はありません。"
        }
    }
}
