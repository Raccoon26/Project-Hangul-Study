import Foundation

enum ConjugationForm: String, Codable, CaseIterable, Sendable {
    case present, past, future, negativeShort, negativeLong, wish, connective, reason, condition
    var title: String {
        switch self {
        case .present: return "現在・丁寧"
        case .past: return "過去・丁寧"
        case .future: return "予定・見込み"
        case .negativeShort: return "否定・안"
        case .negativeLong: return "否定・지 않아요"
        case .wish: return "希望・고 싶어요"
        case .connective: return "つなぐ・고"
        case .reason: return "理由・아/어서"
        case .condition: return "条件・(으)면"
        }
    }
}
struct ConjugationResult: Sendable {
    let stem: String
    let form: String
    let explanation: String
}
enum ConjugationEngine {
    private static func parts(_ text: String) throws -> (String, Int, Int, Int) {
        guard let value = text.unicodeScalars.last?.value, (0xAC00...0xD7A3).contains(value) else { throw GrammarError.changedContent }
        let n = Int(value)-0xAC00
        return (String(text.dropLast()), n/588, (n%588)/28, n%28)
    }
    private static func syllable(_ l: Int, _ v: Int, _ t: Int) -> String {
        String(UnicodeScalar(0xAC00+l*588+v*28+t)!)
    }
    private static func vowelStem(_ stem: String, irregular: String) throws -> String {
        let (p,l,v,t) = try parts(stem)
        if irregular == "b" {
            guard t == 17 else { throw GrammarError.changedContent }
            return p+syllable(l,v,0)+(["돕","곱"].contains(stem) ? "와" : "워")
        }
        if irregular == "d" {
            guard t == 7 else { throw GrammarError.changedContent }
            return p+syllable(l,v,8)+([0,8].contains(v) ? "아" : "어")
        }
        if irregular == "s" {
            guard t == 19 else { throw GrammarError.changedContent }
            return p+syllable(l,v,0)+([0,8].contains(v) ? "아" : "어")
        }
        if irregular == "reu" {
            guard stem.hasSuffix("르"), !p.isEmpty else { throw GrammarError.changedContent }
            let (pp,pl,pv,pt) = try parts(p)
            guard pt == 0 else { throw GrammarError.changedContent }
            return pp+syllable(pl,pv,8)+([0,8].contains(pv) ? "라" : "러")
        }
        // ㅎ lexical exceptions require reviewed overrides; never guess their vowel.
        if irregular == "h" { throw GrammarError.changedContent }
        if stem.hasSuffix("하") { return String(stem.dropLast())+"해" }
        guard irregular == "none" else { throw GrammarError.changedContent }
        if t != 0 { return stem+([0,8].contains(v) ? "아" : "어") }
        if v == 18 {
            let preceding = try? parts(p)
            return p+syllable(l,preceding.map { [0,8].contains($0.2) } == true ? 0 : 4,0)
        }
        let contracted: [Int:Int] = [0:0,4:4,6:6,8:9,9:9,13:14,14:14,20:6,1:1,5:5,7:7,10:11,11:11,15:15]
        if let target = contracted[v] { return p+syllable(l,target,0) }
        return stem+"어"
    }
    static func generate(lemma: String, partOfSpeech: String, irregular: String?, form: ConjugationForm, overrides: [String:String] = [:]) throws -> ConjugationResult {
        guard ["verb","adjective"].contains(partOfSpeech), lemma.hasSuffix("다"), lemma.count > 1,
              let irregular = irregular, ["none","other","b","d","s","reu","h"].contains(irregular) else { throw GrammarError.changedContent }
        guard form != .wish || partOfSpeech == "verb" else { throw GrammarError.changedContent }
        let stem = String(lemma.dropLast())
        let (_,_,_,t) = try parts(stem)
        if let override = overrides[form.rawValue], !override.isEmpty {
            return ConjugationResult(stem:stem,form:override,explanation:"この語は、確認済みの特別な形を使います。")
        }
        guard lemma != "푸다" else { throw GrammarError.changedContent }
        guard irregular != "other" || stem.hasSuffix("하") else { throw GrammarError.changedContent }
        var value: String
        switch form {
        case .connective: value = stem+"고"
        case .wish: value = stem+"고 싶어요"
        case .negativeLong: value = stem+"지 않아요"
        case .negativeShort:
            // 공부하다 -> 공부 안 해요 needs lexical boundary metadata.
            guard !stem.hasSuffix("하") || stem == "하" else { throw GrammarError.changedContent }
            value = "안 " + (try vowelStem(stem,irregular:irregular))+"요"
        case .present, .past, .reason:
            let base = try vowelStem(stem,irregular:irregular)
            if form == .past {
                let (p,l,v,t) = try parts(base)
                guard t == 0 else { throw GrammarError.changedContent }
                value = p+syllable(l,v,20)+"어요"
            } else { value = base+(form == .present ? "요" : "서") }
        case .future, .condition:
            var base = stem
            let (p,l,v,_) = try parts(stem)
            if irregular == "b" { guard t == 17 else { throw GrammarError.changedContent }; base = p+syllable(l,v,0)+"우" }
            // ㄷ becomes ㄹ but still takes 으: 걷다 → 걸으면 / 걸을 거예요.
            if irregular == "d" { guard t == 7 else { throw GrammarError.changedContent }; base = p+syllable(l,v,8)+"으" }
            if irregular == "s" { guard t == 19 else { throw GrammarError.changedContent }; base = p+syllable(l,v,0)+"으" }
            if irregular == "h" { guard t == 27 else { throw GrammarError.changedContent }; base = p+syllable(l,v,0) }
            let (bp,bl,bv,bt) = try parts(base)
            if form == .condition { value = base+([0,8].contains(bt) ? "면" : "으면") }
            else { value = (bt == 0 ? bp+syllable(bl,bv,8) : bt == 8 ? base : base+"을")+" 거예요" }
        }
        return ConjugationResult(stem:stem,form:value,explanation:"基本形の다を取り、語幹「\(stem)-」に付く形を確認します。\(form.title)：\(value)")
    }
}

enum InputJudgement: String, Codable, Sendable { case correct, spacing, incorrect }
enum ProductionAnswer {
    static func normalize(_ value: String) -> String {
        value.precomposedStringWithCanonicalMapping.split(whereSeparator: { $0.isWhitespace }).joined(separator:" ")
    }
    static func judge(_ value: String, accepted: [String], spacingWarning: Bool) -> InputJudgement {
        let value = normalize(value), answers = accepted.map(normalize)
        guard !value.isEmpty else { return .incorrect }
        if answers.contains(value) { return .correct }
        if spacingWarning && answers.contains(where: { $0.replacingOccurrences(of:" ",with:"") == value.replacingOccurrences(of:" ",with:"") }) { return .spacing }
        return .incorrect
    }
}
