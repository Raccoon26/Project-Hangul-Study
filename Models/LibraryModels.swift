import Foundation

enum LookupKind: String, Codable, CaseIterable, Sendable { case vocabulary, grammar
    var title: String { self == .vocabulary ? "単語" : "文法" }
}
struct LookupReference: Hashable, Codable, Identifiable, Sendable {
    let contentID: ContentID
    let kind: LookupKind
    var id: String { kind.rawValue + ":" + contentID.rawValue }
}
struct LookupEntry: Identifiable, Sendable {
    let reference: LookupReference
    let title: String
    let meaning: String
    let subtitle: String
    let level: LearningLevel
    var id: String { reference.id }
}
enum SavedList: String, CaseIterable, Sendable { case favorites, difficult, recent
    var title: String { switch self { case .favorites: return "保存した項目"; case .difficult: return "苦手な項目"; case .recent: return "最近見た項目" } }
}
struct DetailConjugation: Identifiable, Sendable {
    let form: ConjugationForm
    let result: ConjugationResult
    var id: String { form.rawValue }
}
struct VocabularyDetail: Sendable {
    let card: VocabularyCard
    let pronunciation: String?
    let conjugations: [DetailConjugation]
    let irregular: Bool
    let examples: [Example]
    var hasProductionPractice: Bool = false
}
struct LookupPractice: Identifiable, Sendable {
    let id: UUID
    let kind: LookupKind
}
