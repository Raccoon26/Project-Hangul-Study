import Foundation

/// Stable across launches and Swift versions; never uses Swift's randomized hashValue.
enum QuizOptions {
    private struct Generator: RandomNumberGenerator {
        var state: UInt64
        mutating func next() -> UInt64 {
            state &+= 0x9E3779B97F4A7C15
            var z = state
            z = (z ^ (z >> 30)) &* 0xBF58476D1CE4E5B9
            z = (z ^ (z >> 27)) &* 0x94D049BB133111EB
            return z ^ (z >> 31)
        }
    }
    static func ordered(_ choices: [QuizChoice], seed: UInt64, contentID: ContentID) -> [QuizChoice] {
        var hash: UInt64 = 14695981039346656037
        for byte in contentID.rawValue.utf8 { hash = (hash ^ UInt64(byte)) &* 1099511628211 }
        var generator = Generator(state: seed ^ hash)
        var result = choices
        if result.count > 1 {
            for i in stride(from: result.count - 1, through: 1, by: -1) {
                let j = Int(generator.next() % UInt64(i + 1))
                result.swapAt(i, j)
            }
        }
        return result
    }
}

enum HangulComposition {
    private static let initials = Array("ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ")
    private static let vowels = Array("ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ")
    private static let finals = Array(" ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ")
    static func components(of character: Character) -> [String]? {
        let scalars = String(character).unicodeScalars
        guard scalars.count == 1, let scalar = scalars.first, (0xAC00...0xD7A3).contains(scalar.value) else { return nil }
        let index = Int(scalar.value - 0xAC00)
        var parts = [String(initials[index / 588]), String(vowels[(index % 588) / 28])]
        if index % 28 != 0 { parts.append(String(finals[index % 28])) }
        return parts
    }
    static func formulas(for text: String) -> [String] {
        text.compactMap { character in components(of: character).map { $0.joined(separator: " + ") + " → " + String(character) } }
    }
}

/// Individual jamo must never be synthesized with ordinary TTS.
protocol HangulAudioProviding: Sendable {
    func verifiedAudioURL(for contentID: ContentID) -> URL?
}
struct UnavailableHangulAudio: HangulAudioProviding {
    func verifiedAudioURL(for contentID: ContentID) -> URL? { nil }
}
