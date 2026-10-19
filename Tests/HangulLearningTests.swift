import XCTest
@testable import HangulStudy

final class HangulLearningTests: XCTestCase {
    private let lessonID = ContentID(rawValue: "f382fa87-f616-4c47-946b-1910a27a8612")
    private let firstID = ContentID(rawValue: "07c42731-ebd8-4804-85e8-0d5dc88004d0")
    private let secondID = ContentID(rawValue: "5ea0656a-2530-46aa-904d-77cd6f408f06")
    private var directory: URL!
    override func setUpWithError() throws {
        directory = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try FileManager.default.createDirectory(at: directory, withIntermediateDirectories: true)
    }
    override func tearDownWithError() throws { try FileManager.default.removeItem(at: directory) }
    private func repository() throws -> SQLiteProgressRepository {
        let url = try XCTUnwrap(Bundle.main.url(forResource: "user-schema-v1", withExtension: "sql"))
        return try SQLiteProgressRepository(url: directory.appendingPathComponent("user.sqlite"),
            schema: String(contentsOf: url, encoding: .utf8), datasetID: "ko-ja-core")
    }
    private func event(_ session: LessonSession, outcome: StudyOutcome) -> StudyEvent {
        StudyEvent(id: UUID(), contentID: session.currentID, contentRevision: 1, contentVersion: session.contentVersion,
            occurredAt: Date(), timeZoneID: "Asia/Tokyo", skill: "hangul", outcome: outcome, durationMilliseconds: 0, sessionID: session.id)
    }
    func testCompositionIncludingFinalAndNoInventedJamoReading() {
        XCTAssertEqual(HangulComposition.components(of: "가"), ["ㄱ", "ㅏ"])
        XCTAssertEqual(HangulComposition.components(of: "나"), ["ㄴ", "ㅏ"])
        XCTAssertEqual(HangulComposition.components(of: "한"), ["ㅎ", "ㅏ", "ㄴ"])
        XCTAssertEqual(HangulComposition.components(of: "힣"), ["ㅎ", "ㅣ", "ㅎ"])
        XCTAssertNil(HangulComposition.components(of: "ㄱ"))
        XCTAssertNil(UnavailableHangulAudio().verifiedAudioURL(for: firstID))
    }
    func testOptionsRepeatForResumeAndVaryByAttempt() {
        let choices = (0..<4).map { QuizChoice(id: String($0), text: String($0)) }
        let order = QuizOptions.ordered(choices, seed: 123, contentID: firstID)
        XCTAssertEqual(order, QuizOptions.ordered(choices, seed: 123, contentID: firstID))
        XCTAssertEqual(Set(order.map(\.id)), Set(choices.map(\.id)))
        let orders = Set((0..<20).map { QuizOptions.ordered(choices, seed: UInt64($0), contentID: firstID).map(\.id).joined() })
        XCTAssertGreaterThan(orders.count, 1)
    }
    func testCorrectIncorrectAndUnknownChoice() {
        let step = LessonStep(id: firstID, revision: 1, kind: .quiz, symbol: "ㅏ", title: "選んでください",
            category: "確認", explanation: "説明", choices: [QuizChoice(id: "a", text: "아"), QuizChoice(id: "b", text: "오")], correctChoiceID: "a")
        XCTAssertTrue(step.isCorrect("a")); XCTAssertFalse(step.isCorrect("b")); XCTAssertFalse(step.isCorrect("missing"))
    }
    func testResumeAfterReopenKeepsSeedCursorAndFeedback() async throws {
        let repo = try repository()
        let started = try await repo.beginLesson(lessonID, steps: [firstID, secondID], contentVersion: 3, restart: false)
        try await repo.submitStep(sessionID: started.id, event: event(started, outcome: .viewed), selectedChoiceID: nil)
        let advanced = try await repo.advanceLesson(sessionID: started.id)
        XCTAssertEqual(advanced.currentID, secondID)
        try await repo.submitStep(sessionID: advanced.id, event: event(advanced, outcome: .incorrect), selectedChoiceID: "b")
        let reopened = try repository()
        let resumed = try await reopened.beginLesson(lessonID, steps: [firstID, secondID], contentVersion: 3, restart: false)
        XCTAssertEqual(resumed.id, started.id); XCTAssertEqual(resumed.seed, started.seed)
        XCTAssertEqual(resumed.currentID, secondID)
        let results = try await reopened.lessonResults(sessionID: resumed.id)
        XCTAssertEqual(results.count, 2)
        XCTAssertEqual(results.first { $0.contentID == secondID }?.outcome, .incorrect)
        XCTAssertEqual(results.first { $0.contentID == secondID }?.selectedChoiceID, "b")
        let total = try await reopened.summary(now: Date())
        XCTAssertEqual(total.studyCount, 2); XCTAssertEqual(total.incorrectCount, 1)
    }
    func testDuplicateSubmissionAndCompletionDoNotDoubleCount() async throws {
        let repo = try repository()
        let session = try await repo.beginLesson(lessonID, steps: [firstID], contentVersion: 3, restart: false)
        try await repo.submitStep(sessionID: session.id, event: event(session, outcome: .correct), selectedChoiceID: "answer")
        try await repo.submitStep(sessionID: session.id, event: event(session, outcome: .incorrect), selectedChoiceID: "wrong")
        _ = try await repo.advanceLesson(sessionID: session.id)
        let completed = try await repo.advanceLesson(sessionID: session.id)
        XCTAssertTrue(completed.completed)
        let summary = try await repo.summary(now: Date())
        XCTAssertEqual(summary.studyCount, 1); XCTAssertEqual(summary.correctCount, 1)
        let progress = try await repo.lessonProgress()
        XCTAssertEqual(progress.first?.completedCount, 1); XCTAssertEqual(progress.first?.hasActiveSession, false)
        let again = try await repo.beginLesson(lessonID, steps: [firstID], contentVersion: 3, restart: true)
        XCTAssertNotEqual(again.id, session.id)
        let oldResults = try await repo.lessonResults(sessionID: session.id)
        XCTAssertEqual(oldResults.count, 1)
        let retained = try await repo.lessonProgress()
        XCTAssertEqual(retained.first?.completedCount, 1)
    }
    func testCannotSkipUnansweredStep() async throws {
        let repo = try repository()
        let session = try await repo.beginLesson(lessonID, steps: [firstID], contentVersion: 3, restart: false)
        do { _ = try await repo.advanceLesson(sessionID: session.id); XCTFail("Unanswered step advanced") }
        catch { XCTAssertEqual(error as? LessonError, .invalidSession) }
    }
    func testContentChangeRequiresExplicitRestartWithoutDeletingHistory() async throws {
        let repo = try repository()
        let session = try await repo.beginLesson(lessonID, steps: [firstID], contentVersion: 3, restart: false)
        try await repo.submitStep(sessionID: session.id, event: event(session, outcome: .correct), selectedChoiceID: "answer")
        do { _ = try await repo.beginLesson(lessonID, steps: [firstID, secondID], contentVersion: 4, restart: false); XCTFail("Changed content resumed") }
        catch { XCTAssertEqual(error as? LessonError, .contentChanged) }
        let replacement = try await repo.beginLesson(lessonID, steps: [firstID, secondID], contentVersion: 4, restart: true)
        XCTAssertNotEqual(replacement.id, session.id)
        let history = try await repo.lessonResults(sessionID: session.id)
        XCTAssertEqual(history.count, 1)
        let summary = try await repo.summary(now: Date())
        XCTAssertEqual(summary.correctCount, 1)
    }
    func testProductionCourseOrderAndEveryLessonReadable() async throws {
        let url = try XCTUnwrap(Bundle.main.url(forResource: "content", withExtension: "sqlite"))
        let repo = try SQLiteContentRepository(url: url, allowFixture: false)
        let courses = try await repo.courses()
        let course = try XCTUnwrap(courses.first)
        XCTAssertEqual(course.title, "ハングル入門"); XCTAssertEqual(course.lessons.count, 12)
        XCTAssertEqual(course.lessons[1].title, "基本母音①")
        XCTAssertEqual(course.lessons.last?.title, "総合確認")
        for lesson in course.lessons {
            let steps = try await repo.lessonSteps(for: lesson.id)
            XCTAssertEqual(steps.count, lesson.itemCount)
            XCTAssertTrue(steps.contains { $0.kind == .quiz })
            for step in steps where step.kind == .quiz {
                XCTAssertEqual(step.choices.filter { step.isCorrect($0.id) }.count, 1)
            }
        }
    }
}
