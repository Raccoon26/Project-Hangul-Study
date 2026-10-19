import XCTest
import CryptoKit
@testable import HangulStudy

@MainActor
private final class FakeAudioBackend: AudioPlaybackBackend {
    var hasKoreanVoice = true
    var text: String?
    var rate: Float?
    var fileCount = 0
    var shouldStart = true
    var completion: (@MainActor (Bool) -> Void)?
    func speak(_ text: String, rate: Float, finished: @escaping @MainActor (Bool) -> Void) throws -> Bool {
        self.text = text; self.rate = rate; completion = finished; return shouldStart
    }
    func playFile(_ url: URL, rate: Float, finished: @escaping @MainActor (Bool) -> Void) throws -> Bool {
        fileCount += 1; self.rate = rate; completion = finished; return shouldStart
    }
    func stop() { completion = nil }
}
private struct NoRecordings: RecordingResolving {
    func url(for asset: RecordingAsset) -> URL? { nil }
}

@MainActor
final class PronunciationTests: XCTestCase {
    private func tts(_ text: String, usage: LearningAudio.Usage = .wordSentence) -> LearningAudio {
        LearningAudio(source: .systemTTS, usage: usage, text: text, asset: nil)
    }
    func testJamoAndComparisonNeverReachTTS() {
        let backend = FakeAudioBackend()
        let service = KoreanAudioService(backend: backend, recordings: NoRecordings())
        for value in ["ㄱ", "ㅓ", "ㅢ", "ᄀ", "가 / 카 / 까", "[한궁말]"] {
            XCTAssertEqual(service.availability(for: tts(value)), .disallowed)
            XCTAssertFalse(service.play(tts(value), speed: .normal))
        }
        XCTAssertFalse(service.play(tts("가", usage: .comparison), speed: .normal))
        XCTAssertFalse(service.play(tts("먹", usage: .isolated), speed: .normal))
        XCTAssertNil(backend.text)
    }
    func testMissingKoreanVoiceDoesNotUseAnotherLanguage() {
        let backend = FakeAudioBackend(); backend.hasKoreanVoice = false
        let service = KoreanAudioService(backend: backend, recordings: NoRecordings())
        XCTAssertEqual(service.availability(for: tts("사과")), .koreanVoiceMissing)
        XCTAssertFalse(service.play(tts("사과"), speed: .normal))
        XCTAssertNotNil(service.message); XCTAssertNil(backend.text); XCTAssertFalse(service.isPlaying)
    }
    func testNormalSlowAndStopUseSharedPolicy() {
        let backend = FakeAudioBackend()
        let service = KoreanAudioService(backend: backend, recordings: NoRecordings())
        XCTAssertTrue(service.play(tts("한국말"), speed: .normal))
        XCTAssertEqual(backend.text, "한국말") // Never substitute a phonetic spelling.
        XCTAssertEqual(backend.rate, AudioPolicy.speechRate(.normal)); XCTAssertTrue(service.isPlaying)
        XCTAssertTrue(service.play(tts("한국말"), speed: .slow))
        XCTAssertEqual(backend.rate, AudioPolicy.speechRate(.slow)); XCTAssertEqual(service.speed, .slow)
        XCTAssertGreaterThan(AudioPolicy.speechRate(.slow), AudioPolicy.speechRate(.normal) * 0.75)
        service.stop(); XCTAssertFalse(service.isPlaying)
    }
    func testMissingRecordingNeverFallsBackToTTS() {
        let backend = FakeAudioBackend()
        let service = KoreanAudioService(backend: backend, recordings: NoRecordings())
        let request = LearningAudio(source: .verifiedRecording, usage: .comparison, text: nil,
            asset: RecordingAsset(relativePath: "Audio/missing.wav", sha256: String(repeating: "0", count: 64)))
        XCTAssertEqual(service.availability(for: request), .recordingMissing)
        XCTAssertFalse(service.play(request, speed: .slow)); XCTAssertEqual(backend.fileCount, 0)
        XCTAssertNil(backend.text)
    }
    func testLateCancelledCompletionCannotFinishNewPlayback() {
        let backend = FakeAudioBackend()
        let service = KoreanAudioService(backend: backend, recordings: NoRecordings())
        _ = service.play(tts("사과"), speed: .normal)
        let oldCallback = backend.completion
        _ = service.play(tts("바다"), speed: .slow)
        oldCallback?(true)
        XCTAssertTrue(service.isPlaying); XCTAssertEqual(service.completedPlaybackCount, 0)
        backend.completion?(true)
        XCTAssertFalse(service.isPlaying); XCTAssertEqual(service.completedPlaybackCount, 1)
    }
    func testFailedPlaybackDoesNotCountAsHeard() {
        let backend = FakeAudioBackend(); backend.shouldStart = false
        let service = KoreanAudioService(backend: backend, recordings: NoRecordings())
        XCTAssertFalse(service.play(tts("사과"), speed: .normal))
        XCTAssertFalse(service.isPlaying); XCTAssertEqual(service.completedPlaybackCount, 0)
        XCTAssertNotNil(service.message)
    }
    func testInterruptedPlaybackDoesNotUnlockListeningAndCanRestart() {
        let backend = FakeAudioBackend()
        let service = KoreanAudioService(backend:backend,recordings:NoRecordings())
        XCTAssertTrue(service.play(tts("물을 마셔요."),speed:.normal))
        backend.completion?(false) // Backend interruption completion contract; no real phone/route simulation.
        XCTAssertFalse(service.isPlaying); XCTAssertEqual(service.completedPlaybackCount,0)
        XCTAssertNotNil(service.message)
        XCTAssertTrue(service.play(tts("물을 마셔요."),speed:.slow))
        let callback = backend.completion
        service.stop(); callback?(true)
        XCTAssertFalse(service.isPlaying); XCTAssertEqual(service.completedPlaybackCount,0)
    }
    func testMissingAndUnsafeRecordedPathsAreRejected() {
        let resolver = BundleRecordingResolver(root: FileManager.default.temporaryDirectory)
        for path in ["Audio/not-found.wav", "../private.wav", "/tmp/private.wav", "Audio/../private.wav"] {
            XCTAssertNil(resolver.url(for: RecordingAsset(relativePath: path, sha256: String(repeating: "0", count: 64))))
        }
    }
    func testRecordingResolverChecksChecksumBeforePlayback() throws {
        let folder = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try FileManager.default.createDirectory(at: folder.appendingPathComponent("Audio"), withIntermediateDirectories: true)
        defer { try? FileManager.default.removeItem(at: folder) }
        // A checksum fixture, not an educational recording or playable audio assertion.
        let bytes = Data("checksum-test-only".utf8)
        let url = folder.appendingPathComponent("Audio/test.wav")
        try bytes.write(to: url)
        let hash = SHA256.hash(data: bytes).map { String(format: "%02x", $0) }.joined()
        let resolver = BundleRecordingResolver(root: folder)
        XCTAssertEqual(resolver.url(for: RecordingAsset(relativePath: "Audio/test.wav", sha256: hash)), url)
        XCTAssertNil(resolver.url(for: RecordingAsset(relativePath: "Audio/test.wav", sha256: String(repeating: "0", count: 64))))
    }
    func testKoreanVoiceLookupHasSafeFallback() {
        let backend = SystemAudioBackend()
        let service = KoreanAudioService(backend: backend, recordings: NoRecordings())
        let status = service.availability(for: tts("사과"))
        XCTAssertTrue(status == .available || status == .koreanVoiceMissing)
        service.stop() // No actual sound is generated by this test.
    }
    func testPronunciationCourseQueriesAndQuizAnswers() async throws {
        let url = try XCTUnwrap(Bundle.main.url(forResource: "content", withExtension: "sqlite"))
        let repo = try SQLiteContentRepository(url: url, allowFixture: false)
        let courses = try await repo.courses()
        XCTAssertEqual(courses.map(\.title), ["ハングル入門", "発音・パッチム"])
        let course = try XCTUnwrap(courses.last)
        XCTAssertEqual(course.lessons.count, 14)
        XCTAssertEqual(course.lessons.first?.title, "パッチムの位置")
        XCTAssertEqual(course.lessons.last?.title, "総合確認")
        var rules = 0; var listening = 0
        for lesson in course.lessons {
            let steps = try await repo.lessonSteps(for: lesson.id)
            for step in steps {
                XCTAssertEqual(step.skill, "pronunciation")
                if step.kind == .pronunciation {
                    rules += 1
                    let fetched = try await repo.pronunciationRule(for: step.id)
                    XCTAssertEqual(fetched?.spelling, step.symbol)
                }
                if step.requiresListening { listening += 1; XCTAssertEqual(step.symbol, ""); XCTAssertNotNil(step.audio) }
                if step.kind == .quiz {
                    XCTAssertEqual(step.choices.filter { step.isCorrect($0.id) }.count, 1)
                    XCTAssertFalse(step.isCorrect("not-an-option"))
                }
            }
        }
        XCTAssertEqual(rules, 36); XCTAssertEqual(listening, 3)
    }
    func testListeningGateAndPronunciationProgressReopen() async throws {
        let folder = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try FileManager.default.createDirectory(at: folder, withIntermediateDirectories: true)
        defer { try? FileManager.default.removeItem(at: folder) }
        let schemaURL = try XCTUnwrap(Bundle.main.url(forResource: "user-schema-v1", withExtension: "sql"))
        let schema = try String(contentsOf: schemaURL, encoding: .utf8)
        let url = try XCTUnwrap(Bundle.main.url(forResource: "content", withExtension: "sqlite"))
        let content = try SQLiteContentRepository(url: url, allowFixture: false)
        let metadata = try await content.metadata()
        let progress = try SQLiteProgressRepository(url: folder.appendingPathComponent("user.sqlite"), schema: schema, datasetID: metadata.datasetID)
        let services = AppContainer(content: content, progress: progress, metadata: metadata)
        let courses = try await content.courses()
        let lesson = try XCTUnwrap(courses.last?.lessons.first { $0.title == "単語を読んで聞く" })
        let model = LessonViewModel(services: services, lesson: lesson)
        await model.open()
        for _ in 0..<3 { await model.act(expectedID:model.step?.id, expectedAnswered:model.currentResult != nil) }
        XCTAssertEqual(model.step?.requiresListening, true)
        model.selectedChoiceID = model.step?.correctChoiceID
        XCTAssertFalse(model.canAct)
        model.markAudioHeard(); XCTAssertTrue(model.canAct)
        await model.act(expectedID:model.step?.id, expectedAnswered:model.currentResult != nil)
        XCTAssertEqual(model.currentResult?.outcome, .correct)
        let reopened = try SQLiteProgressRepository(url: folder.appendingPathComponent("user.sqlite"), schema: schema, datasetID: metadata.datasetID)
        let second = LessonViewModel(services: AppContainer(content: content, progress: reopened, metadata: metadata), lesson: lesson)
        await second.open()
        XCTAssertEqual(second.session?.id, model.session?.id)
        XCTAssertEqual(second.currentResult?.outcome, .correct)
        XCTAssertTrue(second.canAct)
        let summary = try await reopened.summary(now: Date())
        XCTAssertEqual(summary.correctCount, 1)
        XCTAssertEqual(summary.studyCount, 4)
    }
}
