import XCTest
@testable import HangulStudy

final class ReleaseAuditTests: XCTestCase {
    func testConjugationOeContractsToWaeAndWaeStaysWae() throws {
        // 한국어기초사전: 되어(돼), 뵈어(봬), 꿰어(꿰).
        // 꿰 + ㅆ is 뀄 (ㅞ), not 꿨 (ㅝ).
        for (lemma, present, past, reason) in [("되다","돼요","됐어요","돼서"),("뵈다","봬요","뵀어요","봬서"),("꿰다","꿰요","뀄어요","꿰서")] {
            for (form, expected) in [(ConjugationForm.present,present),(.past,past),(.reason,reason)] {
                XCTAssertEqual(try ConjugationEngine.generate(lemma:lemma,partOfSpeech:"verb",irregular:"none",form:form).form,expected)
            }
        }
    }
    func testInternalErrorsNeverReachLearningUI() {
        let secret = "/private/user.sqlite: SQLITE_CONSTRAINT"
        for error in [DatabaseError.sqlite(secret) as Error, DatabaseError.invalidData(secret), NSError(domain:secret,code:1,userInfo:[NSLocalizedDescriptionKey:secret])] {
            XCTAssertFalse(LearningErrorMessage.message(for:error).contains(secret))
            XCTAssertTrue(LearningErrorMessage.message(for:error).contains("記録"))
        }
        XCTAssertEqual(LearningErrorMessage.message(for:GrammarError.changedContent),GrammarError.changedContent.errorDescription)
    }
    func testSQLiteTextRoundTripsEmbeddedNulAndJapanese() throws {
        let url = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        defer { try? FileManager.default.removeItem(at:url) }
        let db = try SQLiteConnection(url:url,readOnly:false)
        try db.executeScript("CREATE TABLE text_test(value TEXT)")
        let text = "聞く\u{0}들어요🙂"
        try db.execute("INSERT INTO text_test VALUES(?)",[.text(text)])
        XCTAssertEqual(try db.query("SELECT value FROM text_test").first?.text("value"),text)
    }
    func testWrongDatasetDoesNotMigrateExistingFile() throws {
        let dir = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try FileManager.default.createDirectory(at:dir,withIntermediateDirectories:true)
        defer { try? FileManager.default.removeItem(at:dir) }
        let url = dir.appendingPathComponent("user.sqlite")
        let schema = try String(contentsOf:XCTUnwrap(Bundle.main.url(forResource:"user-schema-v1",withExtension:"sql")),encoding:.utf8)
        let db = try SQLiteConnection(url:url,readOnly:false)
        try db.executeScript(schema)
        try db.execute("INSERT INTO user_metadata VALUES('dataset_id','other')")
        XCTAssertThrowsError(try SQLiteProgressRepository(url:url,schema:schema,datasetID:"ko-ja-core"))
        XCTAssertEqual(try db.query("PRAGMA user_version").first?.integer("user_version"),1)
        XCTAssertEqual(try FileManager.default.contentsOfDirectory(at:dir,includingPropertiesForKeys:nil).filter { $0.pathExtension == "backup" }.count,0)
    }
    func testInvalidDateCannotCreateStudyDay() {
        XCTAssertThrowsError(try StudyDay.key(for:Date(timeIntervalSince1970:.infinity),timeZoneID:"Asia/Tokyo"))
    }
    func testProductionResumeSnapshotAndRetryAreIndependentOfContentUpdate() async throws {
        let content = try SQLiteContentRepository(url:XCTUnwrap(Bundle.main.url(forResource:"content",withExtension:"sqlite")),allowFixture:false)
        let entries = try await content.productionVocabulary(after:"")
        let entry = try XCTUnwrap(entries.first)
        let questions = try await content.productionQuestions(id:entry.0)
        let q = try XCTUnwrap(questions.first)
        let dir = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try FileManager.default.createDirectory(at:dir,withIntermediateDirectories:true)
        defer { try? FileManager.default.removeItem(at:dir) }
        let url = dir.appendingPathComponent("user.sqlite")
        let schema = try String(contentsOf:XCTUnwrap(Bundle.main.url(forResource:"user-schema-v1",withExtension:"sql")),encoding:.utf8)
        let repo = try SQLiteProgressRepository(url:url,schema:schema,datasetID:"ko-ja-core")
        var s = try await repo.beginProduction(scope:entry.0,questions:[q],version:13)
        s = try await repo.updateProduction(s,answer:nil)
        s = try await repo.updateProduction(s,answer:"誤答")
        let cold = try SQLiteProgressRepository(url:url,schema:schema,datasetID:"ko-ja-core")
        let restored = try await cold.activeProduction(scope:entry.0)
        XCTAssertEqual(restored?.id,s.id); XCTAssertEqual(restored?.answer,"誤答")
        XCTAssertEqual(restored?.retry,[0])
        let stale = s
        s = try await cold.updateProduction(s,answer:nil)
        do { _ = try await cold.updateProduction(stale,answer:nil); XCTFail("Must reject stale action") } catch { }
        s = try await cold.updateProduction(s,answer:q.accepted[0])
        s = try await cold.updateProduction(s,answer:nil)
        XCTAssertTrue(s.completed)
        let stats = try await cold.statistics(now:Date(),timeZone:TimeZone(identifier:"Asia/Tokyo")!)
        XCTAssertEqual(stats.windows.first?.productionWrong,1)
        XCTAssertEqual(stats.windows.first?.productionCorrect,0)
        let state = try await cold.reviewState(for:entry.0,skill:"vocabulary")
        XCTAssertEqual(state?.reviewCount,0)
    }
    @MainActor
    private func checkUnavailableReviewRecovery(kind: String) async throws {
        let folder = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try FileManager.default.createDirectory(at:folder,withIntermediateDirectories:true)
        defer { try? FileManager.default.removeItem(at:folder) }
        let contentURL = folder.appendingPathComponent("content.sqlite")
        try FileManager.default.copyItem(at:XCTUnwrap(Bundle.main.url(forResource:"content",withExtension:"sqlite")),to:contentURL)
        let contentDB = try SQLiteConnection(url:contentURL,readOnly:false)
        let ids = try contentDB.query("SELECT id FROM content_items WHERE kind=? AND is_active=1 ORDER BY id LIMIT 2",[.text(kind)]).map { ContentID(rawValue:try $0.text("id")) }
        XCTAssertEqual(ids.count,2)
        try contentDB.execute("UPDATE content_items SET is_active=0 WHERE id=?",[.text(ids[0].rawValue)])
        let content = try SQLiteContentRepository(url:contentURL,allowFixture:false)
        let userURL = folder.appendingPathComponent("user.sqlite")
        let schema = try String(contentsOf:XCTUnwrap(Bundle.main.url(forResource:"user-schema-v1",withExtension:"sql")),encoding:.utf8)
        let repo = try SQLiteProgressRepository(url:userURL,schema:schema,datasetID:"ko-ja-core")
        let db = try SQLiteConnection(url:userURL,readOnly:false), now = Date()
        let previous = try StepReviewScheduler.initial(at:now.addingTimeInterval(-86400*3),neededRepetition:false,timeZoneID:"Asia/Tokyo")
        let json = String(decoding:try JSONEncoder().encode(previous),as:UTF8.self)
        for id in ids {
            try db.execute("INSERT INTO srs_state VALUES(?,?,'calendar_steps',1,?,?,NULL,1)",[.text(id.rawValue),.text(kind),.text(json),.real(previous.nextReviewAt.timeIntervalSince1970)])
        }
        try await repo.setFavorite(LookupReference(contentID:ids[0],kind:kind == "vocabulary" ? .vocabulary : .grammar),enabled:true)
        let services = AppContainer(content:content,progress:repo,metadata:try await content.metadata())
        let result: ReviewSession
        if kind == "vocabulary" {
            let model = ReviewViewModel(services:services)
            await model.open(); XCTAssertEqual(model.unavailableID,ids[0])
            await model.deferUnavailable(expectedID:ids[0])
            XCTAssertEqual(model.card?.id,ids[1])
            await model.reveal(expectedID:ids[1]); await model.rate(.remembered,expectedID:ids[1])
            result = try XCTUnwrap(model.session)
        } else {
            let model = GrammarReviewViewModel(services:services)
            await model.open(); XCTAssertEqual(model.unavailableID,ids[0])
            await model.deferUnavailable(expectedID:ids[0])
            let question = try XCTUnwrap(model.question?.question)
            await model.answer(question.correctID,expectedQuestionID:question.id)
            await model.rate(.remembered,expectedQuestionID:question.id)
            result = try XCTUnwrap(model.session)
        }
        XCTAssertTrue(result.completed); XCTAssertEqual(result.completedCount,1); XCTAssertEqual(result.deferredCount,1)
        XCTAssertEqual(result.ids,ids)
        let saved = try await repo.reviewState(for:ids[0],skill:kind)
        XCTAssertEqual(saved,previous)
        let favorites = try await repo.favoriteIDs(); XCTAssertTrue(favorites.contains(ids[0]))
        XCTAssertEqual(try db.query("SELECT COUNT(*) AS n FROM study_events WHERE content_id=?",[.text(ids[0].rawValue)]).first?.integer("n"),0)
        let cold = try SQLiteProgressRepository(url:userURL,schema:schema,datasetID:"ko-ja-core")
        let restored = try await cold.reviewSession(result.id)
        XCTAssertEqual(restored.deferredCount,1); XCTAssertTrue(restored.completed)
    }
    @MainActor
    func testDATA08UnavailableVocabularyReviewContinuesWithoutLosingProgress() async throws {
        try await checkUnavailableReviewRecovery(kind:"vocabulary")
    }
    @MainActor
    func testDATA08UnavailableGrammarReviewContinuesWithoutLosingProgress() async throws {
        try await checkUnavailableReviewRecovery(kind:"grammar")
    }

}
