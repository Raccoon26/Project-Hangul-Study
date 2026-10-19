import Foundation

enum ListeningTask: String, Codable, Sendable { case meaning, korean, dictation, comprehension }
struct ListeningQuestion: Codable, Identifiable, Sendable {
    let id: ContentID
    let itemID: ContentID
    let revision: Int
    let sourceID: ContentID
    let level: LearningLevel
    let task: ListeningTask
    let prompt: String
    let transcript: String
    let translation: String
    let explanation: String
    var choices: [QuizChoice]
    let correctID: String?
    let accepted: [String]
    let recordingRequired: Bool
    let recording: RecordingAsset?
    var audio: LearningAudio { LearningAudio(source:recordingRequired ? .verifiedRecording : .systemTTS,usage:.wordSentence,text:recordingRequired ? nil : transcript,asset:recording) }
    func judge(_ answer: String) -> InputJudgement {
        task == .dictation ? ProductionAnswer.judge(answer,accepted:accepted,spacingWarning:true) :
            (ChoiceJudgement.isCorrect(answer,choices:choices,correctID:correctID) ? .correct : .incorrect)
    }
    func validate() throws {
        guard revision > 0, !transcript.isEmpty, !translation.isEmpty, !prompt.isEmpty,
              transcript.count <= 500, recordingRequired || AudioPolicy.permitsTTS(audio) else { throw GrammarError.invalidState }
        if task == .dictation {
            guard choices.isEmpty, !accepted.isEmpty, accepted.contains(transcript),
                  accepted.allSatisfy({ !ProductionAnswer.normalize($0).isEmpty }) else { throw GrammarError.invalidState }
        } else {
            guard (2...6).contains(choices.count), Set(choices.map(\.id)).count == choices.count,
                  choices.contains(where: { $0.id == correctID }) else { throw GrammarError.invalidState }
        }
    }
}
enum ListeningAction: Sendable { case played(AudioSpeed), submit(String), next }
struct ListeningSession: Codable, Sendable {
    let id: UUID
    let scope: String
    let questions: [ListeningQuestion]
    let contentVersion: Int
    let isReview: Bool
    let startedAt: Date
    var updatedAt: Date
    var position = 0
    var retry: [Int] = []
    var retrying = false
    var heard = false
    var result: InputJudgement?
    var answer: String?
    var revision = 0
    var correct = 0
    var wrong = 0
    var retrySuccess = 0
    var playCount = 0
    var slowCount = 0
    var current: ListeningQuestion? { questions.indices.contains(position) ? questions[position] : nil }
    var completed: Bool { current == nil }
    mutating func apply(_ action: ListeningAction, at now: Date) throws {
        try validate()
        guard let q = current else { throw GrammarError.invalidState }
        switch action {
        case .played(let speed):
            heard = true; playCount += 1; if speed == .slow { slowCount += 1 }
        case .submit(let value):
            guard heard, result == nil, !ProductionAnswer.normalize(value).isEmpty, value.count <= 500,
                  q.task == .dictation || q.choices.contains(where: { $0.id == value }) else { throw GrammarError.invalidState }
            answer = value; result = q.judge(value)
            if retrying { if result == .correct { retrySuccess += 1 } }
            else if result == .correct { correct += 1 }
            else { wrong += 1; retry.append(position) }
        case .next:
            guard result != nil else { throw GrammarError.invalidState }
            result = nil; answer = nil; heard = false
            if retrying { position = retry.isEmpty ? questions.count : retry.removeFirst() }
            else {
                position += 1
                if position == questions.count && !retry.isEmpty { retrying = true; position = retry.removeFirst() }
            }
        }
        revision += 1; updatedAt = now; try validate()
    }
    func validate() throws {
        for q in questions { try q.validate() }
        guard !questions.isEmpty, questions.count <= 20, contentVersion > 0, revision >= 0,
              Set(questions.map(\.itemID)).count == questions.count,
              (0...questions.count).contains(position), Set(retry).count == retry.count,
              retry.allSatisfy({ questions.indices.contains($0) }),
              (answer == nil) == (result == nil), result == nil || (heard && current != nil),
              !completed || (retry.isEmpty && result == nil), correct >= 0, wrong >= 0,
              correct + wrong <= questions.count, retrySuccess >= 0, retrySuccess <= wrong,
              playCount >= slowCount, slowCount >= 0 else { throw GrammarError.invalidState }
    }
}
