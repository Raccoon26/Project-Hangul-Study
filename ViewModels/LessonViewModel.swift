import SwiftUI

@MainActor
final class LessonViewModel: ObservableObject {
    @Published private(set) var steps: [LessonStep] = []
    @Published private(set) var session: LessonSession?
    @Published private(set) var results: [LessonStepResult] = []
    @Published private(set) var busy = false
    @Published private(set) var errorMessage: String?
    @Published private(set) var needsRestart = false
    @Published private(set) var heardStepID: ContentID?
    @Published var selectedChoiceID: String?
    private let services: AppContainer
    let lesson: Lesson

    init(services: AppContainer, lesson: Lesson) { self.services = services; self.lesson = lesson }
    var step: LessonStep? { steps.first { $0.id == session?.currentID } }
    var index: Int { steps.firstIndex { $0.id == session?.currentID } ?? 0 }
    var currentResult: LessonStepResult? { results.first { $0.contentID == session?.currentID } }
    var completed: Bool { session?.completed == true }
    var correctCount: Int { results.filter { $0.outcome == .correct }.count }
    var quizCount: Int { steps.filter { $0.kind == .quiz }.count }
    var options: [QuizChoice] {
        guard let step = step, let session = session else { return [] }
        return QuizOptions.ordered(step.choices, seed: session.seed, contentID: step.id)
    }
    func markAudioHeard() { heardStepID = step?.id }
    var canAct: Bool { !busy && step != nil && (step?.requiresListening != true || currentResult != nil || heardStepID == step?.id) && (step?.kind != .quiz || currentResult != nil || selectedChoiceID != nil) }
    var actionTitle: String {
        if step?.kind == .quiz && currentResult == nil { return "答える" }
        return index + 1 == steps.count ? "レッスンを完了する" : "次へ"
    }
    func open(restart: Bool = false) async {
        guard !busy else { return }
        busy = true; errorMessage = nil; needsRestart = false
        defer { busy = false }
        do {
            let loaded = try await services.content.lessonSteps(for: lesson.id)
            let saved = try await services.progress.beginLesson(lesson.id, steps: loaded.map(\.id), contentVersion: services.metadata.contentVersion, restart: restart)
            let answers = try await services.progress.lessonResults(sessionID: saved.id)
            steps = loaded; session = saved; results = answers; heardStepID = nil
            selectedChoiceID = currentResult?.selectedChoiceID
        } catch {
            needsRestart = (error as? LessonError) == .contentChanged
            errorMessage = needsRestart ? LearningErrorMessage.message(for: error) : "レッスンを開けませんでした。もう一度お試しください。"
        }
    }
    func act(expectedID: ContentID?, expectedAnswered: Bool) async {
        guard canAct, let session = session, let step = step, step.id == expectedID, (currentResult != nil) == expectedAnswered else { return }
        busy = true; errorMessage = nil
        defer { busy = false }
        do {
            if currentResult == nil {
                let choice = step.kind == .quiz ? selectedChoiceID : nil
                let outcome: StudyOutcome = step.kind == .quiz ? (step.isCorrect(choice ?? "") ? .correct : .incorrect) : .viewed
                let event = StudyEvent(id: UUID(), contentID: step.id, contentRevision: step.revision,
                    contentVersion: session.contentVersion, occurredAt: Date(), timeZoneID: TimeZone.current.identifier,
                    skill: step.skill, outcome: outcome, durationMilliseconds: 0, sessionID: session.id)
                try await services.progress.submitStep(sessionID: session.id, event: event, selectedChoiceID: choice)
                results = try await services.progress.lessonResults(sessionID: session.id)
                if step.kind == .quiz { return }
            }
            self.session = try await services.progress.advanceLesson(sessionID: session.id)
            heardStepID = nil
            selectedChoiceID = currentResult?.selectedChoiceID
        } catch {
            errorMessage = "保存できませんでした。学習位置は進めていません。もう一度ボタンを押してください。"
        }
    }
}
