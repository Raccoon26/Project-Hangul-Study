import XCTest
@testable import HangulStudy

@MainActor
private final class ReminderMock: ReminderBackend {
    var status: ReminderAuthorization = .notDetermined
    var grant = false
    var requests = 0
    var scheduled: [(Int,Int)] = []
    var cancellations = 0
    var fail = false
    func authorization() async -> ReminderAuthorization { status }
    func request() async throws -> Bool { requests += 1; status = grant ? .allowed : .denied; return grant }
    func schedule(hour: Int, minute: Int) async throws {
        if fail { throw ReviewError.invalidState }; scheduled.append((hour,minute))
    }
    func cancel() { cancellations += 1 }
}
final class StatisticsAndSettingsTests: XCTestCase {
    func testEmptyAccuracyAndCalendarAcrossDST() throws {
        XCTAssertEqual(ActivityWindow.accuracy(correct:0,wrong:0),"まだ記録がありません")
        XCTAssertTrue(ActivityWindow.accuracy(correct:1,wrong:3).hasPrefix("25%"))
        let zone = try XCTUnwrap(TimeZone(identifier:"America/New_York"))
        let now = try XCTUnwrap(ISO8601DateFormatter().date(from:"2026-03-09T04:30:00Z"))
        let start = StatisticsCalendar.start(days:2,now:now,timeZone:zone)
        XCTAssertEqual(now.timeIntervalSince(start),23.5*3600)
        let tokyo = try XCTUnwrap(TimeZone(identifier:"Asia/Tokyo"))
        XCTAssertNotEqual(StatisticsCalendar.start(days:1,now:now,timeZone:zone),StatisticsCalendar.start(days:1,now:now,timeZone:tokyo))
    }
    @MainActor
    func testPreferencesPersistAndNoLaunchPermissionPrompt() async throws {
        let name = UUID().uuidString, backend = ReminderMock()
        let defaults = try XCTUnwrap(UserDefaults(suiteName:name)); defer { defaults.removePersistentDomain(forName:name) }
        let store = LearningPreferencesStore(defaults:defaults,reminders:backend)
        await store.reconcile(); XCTAssertEqual(backend.requests,0)
        store.setAmount(.standard)
        let date = try XCTUnwrap(Calendar.current.date(from:DateComponents(year:2026,month:1,day:1,hour:9,minute:35)))
        await store.setTime(date)
        let savedPreferences = defaults.data(forKey:LearningPreferencesStore.key)
        let content = try SQLiteContentRepository(url:XCTUnwrap(Bundle.main.url(forResource:"content",withExtension:"sqlite")),allowFixture:false)
        let metadata = try await content.metadata()
        XCTAssertEqual(metadata.contentVersion,29)
        let courses = try await content.courses()
        let integrated = try XCTUnwrap(courses.first { $0.title == "初中級・会話と現代生活" })
        _ = try await content.lessonSteps(for:try XCTUnwrap(integrated.lessons.first).id)
        XCTAssertEqual(defaults.data(forKey:LearningPreferencesStore.key),savedPreferences)
        let reopened = LearningPreferencesStore(defaults:defaults,reminders:backend)
        XCTAssertEqual(reopened.value.amount,.standard); XCTAssertEqual(reopened.value.hour,9); XCTAssertEqual(reopened.value.minute,35)
        XCTAssertFalse(reopened.value.reminderEnabled); XCTAssertEqual(backend.requests,0)
    }
    @MainActor
    func testPermissionDeniedDoesNotRepeatRequestOrEnableReminder() async throws {
        let name = UUID().uuidString, backend = ReminderMock()
        let defaults = try XCTUnwrap(UserDefaults(suiteName:name)); defer { defaults.removePersistentDomain(forName:name) }
        let store = LearningPreferencesStore(defaults:defaults,reminders:backend)
        await store.setReminder(true); await store.setReminder(true)
        XCTAssertEqual(backend.requests,1); XCTAssertTrue(store.denied); XCTAssertFalse(store.value.reminderEnabled)
        XCTAssertTrue(backend.scheduled.isEmpty)
    }
    @MainActor
    func testEnableDisableFailureAndRevokedPermission() async throws {
        let name = UUID().uuidString, backend = ReminderMock(); backend.grant = true
        let defaults = try XCTUnwrap(UserDefaults(suiteName:name)); defer { defaults.removePersistentDomain(forName:name) }
        let store = LearningPreferencesStore(defaults:defaults,reminders:backend)
        await store.setReminder(true); XCTAssertTrue(store.value.reminderEnabled); XCTAssertEqual(backend.scheduled.count,1)
        await store.setReminder(false); XCTAssertFalse(store.value.reminderEnabled)
        backend.fail = true; await store.setReminder(true); XCTAssertFalse(store.value.reminderEnabled)
        backend.fail = false; await store.setReminder(true); XCTAssertTrue(store.value.reminderEnabled)
        backend.status = .denied; await store.reconcile(); XCTAssertFalse(store.value.reminderEnabled); XCTAssertTrue(store.denied)
        XCTAssertEqual(backend.requests,1)
    }
    private func progress(_ url: URL) throws -> SQLiteProgressRepository {
        let schema = try String(contentsOf:XCTUnwrap(Bundle.main.url(forResource:"user-schema-v1",withExtension:"sql")),encoding:.utf8)
        return try SQLiteProgressRepository(url:url,schema:schema,datasetID:"dev12-tests")
    }
    func testEmptyAndPartialStatisticsPersist() async throws {
        let folder = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try FileManager.default.createDirectory(at:folder,withIntermediateDirectories:true)
        defer { try? FileManager.default.removeItem(at:folder) }
        let url = folder.appendingPathComponent("u.sqlite"), repo = try progress(url), now = Date()
        let empty = try await repo.statistics(now:now,timeZone:.current)
        XCTAssertTrue(empty.windows.allSatisfy { $0.actions == 0 }); XCTAssertEqual(empty.seenWords,0)
        let event = StudyEvent(id:UUID(),contentID:ContentID(rawValue:UUID().uuidString),contentRevision:1,contentVersion:13,occurredAt:now,timeZoneID:TimeZone.current.identifier,skill:"production_polite",outcome:.correct,durationMilliseconds:0,sessionID:nil)
        try await repo.record(event); try await repo.record(event)
        let reopened = try progress(url)
        let stats = try await reopened.statistics(now:now,timeZone:.current)
        XCTAssertEqual(stats.windows.first?.actions,1); XCTAssertEqual(stats.windows.first?.productionCorrect,1); XCTAssertEqual(stats.seenWords,1)
    }
    func testUnchangedLessonSurvivesContentReleaseWithoutReset() async throws {
        let folder = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try FileManager.default.createDirectory(at:folder,withIntermediateDirectories:true)
        defer { try? FileManager.default.removeItem(at:folder) }
        let url = folder.appendingPathComponent("u.sqlite"), repo = try progress(url)
        let lesson = ContentID(rawValue:UUID().uuidString), ids = (0..<2).map { _ in ContentID(rawValue:UUID().uuidString) }
        let session = try await repo.beginLesson(lesson,steps:ids,contentVersion:12,restart:false)
        try await repo.submitStep(sessionID:session.id,event:StudyEvent(id:UUID(),contentID:ids[0],contentRevision:1,contentVersion:12,occurredAt:Date(),timeZoneID:"Asia/Tokyo",skill:"hangul",outcome:.viewed,durationMilliseconds:0,sessionID:session.id),selectedChoiceID:nil)
        _ = try await repo.advanceLesson(sessionID:session.id)
        let reopened = try progress(url)
        let resumed = try await reopened.beginLesson(lesson,steps:ids,contentVersion:13,restart:false)
        XCTAssertEqual(resumed.id,session.id); XCTAssertEqual(resumed.currentID,ids[1]); XCTAssertEqual(resumed.contentVersion,13)
        let results = try await reopened.lessonResults(sessionID:session.id); XCTAssertEqual(results.count,1)
    }
    func testFiveItemReviewPartialCompletionColdResumeAndBacklog() async throws {
        let folder = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try FileManager.default.createDirectory(at:folder,withIntermediateDirectories:true)
        defer { try? FileManager.default.removeItem(at:folder) }
        let url = folder.appendingPathComponent("u.sqlite"), repo = try progress(url)
        let ids = (0..<20).map { _ in ContentID(rawValue:UUID().uuidString) }
        let set = try await repo.createVocabularySet(level:.intro,ids:ids)
        var round = try await repo.beginVocabularySet(set.id,contentVersion:13,restart:false)
        for _ in ids {
            round = try await repo.updateVocabularySession(round.id,expectedRevision:round.revision,action:.expose(revision:1,contentVersion:13))
            round = try await repo.updateVocabularySession(round.id,expectedRevision:round.revision,action:.reveal)
            round = try await repo.updateVocabularySession(round.id,expectedRevision:round.revision,action:.decide(.known))
        }
        let now = Date().addingTimeInterval(2*86400)
        var session = try await repo.beginReview(now:now,limit:5)
        XCTAssertEqual(session.ids.count,5)
        for _ in 0..<4 {
            let id = try XCTUnwrap(session.currentID)
            session = try await repo.exposeReview(sessionID:session.id,contentID:id,contentRevision:1,contentVersion:13,now:now,timeZoneID:"Asia/Tokyo")
            session = try await repo.revealReview(sessionID:session.id,contentID:id,now:now)
            session = try await repo.submitReview(sessionID:session.id,contentID:id,rating:.remembered,now:now,timeZoneID:"Asia/Tokyo")
        }
        let reopened = try progress(url)
        let resumed = try await reopened.beginReview(now:now,limit:20)
        XCTAssertEqual(resumed.id,session.id); XCTAssertEqual(resumed.ids,session.ids); XCTAssertEqual(resumed.currentID,session.currentID)
        XCTAssertEqual(resumed.completedCount,4); XCTAssertFalse(resumed.completed)
        let summary = try await reopened.reviewSummary(now:now,timeZoneID:"Asia/Tokyo"); XCTAssertEqual(summary.due,16)
    }
}

