import XCTest
@testable import HangulStudy

final class LookupTests: XCTestCase {
    private func content() throws -> SQLiteContentRepository {
        try SQLiteContentRepository(url:XCTUnwrap(Bundle.main.url(forResource:"content",withExtension:"sqlite")),allowFixture:false)
    }
    private func progress(_ url: URL) throws -> SQLiteProgressRepository {
        let schema = try String(contentsOf:XCTUnwrap(Bundle.main.url(forResource:"user-schema-v1",withExtension:"sql")),encoding:.utf8)
        return try SQLiteProgressRepository(url:url,schema:schema,datasetID:"ko-ja-core")
    }
    private func directory() throws -> URL {
        let p = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try FileManager.default.createDirectory(at:p,withIntermediateDirectories:true); return p
    }
    func testActualSearchRankingTypesAndEmptyInput() async throws {
        let c = try content()
        for query in ["학교","学校"," 学校 "] {
            let rows = try await c.lookup(query,offset:0)
            XCTAssertEqual(rows.first?.title,"학교"); XCTAssertEqual(rows.first?.reference.kind,.vocabulary)
        }
        let grammar = try await c.lookup("したい",offset:0)
        XCTAssertTrue(grammar.contains { $0.reference.kind == .grammar })
        for term in ["", "   ", "%", "' OR 1=1 --", String(repeating:"a",count:101)] {
            let rows = try await c.lookup(term,offset:0); XCTAssertTrue(rows.isEmpty)
        }
        let rows = try await c.lookup("학교",offset:0)
        let first = try XCTUnwrap(rows.first)
        let wrong = try await c.lookupEntry(LookupReference(contentID:first.reference.contentID,kind:.grammar))
        XCTAssertNil(wrong)
    }
    func testDetailUsesSameConjugationEngineAndOverridesAsLearning() async throws {
        let c = try content()
        for lemma in ["먹다","듣다","춥다","파랗다"] {
            let rows = try await c.lookup(lemma,offset:0)
            let entry = try XCTUnwrap(rows.first { $0.title == lemma && $0.reference.kind == .vocabulary })
            let detail = try await c.vocabularyDetail(id:entry.reference.contentID)
            XCTAssertFalse(detail.conjugations.isEmpty)
            // Production questions are authored only for a subset. Compare where supported.
            if let questions = try? await c.productionQuestions(id:entry.reference.contentID) {
                for q in questions {
                    if let form = detail.conjugations.first(where: { $0.form == q.form }) { XCTAssertEqual(form.result.form,q.generated) }
                }
            }
        }
        let nouns = try await c.lookup("학교",offset:0)
        let noun = try XCTUnwrap(nouns.first)
        let detail = try await c.vocabularyDetail(id:noun.reference.contentID)
        XCTAssertTrue(detail.conjugations.isEmpty)
    }
    func testTypedFavoriteRecentAndColdReopenDoNotCreateLearning() async throws {
        let folder = try directory(); defer { try? FileManager.default.removeItem(at:folder) }
        let c = try content(), p = try progress(folder.appendingPathComponent("user.sqlite"))
        let words = try await c.lookup("학교",offset:0), grammar = try await c.lookup("したい",offset:0)
        let refs = [try XCTUnwrap(words.first).reference,try XCTUnwrap(grammar.first { $0.reference.kind == .grammar }).reference]
        for ref in refs {
            try await p.setFavorite(ref,enabled:true); try await p.setFavorite(ref,enabled:true)
            try await p.rememberLookup(ref,now:Date())
            let state = try await p.reviewState(for:ref.contentID,skill:ref.kind.rawValue); XCTAssertNil(state)
        }
        let cold = try progress(folder.appendingPathComponent("user.sqlite"))
        let saved = try await cold.savedReferences(list:.favorites,kind:nil,offset:0,now:Date())
        XCTAssertEqual(Set(saved),Set(refs))
        let summary = try await cold.summary(now:Date()); XCTAssertEqual(summary.studyCount,0)
        try await cold.setFavorite(refs[1],enabled:false)
        let favorite = try await cold.isFavorite(refs[1]); XCTAssertFalse(favorite)
    }
    func testManualVocabularyReviewPreservesScheduleAndRoundResume() async throws {
        let folder = try directory(); defer { try? FileManager.default.removeItem(at:folder) }
        let c = try content(), p = try progress(folder.appendingPathComponent("user.sqlite"))
        let rows = try await c.lookup("먹다",offset:0); let ref = try XCTUnwrap(rows.first).reference
        let card = try await c.vocabularyCard(id:ref.contentID)
        let set = try await p.createVocabularySet(level:.intro,ids:[ref.contentID])
        var round = try await p.beginVocabularySet(set.id,contentVersion:13,restart:false)
        round = try await p.updateVocabularySession(round.id,expectedRevision:round.revision,action:.expose(revision:card.revision,contentVersion:13))
        round = try await p.updateVocabularySession(round.id,expectedRevision:round.revision,action:.reveal)
        round = try await p.updateVocabularySession(round.id,expectedRevision:round.revision,action:.decide(.known))
        let before = try await p.reviewState(for:ref.contentID,skill:"vocabulary"); XCTAssertNotNil(before)
        let s = try await p.beginLookupPractice(ids:[ref.contentID],kind:.vocabulary,now:Date())
        XCTAssertTrue(s.isPractice)
        _ = try await p.exposeReview(sessionID:s.id,contentID:ref.contentID,contentRevision:card.revision,contentVersion:13,now:Date(),timeZoneID:"Asia/Tokyo")
        _ = try await p.revealReview(sessionID:s.id,contentID:ref.contentID,now:Date())
        let cold = try progress(folder.appendingPathComponent("user.sqlite"))
        let resumed = try await cold.beginLookupPractice(ids:[ref.contentID],kind:.vocabulary,now:Date())
        XCTAssertEqual(resumed.id,s.id); XCTAssertTrue(resumed.revealed)
        let done = try await cold.submitReview(sessionID:s.id,contentID:ref.contentID,rating:.difficult,now:Date(),timeZoneID:"Asia/Tokyo")
        XCTAssertTrue(done.completed)
        _ = try await cold.submitReview(sessionID:s.id,contentID:ref.contentID,rating:.remembered,now:Date(),timeZoneID:"Asia/Tokyo")
        let after = try await cold.reviewState(for:ref.contentID,skill:"vocabulary"); XCTAssertEqual(before,after)
        let restoredRound = try await cold.vocabularySession(round.id); XCTAssertEqual(round,restoredRound)
    }
    func testGrammarPracticeUsesQuizAndDoesNotMarkCourseComplete() async throws {
        let folder = try directory(); defer { try? FileManager.default.removeItem(at:folder) }
        let c = try content(), p = try progress(folder.appendingPathComponent("user.sqlite"))
        let rows = try await c.lookup("したい",offset:0)
        let ref = try XCTUnwrap(rows.first { $0.reference.kind == .grammar }).reference
        let card = try await c.grammarCard(id:ref.contentID), q = try XCTUnwrap(card.questions.first)
        let s = try await p.beginLookupPractice(ids:[ref.contentID],kind:.grammar,now:Date())
        _ = try await p.prepareGrammarReview(sessionID:s.id,contentID:ref.contentID,question:q)
        _ = try await p.exposeReview(sessionID:s.id,contentID:ref.contentID,contentRevision:card.revision,contentVersion:13,now:Date(),timeZoneID:"Asia/Tokyo")
        _ = try await p.answerGrammarReview(sessionID:s.id,contentID:ref.contentID,choice:q.correctID,contentRevision:card.revision,contentVersion:13)
        let done = try await p.submitReview(sessionID:s.id,contentID:ref.contentID,rating:.remembered,now:Date(),timeZoneID:"Asia/Tokyo")
        XCTAssertTrue(done.completed)
        let state = try await p.reviewState(for:ref.contentID,skill:"grammar"); XCTAssertNil(state)
        let count = try await p.curriculumCounts(ids:[ref.contentID],kind:"grammar"); XCTAssertEqual(count.0,0)
    }
    @MainActor
    func testReviewRejectsDelayedActionsForAnotherCard() async throws {
        let folder = try directory(); defer { try? FileManager.default.removeItem(at:folder) }
        let c = try content(), p = try progress(folder.appendingPathComponent("user.sqlite"))
        let rows = try await c.lookup("학교",offset:0), ref = try XCTUnwrap(rows.first).reference
        let session = try await p.beginLookupPractice(ids:[ref.contentID],kind:.vocabulary,now:Date())
        let services = AppContainer(content:c,progress:p,metadata:try await c.metadata())
        let model = ReviewViewModel(services:services,practiceID:session.id)
        await model.open()
        let stale = ContentID(rawValue:UUID().uuidString)
        await model.reveal(expectedID:stale); XCTAssertEqual(model.session?.revealed,false)
        await model.reveal(expectedID:ref.contentID); XCTAssertEqual(model.session?.revealed,true)
        await model.rate(.remembered,expectedID:stale); XCTAssertEqual(model.session?.completed,false)
        await model.rate(.remembered,expectedID:ref.contentID); XCTAssertEqual(model.session?.completed,true)
        let state = try await p.reviewState(for:ref.contentID,skill:"vocabulary"); XCTAssertNil(state)
    }

}
