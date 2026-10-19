import XCTest
@testable import HangulStudy
final class ProductionLearningTests: XCTestCase {
    private func allProductionEntries(_ content: SQLiteContentRepository) async throws -> [(ContentID,String)] {
        var entries: [(ContentID,String)] = []
        var after = ""
        while true {
            let page = try await content.productionVocabulary(after:after)
            guard let last = page.last else { return entries }
            XCTAssertLessThanOrEqual(page.count,30)
            entries.append(contentsOf:page)
            after = last.0.rawValue
        }
    }
    private func form(_ lemma:String,_ irregular:String = "none",_ target:ConjugationForm = .present,_ pos:String = "verb") throws -> String {
        try ConjugationEngine.generate(lemma:lemma,partOfSpeech:pos,irregular:irregular,form:target).form
    }
    func testRegularAndContractions() throws {
        for (lemma,expected) in [("가다","가요"),("먹다","먹어요"),("보다","봐요"),("오다","와요"),("주다","줘요"),("마시다","마셔요"),("크다","커요"),("쓰다","써요"),("켜다","켜요"),("따르다","따라요")] { XCTAssertEqual(try form(lemma),expected) }
        XCTAssertEqual(try form("공부하다","other"),"공부해요")
        XCTAssertEqual(try form("보다","none",.past),"봤어요")
        XCTAssertEqual(try form("공부하다","other",.past),"공부했어요")
    }
    func testIrregularsAndRegularCounterexamples() throws {
        for (lemma,kind,expected) in [("어렵다","b","어려워요"),("걷다","d","걸어요"),("모르다","reu","몰라요"),("낫다","s","나아요"),("받다","none","받아요"),("입다","none","입어요"),("웃다","none","웃어요"),("좋다","none","좋아요")] { XCTAssertEqual(try form(lemma,kind),expected) }
        XCTAssertEqual(try form("걷다","d",.condition),"걸으면")
        XCTAssertEqual(try form("걷다","d",.future),"걸을 거예요")
        XCTAssertEqual(try form("듣다","d",.condition),"들으면")
        XCTAssertEqual(try form("묻다","d",.future),"물을 거예요")
        XCTAssertEqual(try form("어렵다","b",.future),"어려울 거예요")
        XCTAssertEqual(try form("낫다","s",.future),"나을 거예요")
        XCTAssertEqual(try form("살다","none",.condition),"살면")
        XCTAssertEqual(try form("살다","none",.future),"살 거예요")
    }
    func testAllTargetFormsAndRestrictions() throws {
        let expected:[ConjugationForm:String] = [.present:"먹어요",.past:"먹었어요",.future:"먹을 거예요",.negativeShort:"안 먹어요",.negativeLong:"먹지 않아요",.wish:"먹고 싶어요",.connective:"먹고",.reason:"먹어서",.condition:"먹으면"]
        for (target,value) in expected { XCTAssertEqual(try form("먹다","none",target),value) }
        XCTAssertThrowsError(try form("좋다","none",.wish,"adjective"))
        XCTAssertThrowsError(try form("공부하다","other",.negativeShort))
        XCTAssertThrowsError(try form("푸다"))
        XCTAssertThrowsError(try form("어떻다","h"))
        XCTAssertEqual(try ConjugationEngine.generate(lemma:"어떻다",partOfSpeech:"adjective",irregular:"h",form:.present,overrides:["present":"어때요"]).form,"어때요")
    }
    func testDATA08BatchAReviewedMetadataAndConjugations() async throws {
        let content = try SQLiteContentRepository(url:XCTUnwrap(Bundle.main.url(forResource:"content",withExtension:"sqlite")),allowFixture:false)
        for (lemma,pos,expected) in [("들르다","verb","들러요"),("서투르다","adjective","서툴러요"),("어지르다","verb","어질러요"),("너그럽다","adjective","너그러워요"),("맞추다","verb","맞춰요"),("맞히다","verb","맞혀요")] {
            let found = try await content.vocabulary(matching:VocabularyQuery(level:.lowerIntermediate,prefix:lemma),after:nil,limit:10)
            let word = try XCTUnwrap(found.first(where: { $0.headword == lemma }))
            XCTAssertEqual(word.partOfSpeech,try XCTUnwrap(PartOfSpeech(rawValue:pos)).japaneseName)
            let generated = try ConjugationEngine.generate(lemma:word.headword,partOfSpeech:pos,irregular:word.irregularType,form:.present)
            XCTAssertEqual(generated.form,expected)
            let card = try await content.vocabularyCard(id:word.id)
            XCTAssertFalse(card.meanings.isEmpty)
        }
    }
    func testInputNormalizationAndSpacing() {
        XCTAssertEqual(ProductionAnswer.judge("  먹어요\n",accepted:["먹어요"],spacingWarning:true),.correct)
        XCTAssertEqual(ProductionAnswer.judge("먹을   거예요",accepted:["먹을 거예요"],spacingWarning:true),.correct)
        XCTAssertEqual(ProductionAnswer.judge("먹을거예요",accepted:["먹을 거예요"],spacingWarning:true),.spacing)
        XCTAssertEqual(ProductionAnswer.judge("먹을거예요",accepted:["먹을 거예요"],spacingWarning:false),.incorrect)
        XCTAssertEqual(ProductionAnswer.judge("보아요",accepted:["봐요","보아요"],spacingWarning:true),.correct)
        XCTAssertEqual(ProductionAnswer.judge("먹어오",accepted:["먹어요"],spacingWarning:true),.incorrect)
        XCTAssertEqual(ProductionAnswer.judge("  ",accepted:["먹어요"],spacingWarning:true),.incorrect)
    }
    func testActualProductionQuestionsAndSavedRetry() async throws {
        let url=try XCTUnwrap(Bundle.main.url(forResource:"content",withExtension:"sqlite"))
        let content=try SQLiteContentRepository(url:url,allowFixture:false)
        let entries=try await allProductionEntries(content)
        XCTAssertEqual(entries.count,31)
        for entry in entries {
            let questions=try await content.productionQuestions(id:entry.0)
            XCTAssertFalse(questions.isEmpty)
            XCTAssertTrue(questions.allSatisfy { !$0.generated.isEmpty })
        }
        let first=try XCTUnwrap(entries.first)
        let questions=try await content.productionQuestions(id:first.0)
        let dir=FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try FileManager.default.createDirectory(at:dir,withIntermediateDirectories:true)
        defer { try? FileManager.default.removeItem(at:dir) }
        let schema=try String(contentsOf:XCTUnwrap(Bundle.main.url(forResource:"user-schema-v1",withExtension:"sql")),encoding:.utf8)
        let repo=try SQLiteProgressRepository(url:dir.appendingPathComponent("user.sqlite"),schema:schema,datasetID:"ko-ja-core")
        var s=try await repo.beginProduction(scope:first.0,questions:questions,version:9)
        s=try await repo.updateProduction(s,answer:nil)
        s=try await repo.updateProduction(s,answer:"違う答え")
        XCTAssertEqual(s.result,.incorrect);XCTAssertEqual(s.retry,[0])
        let cold=try SQLiteProgressRepository(url:dir.appendingPathComponent("user.sqlite"),schema:schema,datasetID:"ko-ja-core")
        let restored=try await cold.beginProduction(scope:first.0,questions:Array(questions.reversed()),version:10)
        XCTAssertEqual(restored.answer,s.answer);XCTAssertEqual(restored.questions.map(\.id),s.questions.map(\.id))
        s=try await repo.updateProduction(s,answer:nil)
        var iterations=0
        while let q=s.current {
            if s.studying { s=try await repo.updateProduction(s,answer:nil) }
            s=try await repo.updateProduction(s,answer:q.accepted[0])
            s=try await repo.updateProduction(s,answer:nil)
            iterations+=1;XCTAssertLessThan(iterations,30)
        }
        XCTAssertTrue(s.completed)
        let state=try await repo.reviewState(for:first.0,skill:"vocabulary");XCTAssertNotNil(state)
    }
    func testDATA04GrammarLinksGenerateAcceptedForms() async throws {
        let content=try SQLiteContentRepository(url:XCTUnwrap(Bundle.main.url(forResource:"content",withExtension:"sqlite")),allowFixture:false)
        let targets: Set<String> = ["f635b8cc-1c6a-415e-96cc-a450a8ff357f","f331886b-4670-4a73-a700-b0f0f036b1a4","1734a471-0e5b-4500-956c-dfa22926d2e9","19d5aacf-8e98-451e-affa-737a71b4d748","b8314a89-448e-4d2e-8aea-1fb8625311ce"]
        var seen=Set<String>()
        let entries=try await allProductionEntries(content)
        for entry in entries {
            let questions=try await content.productionQuestions(id:entry.0)
            for q in questions {
                guard let grammar=q.grammarID, targets.contains(grammar.rawValue) else { continue }
                let card=try await content.grammarCard(id:grammar)
                XCTAssertFalse(card.examples.isEmpty)
                XCTAssertEqual(ProductionAnswer.judge(q.generated,accepted:q.accepted,spacingWarning:q.spacingWarning),.correct)
                seen.insert(grammar.rawValue)
            }
        }
        XCTAssertEqual(seen,targets)
    }


