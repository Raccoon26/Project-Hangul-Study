import Foundation

enum LearningLevel: String, CaseIterable, Codable, Sendable {
    case hangul, intro, beginner
    case lowerIntermediate = "lower_intermediate"
    case intermediate
    case upperIntermediate = "upper_intermediate"
    case advanced, master, maintenance
    var japaneseName: String {
        switch self {
        case .hangul: return "ハングル"
        case .intro: return "入門"
        case .beginner: return "初級"
        case .lowerIntermediate: return "初中級"
        case .intermediate: return "中級"
        case .upperIntermediate: return "中上級"
        case .advanced: return "上級"
        case .master: return "マスター"
        case .maintenance: return "維持学習"
        }
    }
}

enum PartOfSpeech: String, Codable, Sendable {
    case noun, pronoun, numeral, verb, adjective, determiner, adverb, particle, interjection
    case auxiliaryVerb = "auxiliary_verb"
    case auxiliaryAdjective = "auxiliary_adjective"
    case boundNoun = "bound_noun"
    case prefix, suffix, ending, expression
    var japaneseName: String {
        switch self {
        case .noun: return "名詞"
        case .pronoun: return "代名詞"
        case .numeral: return "数詞"
        case .verb: return "動詞"
        case .adjective: return "形容詞"
        case .determiner: return "冠形詞"
        case .adverb: return "副詞"
        case .particle: return "助詞"
        case .interjection: return "感動詞"
        case .auxiliaryVerb: return "補助動詞"
        case .auxiliaryAdjective: return "補助形容詞"
        case .boundNoun: return "依存名詞"
        case .prefix: return "接頭辞"
        case .suffix: return "接尾辞"
        case .ending: return "語尾"
        case .expression: return "表現"
        }
    }
}

struct VocabularyQuery: Sendable {
    let level: LearningLevel?
    let prefix: String?
    init(level: LearningLevel? = nil, prefix: String? = nil) {
        self.level = level
        self.prefix = prefix
    }
}
