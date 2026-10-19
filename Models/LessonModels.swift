import Foundation

struct QuizChoice: Identifiable, Equatable, Codable, Sendable {
    let id: String
    let text: String
}
struct LessonStep: Identifiable, Sendable {
    enum Kind: Equatable, Sendable { case character, explanation, pronunciation, quiz }
    let id: ContentID
    let revision: Int
    let kind: Kind
    let symbol: String
    let title: String
    let category: String
    let explanation: String
    let choices: [QuizChoice]
    let correctChoiceID: String?
    var pronunciation: PronunciationContent? = nil
    var audio: LearningAudio? = nil
    var requiresListening: Bool = false
    var skill: String = "hangul"
    func isCorrect(_ choiceID: String) -> Bool {
        ChoiceJudgement.isCorrect(choiceID, choices: choices, correctID: correctChoiceID)
    }
}
struct LessonSession: Sendable {
    let id: UUID
    let lessonID: ContentID
    let contentVersion: Int
    let seed: UInt64
    let stepIDs: [ContentID]
    let currentID: ContentID
    let completed: Bool
}
struct LessonStepResult: Sendable {
    let contentID: ContentID
    let outcome: StudyOutcome
    let selectedChoiceID: String?
}
struct LessonProgress: Sendable {
    let lessonID: ContentID
    let completedCount: Int
    let hasActiveSession: Bool
}
enum LessonError: Equatable, LocalizedError {
    case contentChanged, invalidSession
    var errorDescription: String? {
        switch self {
        case .contentChanged: return "教材が更新されています。これまでの記録を残して、このレッスンを最初から始めてください。"
        case .invalidSession: return "学習位置を確認できませんでした。レッスンを開き直してください。"
        }
    }
}
