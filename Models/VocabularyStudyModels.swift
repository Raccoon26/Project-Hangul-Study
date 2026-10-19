import Foundation

struct VocabularyMeaning: Identifiable, Sendable {
    let id: ContentID
    let text: String
    let usage: String?
    let nuance: String?
    let example: Example?
    let exampleAudio: LearningAudio?
}
struct VocabularyNote: Identifiable, Sendable {
    let id: ContentID
    let title: String
    let text: String
}
struct VocabularyCard: Sendable {
    let id: ContentID
    let revision: Int
    let headword: String
    let audio: LearningAudio
    let partOfSpeech: String
    let meanings: [VocabularyMeaning]
    let notes: [VocabularyNote]
}
struct VocabularyStudySet: Identifiable, Sendable {
    let id: UUID
    let level: LearningLevel
    let number: Int
    let vocabularyIDs: [ContentID]
    let completedCount: Int
    let hasActiveSession: Bool
    var title: String { "\(level.japaneseName) \(number)" }
}
enum VocabularyDecision: String, Codable, Sendable { case learn, known }
enum VocabularyAction: Sendable {
    case expose(revision: Int, contentVersion: Int)
    case reveal
    case decide(VocabularyDecision)
    case nextRound
}
enum VocabularyStudyError: Error, LocalizedError, Equatable {
    case invalidState, staleState, missingContent, noNewWords
    var errorDescription: String? {
        switch self {
        case .invalidState: return "学習記録を確認できません。記録は削除せずに保存されています。"
        case .staleState: return "記録が更新されています。読み直してから続けてください。"
        case .missingContent: return "この単語の教材を利用できません。学習記録を保ったまま、教材の更新をお待ちください。"
        case .noNewWords: return "新しいセットはありません。これまでのセットをもう一度学べます。"
        }
    }
}

/// A bounded snapshot of IDs, never a cache of content text. Position indexes this saved order only.
struct VocabularySession: Codable, Equatable, Sendable {
    let id: UUID
    let setID: UUID
    let vocabularyIDs: [ContentID]
    let contentVersionAtStart: Int
    let seed: UInt64
    let startedAt: Date
    var updatedAt: Date
    var completedAt: Date?
    var revision: Int = 0
    var round: Int = 1
    var order: [ContentID]
    var position: Int = 0
    var passed: [ContentID] = []
    var deferred: [ContentID] = []
    var exposed = false
    var revealed = false
    var totalExposures = 0
    var passID: UUID
    var completed: Bool { completedAt != nil }
    var currentID: ContentID? { position < order.count ? order[position] : nil }
    var remaining: [ContentID] { Array(order.dropFirst(position)) }
    var needsNextRound: Bool { !completed && currentID == nil }

    func validate() throws {
        let all = Set(vocabularyIDs), current = Set(order)
        guard !all.isEmpty, all.count == vocabularyIDs.count, all.count <= 25,
              !order.isEmpty, current.count == order.count, current.isSubset(of: all),
              (0...order.count).contains(position), round > 0, revision >= 0,
              contentVersionAtStart > 0, totalExposures >= position + (exposed ? 1 : 0),
              Set(passed).count == passed.count, Set(deferred).count == deferred.count,
              Set(passed).isDisjoint(with: Set(deferred)),
              Set(passed + deferred) == Set(order.prefix(position)),
              !revealed || exposed, currentID != nil || (!exposed && !revealed),
              !completed || (position == order.count && deferred.isEmpty),
              completed || position < order.count || !deferred.isEmpty else {
            throw VocabularyStudyError.invalidState
        }
    }
}
