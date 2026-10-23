import XCTest
import Security
@testable import HangulStudy

@MainActor
final class NativeRegressionTests: XCTestCase {
    func testSystemAudioBackendAndItsObserversReleaseAfterUse() {
        weak var released: SystemAudioBackend?
        autoreleasepool {
            let backend = SystemAudioBackend()
            released = backend; backend.stop()
        }
        XCTAssertNil(released,"Notification callbacks must not retain the audio backend")
    }
    private struct Cache: PurchaseCacheStoring {
        let result: PurchaseCacheRead
        func load() -> PurchaseCacheRead { result }
        func write(_ value: VerifiedPurchaseCache?) -> OSStatus { errSecNotAvailable }
    }
    func testKeychainUnavailableNeverBecomesFreeAtColdStart() {
        for status in [errSecNotAvailable, errSecInteractionNotAllowed, errSecMissingEntitlement, errSecDecode] {
            let service = PurchaseService(cache:Cache(result:.unavailable(status)))
            XCTAssertEqual(service.state,.verificationFailed)
            XCTAssertFalse(service.state.permitsAds)
        }
        XCTAssertEqual(PurchaseService(cache:Cache(result:.missing)).state,.checking)
        let value = VerifiedPurchaseCache(productID:MonetizationConfiguration.productID,transactionID:42,purchaseDate:Date())
        XCTAssertEqual(PurchaseService(cache:Cache(result:.verified(value))).state,.offlineProtected)
    }
    func testRealKeychainInsertUpdateColdReadAndDelete() {
        let store = PurchaseCacheStore()
        let previous = store.read()
        defer { store.write(previous) }
        XCTAssertEqual(store.write(nil),errSecSuccess)
        let first = VerifiedPurchaseCache(productID:MonetizationConfiguration.productID,transactionID:41,purchaseDate:Date(timeIntervalSince1970:1_800_000_000))
        XCTAssertEqual(store.write(first),errSecSuccess,"Requires normal Simulator ad-hoc signing and application identifier entitlement")
        XCTAssertEqual(PurchaseCacheStore().read(),first)
        let second = VerifiedPurchaseCache(productID:first.productID,transactionID:42,purchaseDate:first.purchaseDate)
        XCTAssertEqual(store.write(second),errSecSuccess)
        XCTAssertEqual(PurchaseCacheStore().read(),second)
        XCTAssertEqual(store.write(nil),errSecSuccess)
        if case .missing = store.load() {} else { XCTFail("Deleted cache must be missing") }
    }
    func testEveryPublishedDoedaDictionaryFormAndProductionRubric() async throws {
        let url = try XCTUnwrap(Bundle.main.url(forResource:"content",withExtension:"sqlite"))
        let db = try SQLiteConnection(url:url,readOnly:true)
        let content = try SQLiteContentRepository(url:url,allowFixture:false)
        let rows = try db.query("SELECT v.id,v.headword,v.part_of_speech,v.irregular_type FROM vocabulary v JOIN content_items i ON i.id=v.id WHERE i.is_active=1 AND v.part_of_speech IN ('verb','adjective') AND v.headword LIKE '%되다'")
        XCTAssertEqual(rows.count,85) // Content29 impact cohort; no data changes in DATA10-7.
        for row in rows {
            let lemma = try row.text("headword"), prefix = String(try row.text("headword").dropLast(2))
            let detail = try await content.vocabularyDetail(id:ContentID(rawValue:row.text("id")))
            for (form, expected, uncontracted) in [(ConjugationForm.present,prefix+"돼요",prefix+"되어요"),(.past,prefix+"됐어요",prefix+"되었어요"),(.future,prefix+"될 거예요",prefix+"될 거예요")] {
                let generated = try ConjugationEngine.generate(lemma:lemma,partOfSpeech:row.text("part_of_speech"),irregular:row["irregular_type"]?.string,form:form)
                XCTAssertEqual(generated.form,expected,lemma)
                let displayed = try XCTUnwrap(detail.conjugations.first { $0.form == form })
                XCTAssertTrue([expected,uncontracted].contains(displayed.result.form),lemma+": "+displayed.result.form)
            }
        }
        // The fix must keep all published authored questions loadable, including overrides.
        var cursor = "", checked = 0
        while true {
            let entries = try await content.productionVocabulary(after:cursor)
            if entries.isEmpty { break }
            for (id,_) in entries { checked += try await content.productionQuestions(id:id).count }
            cursor = try XCTUnwrap(entries.last).0.rawValue
        }
        XCTAssertEqual(checked,1227)
    }
    func testAllFourPublishedHAdjectivesHaveReviewedDictionaryPresentAndPast() async throws {
        let content = try SQLiteContentRepository(url:XCTUnwrap(Bundle.main.url(forResource:"content",withExtension:"sqlite")),allowFixture:false)
        let forms = [("어떻다","어때요","어땠어요","어떨 거예요"),("빨갛다","빨개요","빨갰어요","빨갈 거예요"),("파랗다","파래요","파랬어요","파랄 거예요"),("노랗다","노래요","노랬어요","노랄 거예요")]
        for (lemma,present,past,future) in forms {
            let entries = try await content.lookup(lemma,offset:0)
            let entry = try XCTUnwrap(entries.first { $0.title == lemma && $0.reference.kind == .vocabulary })
            let detail = try await content.vocabularyDetail(id:entry.reference.contentID)
            for (form,expected) in [(ConjugationForm.present,present),(.past,past),(.future,future)] {
                XCTAssertEqual(try ConjugationEngine.generate(lemma:lemma,partOfSpeech:"adjective",irregular:"h",form:form).form,expected)
                XCTAssertEqual(detail.conjugations.first { $0.form == form }?.result.form,expected)
            }
        }
        XCTAssertThrowsError(try ConjugationEngine.generate(lemma:"누렇다",partOfSpeech:"adjective",irregular:"h",form:.present))
        XCTAssertEqual(try ConjugationEngine.generate(lemma:"파랗다",partOfSpeech:"adjective",irregular:"h",form:.present,overrides:["present":"검수한 예외"]).form,"검수한 예외")
    }

