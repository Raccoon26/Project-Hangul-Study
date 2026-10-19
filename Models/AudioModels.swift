import Foundation

struct RecordingAsset: Codable, Equatable, Sendable {
    let relativePath: String
    let sha256: String
}
struct LearningAudio: Codable, Equatable, Sendable {
    enum Source: String, Codable, Equatable, Sendable { case systemTTS, verifiedRecording }
    enum Usage: String, Codable, Sendable { case wordSentence = "word_sentence", isolated, comparison }
    let source: Source
    let usage: Usage
    let text: String?
    let asset: RecordingAsset?
}
enum AudioSpeed: String, CaseIterable, Sendable { case normal, slow }
enum AudioPolicy {
    // A modest change, not extreme stretching. Auditory validation on device is still required.
    static func speechRate(_ speed: AudioSpeed) -> Float { speed == .normal ? 0.5 : 0.42 }
    static func recordingRate(_ speed: AudioSpeed) -> Float { speed == .normal ? 1.0 : 0.85 }
    static func permitsTTS(_ audio: LearningAudio) -> Bool {
        guard audio.source == .systemTTS, audio.usage == .wordSentence,
              let text = audio.text, !text.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty,
              text.count <= 500, !text.contains(where: { "[]/→+".contains($0) }) else { return false }
        var hasSyllable = false
        for scalar in text.unicodeScalars {
            let code = scalar.value
            if (0x1100...0x11FF).contains(code) || (0x3130...0x318F).contains(code) ||
                (0xA960...0xA97F).contains(code) || (0xD7B0...0xD7FF).contains(code) { return false }
            if (0xAC00...0xD7A3).contains(code) { hasSyllable = true }
        }
        return hasSyllable
    }
}
enum AudioAvailability: Equatable {
    case available, recordingMissing, koreanVoiceMissing, disallowed
    var message: String? {
        switch self {
        case .available: return nil
        case .recordingMissing: return "この発音の確認用音声は、今後追加予定です。"
        case .koreanVoiceMissing: return "韓国語のシステム音声を利用できません。iPhoneの設定で音声の追加状況をご確認ください。"
        case .disallowed: return "この教材ではシステム音声を使用しません。"
        }
    }
}