    func testDATA05RealVocabularyPassColdResumeAndReview() async throws {
        let content = try SQLiteContentRepository(url:XCTUnwrap(Bundle.main.url(forResource:"content",withExtension:"sqlite")),allowFixture:false)
        let ids = [ContentID(rawValue:"16db0578-bf0b-4db5-aea2-35c2a326a2a8"),ContentID(rawValue:"2eb45a9a-b91c-4e4c-8c49-710cd60a81e2")]
        let folder = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try FileManager.default.createDirectory(at:folder,withIntermediateDirectories:true)
        defer { try? FileManager.default.removeItem(at:folder) }
        let schema = try String(contentsOf:XCTUnwrap(Bundle.main.url(forResource:"user-schema-v1",withExtension:"sql")),encoding:.utf8)
        let url = folder.appendingPathComponent("user.sqlite")
        let repo = try SQLiteProgressRepository(url:url,schema:schema,datasetID:"ko-ja-core")
        let set = try await repo.createVocabularySet(level:.beginner,ids:ids)
        var pass = try await repo.beginVocabularySet(set.id,contentVersion:12,restart:false)
        let first = try XCTUnwrap(pass.currentID)
        let card = try await content.vocabularyCard(id:first)
        XCTAssertFalse(card.meanings.isEmpty)
        XCTAssertNotNil(card.meanings.first?.example)
        XCTAssertTrue(AudioPolicy.permitsTTS(card.audio))
        pass = try await repo.updateVocabularySession(pass.id,expectedRevision:pass.revision,action:.expose(revision:card.revision,contentVersion:12))
        pass = try await repo.updateVocabularySession(pass.id,expectedRevision:pass.revision,action:.reveal)
        let cold = try SQLiteProgressRepository(url:url,schema:schema,datasetID:"ko-ja-core")
        let restored = try await cold.beginVocabularySet(set.id,contentVersion:13,restart:false)
        XCTAssertEqual(restored,pass)
        pass = try await cold.updateVocabularySession(pass.id,expectedRevision:pass.revision,action:.decide(.learn))
        while let id = pass.currentID {
            let c = try await content.vocabularyCard(id:id)
            pass = try await cold.updateVocabularySession(pass.id,expectedRevision:pass.revision,action:.expose(revision:c.revision,contentVersion:12))
            pass = try await cold.updateVocabularySession(pass.id,expectedRevision:pass.revision,action:.reveal)
            pass = try await cold.updateVocabularySession(pass.id,expectedRevision:pass.revision,action:.decide(.known))
        }
        pass = try await cold.updateVocabularySession(pass.id,expectedRevision:pass.revision,action:.nextRound)
        XCTAssertEqual(pass.order,[first])
        pass = try await cold.updateVocabularySession(pass.id,expectedRevision:pass.revision,action:.expose(revision:card.revision,contentVersion:12))
        pass = try await cold.updateVocabularySession(pass.id,expectedRevision:pass.revision,action:.reveal)
        pass = try await cold.updateVocabularySession(pass.id,expectedRevision:pass.revision,action:.decide(.known))
        XCTAssertTrue(pass.completed)
        for id in ids {
            let state = try await cold.reviewState(for:id,skill:"vocabulary")
            XCTAssertNotNil(state);XCTAssertEqual(state?.stage,0)
        }
        let state = try await cold.reviewState(for:first,skill:"vocabulary")
        let due = try XCTUnwrap(state).nextReviewAt.addingTimeInterval(60)
        var review = try await cold.beginReview(now:due)
        let reviewedID = try XCTUnwrap(review.currentID)
        let reviewCard = try await content.vocabularyCard(id:reviewedID)
        review = try await cold.exposeReview(sessionID:review.id,contentID:reviewedID,contentRevision:reviewCard.revision,contentVersion:12,now:due,timeZoneID:"Asia/Tokyo")
        review = try await cold.revealReview(sessionID:review.id,contentID:reviewedID,now:due)
        _ = try await cold.submitReview(sessionID:review.id,contentID:reviewedID,rating:.remembered,now:due,timeZoneID:"Asia/Tokyo")
        _ = try await cold.submitReview(sessionID:review.id,contentID:reviewedID,rating:.remembered,now:due,timeZoneID:"Asia/Tokyo")
        let reopen = try SQLiteProgressRepository(url:url,schema:schema,datasetID:"ko-ja-core")
        let after = try await reopen.reviewState(for:reviewedID,skill:"vocabulary")
        XCTAssertEqual(after?.reviewCount,1);XCTAssertEqual(after?.stage,1)
        let savedPass = try await reopen.vocabularySession(pass.id)
        XCTAssertEqual(savedPass,pass)
    }
    func testDATA05ListeningSourceColdResumeAndDueRegistration() async throws {
        let content = try SQLiteContentRepository(url:XCTUnwrap(Bundle.main.url(forResource:"content",withExtension:"sqlite")),allowFixture:false)
        // Preserve the DATA05 cohort; batch 2 later gained DATA06 items.
        let ids = [ContentID(rawValue:"ad718366-2ef8-464a-8f18-7cf0253f76b8"),ContentID(rawValue:"ca6e2de8-4257-4f3c-b2f0-de4b475d9642"),ContentID(rawValue:"2e921b48-691a-4d4e-8113-09751373d569"),ContentID(rawValue:"343a416b-70a5-444a-b25b-9584e6cf9515")]
        XCTAssertEqual(ids.count,4)
        let questions = try await content.listeningQuestions(level:.beginner,ids:ids)
        XCTAssertEqual(questions.count,4)
        for q in questions { try q.validate();XCTAssertTrue(AudioPolicy.permitsTTS(q.audio)) }
        let q = try XCTUnwrap(questions.first(where: { $0.task == .dictation }))
        let folder = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try FileManager.default.createDirectory(at:folder,withIntermediateDirectories:true)
        defer { try? FileManager.default.removeItem(at:folder) }
        let schema = try String(contentsOf:XCTUnwrap(Bundle.main.url(forResource:"user-schema-v1",withExtension:"sql")),encoding:.utf8)
        let url = folder.appendingPathComponent("user.sqlite")
        let repo = try SQLiteProgressRepository(url:url,schema:schema,datasetID:"ko-ja-core")
        var session = try await repo.beginListening(scope:"data05",questions:[q],version:12,review:false)
        session = try await repo.updateListening(session,action:.played(.normal),now:Date())
        let cold = try SQLiteProgressRepository(url:url,schema:schema,datasetID:"ko-ja-core")
        let resumed = try await cold.beginListening(scope:"data05",questions:questions,version:13,review:false)
        XCTAssertEqual(resumed.id,session.id);XCTAssertTrue(resumed.heard)
        session = try await cold.updateListening(resumed,action:.submit(q.transcript),now:Date())
        XCTAssertEqual(session.result,.correct)
        session = try await cold.updateListening(session,action:.next,now:Date())
        XCTAssertTrue(session.completed)
        let state = try await cold.reviewState(for:q.itemID,skill:"listening")
        let due = try XCTUnwrap(state).nextReviewAt
        let found = try await cold.listeningDue(now:due)
        XCTAssertTrue(found.1.contains(q.itemID))
        let vocabulary = try await cold.reviewState(for:q.itemID,skill:"vocabulary")
        XCTAssertNil(vocabulary)
    }
}