extension StatisticsAndSettingsTests {
    @MainActor
    func testDelayedGrammarAndVocabularyActionsDoNotAdvanceFreshState() async throws {
        let folder = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try FileManager.default.createDirectory(at:folder,withIntermediateDirectories:true)
        defer { try? FileManager.default.removeItem(at:folder) }
        let content = try SQLiteContentRepository(url:XCTUnwrap(Bundle.main.url(forResource:"content",withExtension:"sqlite")),allowFixture:false)
        let repo = try progress(folder.appendingPathComponent("u.sqlite"))
        let services = AppContainer(content:content,progress:repo,metadata:try await content.metadata())
        let rows = try await content.lookup("학교",offset:0)
        let id = try XCTUnwrap(rows.first).reference.contentID
        let set = try await repo.createVocabularySet(level:.intro,ids:[id])
        let words = VocabularyStudyViewModel(services:services,set:set)
        await words.open(); let revision = try XCTUnwrap(words.session?.revision)
        await words.act(.reveal,expectedRevision:revision)
        let revealed = words.session
        await words.act(.decide(.known),expectedRevision:revision)
        XCTAssertEqual(words.session,revealed); XCTAssertNil(words.errorMessage)
        let lessons = try await content.grammarLessons(level:.intro,after:-1,limit:1)
        let model = GrammarViewModel(services:services,lesson:try XCTUnwrap(lessons.first))
        await model.open(); let old = try XCTUnwrap(model.session?.revision)
        await model.send(.next,expectedRevision:old)
        let advanced = model.session
        await model.send(.next,expectedRevision:old)
        XCTAssertEqual(model.session,advanced); XCTAssertEqual(model.session?.page,1); XCTAssertNil(model.error)
    }
    @MainActor
    func testDelayedLessonNextDoesNotSkipFollowingExplanation() async throws {
        let folder = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try FileManager.default.createDirectory(at:folder,withIntermediateDirectories:true)
        defer { try? FileManager.default.removeItem(at:folder) }
        let c = try SQLiteContentRepository(url:XCTUnwrap(Bundle.main.url(forResource:"content",withExtension:"sqlite")),allowFixture:false)
        let p = try progress(folder.appendingPathComponent("u.sqlite"))
        let courses = try await c.courses(), lesson = try XCTUnwrap(courses.first?.lessons.first)
        let model = LessonViewModel(services:AppContainer(content:c,progress:p,metadata:try await c.metadata()),lesson:lesson)
        await model.open()
        let first = try XCTUnwrap(model.step?.id)
        await model.act(expectedID:first,expectedAnswered:false)
        let position = model.session?.currentID, summary = try await p.summary(now:Date())
        await model.act(expectedID:first,expectedAnswered:false)
        XCTAssertEqual(model.session?.currentID,position)
        let after = try await p.summary(now:Date()); XCTAssertEqual(after.studyCount,summary.studyCount)
    }
    @MainActor
    func testOffPreferencesCancelStalePendingReminderWithoutPermissionPrompt() async throws {
        let name = UUID().uuidString, backend = ReminderMock(); backend.status = .allowed
        let defaults = try XCTUnwrap(UserDefaults(suiteName:name)); defer { defaults.removePersistentDomain(forName:name) }
        let store = LearningPreferencesStore(defaults:defaults,reminders:backend)
        await store.reconcile()
        XCTAssertEqual(backend.cancellations,1); XCTAssertEqual(backend.requests,0); XCTAssertFalse(store.value.reminderEnabled)
    }
}
