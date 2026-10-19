import Foundation

struct GrammarQuestion: Codable, Identifiable, Sendable, Equatable {
    let id: ContentID
    let revision: Int
    let prompt: String
    let korean: String?
    let explanation: String
    let choices: [QuizChoice]
    let correctID: String
    let purpose: String
    func isCorrect(_ id: String) -> Bool { ChoiceJudgement.isCorrect(id, choices: choices, correctID: correctID) }
    func validate() throws {
        guard revision > 0, !prompt.isEmpty, !explanation.isEmpty,
              (2...6).contains(choices.count), Set(choices.map(\.id)).count == choices.count,
              choices.allSatisfy({ !$0.id.isEmpty && !$0.text.isEmpty }),
              choices.contains(where: { $0.id == correctID }),
              ["meaning","context","blank","form","contrast"].contains(purpose) else { throw GrammarError.invalidState }
    }
}
struct GrammarCard: Sendable {
    let id: ContentID
    let revision: Int
    let pattern: String
    let meaning: String
    let explanation: String
    let form: String
    let constraints: String?
    let note: String?
    let examples: [Example]
    let comparisons: [GrammarComparison]
    let questions: [GrammarQuestion]
}
struct GrammarComparison: Identifiable, Sendable {
    let id: ContentID
    let pattern: String
    let meaning: String
    let difference: String
    let example: Example?
}
struct GrammarLesson: Identifiable, Sendable {
    let id: ContentID
    let title: String
    let level: LearningLevel
    let order: Int
    let count: Int
}
struct GrammarLessonStatus: Sendable {
    let lessonID: ContentID
    let completed: Int
    let active: Bool
}
struct GrammarSession: Codable, Equatable, Sendable {
    let id: UUID
    let lessonID: ContentID
    let ids: [ContentID]
    let contentVersion: Int
    let seed: UInt64
    let startedAt: Date
    var updatedAt: Date
    var revision = 0
    var round = 1
    var order: [ContentID]
    var position = 0
    var deferred: [ContentID] = []
    var repeated: [ContentID] = []
    var page = 0 // 0 meaning, 1 form, 2 examples/comparison, 3 questions, 4 recall decision
    var questions: [GrammarQuestion] = [] // bounded current-item snapshot for safe resume
    var questionIndex = 0
    var selected: String?
    var correctCount = 0
    var wrongCount = 0
    var exposures = 0
    var exposed = false
    var completedAt: Date?
    var currentID: ContentID? { position < order.count ? order[position] : nil }
    var completed: Bool { completedAt != nil }
    var nextRound: Bool { !completed && currentID == nil }
    var question: GrammarQuestion? { questions.indices.contains(questionIndex) ? questions[questionIndex] : nil }
    func validate() throws {
        for question in questions { try question.validate() }
        let all = Set(ids)
        guard !ids.isEmpty, ids.count <= 20, all.count == ids.count,
              !order.isEmpty, Set(order).count == order.count, Set(order).isSubset(of: all),
              (0...order.count).contains(position), (0...4).contains(page), round > 0, revision >= 0, contentVersion > 0,
              Set(deferred).count == deferred.count, Set(deferred).isSubset(of: Set(order.prefix(position))),
              Set(repeated).isSubset(of: all), correctCount >= 0, wrongCount >= 0, exposures >= 0,
              !completed || (currentID == nil && deferred.isEmpty),
              completed || currentID != nil || !deferred.isEmpty,
              questions.count <= 20, Set(questions.map(\.id)).count == questions.count,
              questionIndex >= 0, questionIndex <= questions.count,
              !exposed || !questions.isEmpty,
              page == 0 || exposed,
              page != 3 || question != nil,
              page != 4 || questionIndex == questions.count,
              currentID != nil || (!exposed && page == 0 && questions.isEmpty),
              selected == nil || question?.choices.contains(where: { $0.id == selected }) == true else { throw GrammarError.invalidState }
    }
}
enum GrammarAction: Sendable {
    case expose([GrammarQuestion])
    case next
    case answer(String)
    case decide(Bool)
    case nextRound
}
enum GrammarError: LocalizedError {
    case invalidState, changedContent
    var errorDescription: String? {
        switch self {
        case .invalidState: return "文法の学習記録を確認できません。記録を読み直してください。"
        case .changedContent: return "この教材を確認できません。記録は保存されています。教材の更新をお待ちください。"
        }
    }
}
struct GrammarReviewQuestion: Sendable {
    let question: GrammarQuestion
    let selected: String?
}