    private func repository(_ directory: URL) throws -> SQLiteProgressRepository {
        let schema = try String(contentsOf:XCTUnwrap(Bundle.main.url(forResource:"user-schema-v1",withExtension:"sql")),encoding:.utf8)
        return try SQLiteProgressRepository(url:directory.appendingPathComponent("user.sqlite"),schema:schema,datasetID:"ko-ja-core")
    }
    func testDictationDraftColdResumeLateWritesAndRetryDoNotGradeOrResetSRS() async throws {
        let directory = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try FileManager.default.createDirectory(at:directory,withIntermediateDirectories:true)
        defer { try? FileManager.default.removeItem(at:directory) }
        let content = try SQLiteContentRepository(url:XCTUnwrap(Bundle.main.url(forResource:"content",withExtension:"sqlite")),allowFixture:false)
        let questions = try await content.listeningQuestions(level:.intro,ids:nil)
        let q = try XCTUnwrap(questions.first { $0.task == .dictation })
        let progress = try repository(directory)
        let initial = try await progress.beginListening(scope:"practice:intro:draft",questions:[q],version:29,review:false)
        try await progress.saveListeningDraft(initial,text:"물을 마",sequence:2)
        try await progress.saveListeningDraft(initial,text:"물",sequence:1) // Delayed older edit.
        let cold = try repository(directory)
        let initialSaved = try await cold.activeListening(scope:initial.scope)
        var saved = try XCTUnwrap(initialSaved)
        XCTAssertEqual(saved.draft,"물을 마"); XCTAssertEqual(saved.revision,initial.revision)
        XCTAssertNil(saved.answer); XCTAssertNil(saved.result); XCTAssertFalse(saved.heard)
        let emptySummary = try await cold.summary(now:Date())
        XCTAssertEqual(emptySummary.studyCount,0)
        let noSRS = try await cold.reviewState(for:q.itemID,skill:"listening")
        XCTAssertNil(noSRS)
        saved = try await cold.updateListening(saved,action:.played(.slow),now:Date())
        XCTAssertEqual(saved.draft,"물을 마"); XCTAssertTrue(saved.heard)
        try await cold.saveListeningDraft(initial,text:"保存した続き",sequence:3) // Playback revision may advance.
        let draftSaved = try await cold.activeListening(scope:initial.scope)
        saved = try XCTUnwrap(draftSaved)
        XCTAssertEqual(saved.draft,"保存した続き"); XCTAssertEqual(saved.slowCount,1)
        let firstTurn = saved
        saved = try await cold.updateListening(saved,action:.submit("誤答"),now:Date())
        XCTAssertNil(saved.draft); XCTAssertEqual(saved.wrong,1)
        saved = try await cold.updateListening(saved,action:.next,now:Date())
        XCTAssertTrue(saved.retrying); XCTAssertFalse(saved.heard)
        try await cold.saveListeningDraft(saved,text:"新しい再入力",sequence:4)
        try await cold.saveListeningDraft(firstTurn,text:"遅れた初回入力",sequence:99)
        let retrySaved = try await cold.activeListening(scope:initial.scope)
        saved = try XCTUnwrap(retrySaved)
        XCTAssertEqual(saved.draft,"新しい再入力")
        let originalDue = try await cold.reviewState(for:q.itemID,skill:"listening")
        saved = try await cold.updateListening(saved,action:.played(.normal),now:Date())
        saved = try await cold.updateListening(saved,action:.submit(q.transcript),now:Date())
        let afterRetry = try await cold.reviewState(for:q.itemID,skill:"listening")
        XCTAssertEqual(originalDue?.nextReviewAt,afterRetry?.nextReviewAt)
        XCTAssertEqual(saved.correct,0); XCTAssertEqual(saved.retrySuccess,1); XCTAssertNil(saved.draft)
        var json = try XCTUnwrap(JSONSerialization.jsonObject(with:JSONEncoder().encode(initial)) as? [String:Any])
        json.removeValue(forKey:"draft"); json.removeValue(forKey:"draftSequence")
        let legacy = try JSONDecoder().decode(ListeningSession.self,from:JSONSerialization.data(withJSONObject:json))
        try legacy.validate(); XCTAssertNil(legacy.draft)
    }
    func testProductionDraftColdResumeAndGradingKeepLegacySnapshotContract() async throws {
        let directory = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try FileManager.default.createDirectory(at:directory,withIntermediateDirectories:true)
        defer { try? FileManager.default.removeItem(at:directory) }
        let content = try SQLiteContentRepository(url:XCTUnwrap(Bundle.main.url(forResource:"content",withExtension:"sqlite")),allowFixture:false)
        let entries = try await content.productionVocabulary(after:"")
        let id = try XCTUnwrap(entries.first).0
        let questions = try await content.productionQuestions(id:id)
        let q = try XCTUnwrap(questions.first)
        let progress = try repository(directory)
        var s = try await progress.beginProduction(scope:id,questions:[q],version:29)
        s = try await progress.updateProduction(s,answer:nil)
        try await progress.saveProductionDraft(s,text:"入力の続き",sequence:2)
        try await progress.saveProductionDraft(s,text:"古い入力",sequence:1)
        let cold = try repository(directory)
        let active = try await cold.activeProduction(scope:id)
        let restored = try XCTUnwrap(active)
        XCTAssertEqual(restored.draft,"入力の続き"); XCTAssertEqual(restored.revision,s.revision)
        XCTAssertNil(restored.result); XCTAssertNil(restored.answer)
        let summary = try await cold.summary(now:Date())
        XCTAssertEqual(summary.studyCount,0)
        var legacy = try XCTUnwrap(JSONSerialization.jsonObject(with:JSONEncoder().encode(s)) as? [String:Any])
        legacy.removeValue(forKey:"draft"); legacy.removeValue(forKey:"draftSequence")
        let decoded = try JSONDecoder().decode(ProductionSession.self,from:JSONSerialization.data(withJSONObject:legacy))
        try decoded.validate(); XCTAssertNil(decoded.draft)
        s = try await cold.updateProduction(restored,answer:q.accepted[0])
        XCTAssertEqual(s.result,.correct); XCTAssertNil(s.draft)
        try await cold.saveProductionDraft(restored,text:"遅れた入力",sequence:99)
        let activeAnswered = try await cold.activeProduction(scope:id)
        let answered = try XCTUnwrap(activeAnswered)
        XCTAssertNil(answered.draft); XCTAssertEqual(answered.answer,q.accepted[0])
        let graded = try await cold.summary(now:Date())
        XCTAssertEqual(graded.studyCount,1)
    }
}
