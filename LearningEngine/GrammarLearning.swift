import Foundation

/// Shared single-choice judgement, also used by the existing lesson quizzes.
enum ChoiceJudgement {
    static func isCorrect(_ id: String, choices: [QuizChoice], correctID: String?) -> Bool {
        choices.contains { $0.id == id } && correctID == id
    }
}
/// Both pass engines use the existing seeded quiz shuffle, without casting their state models.
enum RecallOrder {
    static func next(_ ids: [ContentID], previous: [ContentID], seed: UInt64, scope: ContentID) -> [ContentID] {
        var result = QuizOptions.ordered(ids.map { QuizChoice(id: $0.rawValue, text: "") }, seed: seed, contentID: scope)
            .map { ContentID(rawValue: $0.id) }
        if result.count > 1 && result.first == previous.last { result.append(result.removeFirst()) }
        if result.count > 2 && result == previous { result.swapAt(1, 2) }
        return result
    }
}
enum GrammarLearning {
    static func apply(_ action: GrammarAction, to original: GrammarSession, now: Date = Date()) throws -> GrammarSession {
        try original.validate()
        guard !original.completed else { throw GrammarError.invalidState }
        var s = original
        switch action {
        case .expose(let questions):
            guard s.currentID != nil, !questions.isEmpty, questions.count <= 20 else { throw GrammarError.invalidState }
            if s.exposed { return s }
            s.questions = questions; s.exposed = true; s.exposures += 1
        case .next:
            guard s.exposed else { throw GrammarError.invalidState }
            if s.page < 3 { s.page += 1 }
            else if s.page == 3, s.selected != nil {
                s.questionIndex += 1; s.selected = nil
                if s.questionIndex == s.questions.count { s.page = 4 }
            } else { throw GrammarError.invalidState }
        case .answer(let id):
            guard s.page == 3, s.selected == nil, let q = s.question,
                  q.choices.contains(where: { $0.id == id }) else { throw GrammarError.invalidState }
            s.selected = id
            if q.isCorrect(id) { s.correctCount += 1 } else { s.wrongCount += 1 }
        case .decide(let known):
            guard s.page == 4, let id = s.currentID else { throw GrammarError.invalidState }
            if !known {
                s.deferred.append(id)
                if !s.repeated.contains(id) { s.repeated.append(id) }
            }
            s.position += 1; s.page = 0; s.questions = []; s.questionIndex = 0; s.selected = nil; s.exposed = false
            if s.position == s.order.count && s.deferred.isEmpty { s.completedAt = now }
        case .nextRound:
            guard s.nextRound else { throw GrammarError.invalidState }
            s.round += 1
            s.order = RecallOrder.next(s.deferred, previous: s.order, seed: s.seed &+ UInt64(s.round), scope: s.lessonID)
            s.deferred = []; s.position = 0
        }
        s.updatedAt = now; s.revision += 1
        try s.validate()
        return s
    }
}
