import Foundation

struct CurriculumProfile: Codable, Sendable {
    var version = 1
    var level: LearningLevel
    var skippedHangul: Bool
}
struct CurriculumRoute: Identifiable, Sendable {
    let kind: String
    let target: String
    let level: LearningLevel?
    var id: String { kind + ":" + target }
    var title: String {
        switch kind {
        case "vocabulary": return "単語の続き"
        case "grammar": return "文法の続き"
        case "production": return "活用・入力の続き"
        case "listening": return "リスニングの続き"
        case "lesson": return "文字・発音の続き"
        case "practice": return "自主練習の続き"
        default: return "復習の続き"
        }
    }
}
struct CurriculumCount: Identifiable, Sendable {
    let kind: String
    var total = 0
    var completed = 0
    var stable = 0
    var id: String { kind }
    var title: String { ["vocabulary":"単語","grammar":"文法","listening":"リスニング","lesson":"文字・発音"][kind] ?? kind }
}
struct DiagnosticItem: Codable, Identifiable, Sendable {
    let id: ContentID
    let area: String
    let prompt: String
    let korean: String?
    var choices: [QuizChoice]
    let correct: String?
    let accepted: [String]
    let audio: LearningAudio?
    func judge(_ value: String) -> Bool {
        choices.isEmpty ? ProductionAnswer.judge(value,accepted:accepted,spacingWarning:false) == .correct : ChoiceJudgement.isCorrect(value,choices:choices,correctID:correct)
    }
}
struct DiagnosticSession: Codable, Sendable {
    var version = 1
    let id: UUID
    let contentVersion: Int
    var items: [DiagnosticItem]
    var results: [Bool?] = []
    var revision = 0
    var ended = false
    var current: DiagnosticItem? { !ended && items.indices.contains(results.count) ? items[results.count] : nil }
    var recommendation: LearningLevel {
        let assessed = zip(items,results).filter { $0.1 != nil }
        let reading = assessed.filter { $0.0.area == "hangul" }
        if !reading.isEmpty && reading.allSatisfy({ $0.1 == false }) { return .hangul }
        let core = assessed.filter { $0.0.area != "hangul" }
        return core.count >= 4 && core.filter({ $0.1 == true }).count * 4 >= core.count * 3 ? .beginner : .intro
    }
    func validate() throws {
        guard version == 1, contentVersion > 0, !items.isEmpty, items.count <= 10,
              Set(items.map(\.id)).count == items.count, results.count <= items.count,
              revision == results.count, ended || results.count < items.count else { throw GrammarError.invalidState }
        for item in items {
            guard !item.prompt.isEmpty else { throw GrammarError.invalidState }
            if item.choices.isEmpty {
                guard !item.accepted.isEmpty, item.accepted.allSatisfy({ !ProductionAnswer.normalize($0).isEmpty }) else { throw GrammarError.invalidState }
            } else {
                guard item.choices.count >= 2, Set(item.choices.map(\.id)).count == item.choices.count,
                      item.choices.contains(where: { $0.id == item.correct }) else { throw GrammarError.invalidState }
            }
        }
    }
    mutating func answer(_ value: String?, expectedRevision: Int) throws {
        try validate()
        guard expectedRevision == revision, let item = current else { throw VocabularyStudyError.staleState }
        if let value = value {
            guard value.count <= 500, !ProductionAnswer.normalize(value).isEmpty else { throw GrammarError.invalidState }
            results.append(item.judge(value))
        } else { results.append(nil) }
        revision += 1
        let reading = zip(items,results).filter { $0.0.area == "hangul" }
        // Two failed reading checks end early; unassessed audio is never a failure.
        ended = results.count == items.count || (reading.count == 2 && reading.allSatisfy { $0.1 == false })
        try validate()
    }
}
