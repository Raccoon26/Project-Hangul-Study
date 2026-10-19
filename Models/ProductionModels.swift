import Foundation
struct ProductionQuestion: Codable, Identifiable, Sendable {
    let id: ContentID
    let revision: Int
    let vocabularyID: ContentID
    let vocabularyRevision: Int
    let grammarID: ContentID?
    let lemma: String
    let meaning: String
    let prompt: String
    let korean: String?
    let explanation: String
    let accepted: [String]
    let form: ConjugationForm
    let generated: String
    let spacingWarning: Bool
}
struct ProductionSession: Codable, Sendable {
    let id: UUID
    let scope: ContentID
    let questions: [ProductionQuestion]
    let contentVersion: Int
    var updatedAt: Date? = nil // Optional preserves decoding of DEV08–12 snapshots.
    var position = 0
    var retry: [Int] = []
    var retrying = false
    var result: InputJudgement?
    var answer: String?
    var revision = 0
    var studying = true
    var current: ProductionQuestion? { questions.indices.contains(position) ? questions[position] : nil }
    var completed: Bool { current == nil }
    func validate() throws {
        guard !questions.isEmpty, questions.count <= 20, (0...questions.count).contains(position), revision >= 0, contentVersion > 0,
              Set(retry).count == retry.count,
              result == nil || (!studying && current != nil),
              !completed || (retry.isEmpty && result == nil),
              Set(questions.map(\.id)).count == questions.count,
              questions.allSatisfy({ $0.vocabularyID == scope && !$0.accepted.isEmpty && $0.accepted.allSatisfy({ !ProductionAnswer.normalize($0).isEmpty }) }),
              retry.allSatisfy({ questions.indices.contains($0) }),
              (result == nil) == (answer == nil) else { throw GrammarError.invalidState }
    }
}
