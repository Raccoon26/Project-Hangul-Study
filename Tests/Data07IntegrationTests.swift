import XCTest
@testable import HangulStudy
final class Data07IntegrationTests: XCTestCase {
    func testDATA07NewWordsRoundColdResumeAndSRS() async throws {
        let content = try SQLiteContentRepository(url:XCTUnwrap(Bundle.main.url(forResource:"content",withExtension:"sqlite")),allowFixture:false)
        let ids = [ContentID(rawValue:"894354d2-a19a-4a42-8449-a2e46c917fe6"),ContentID(rawValue:"4d881879-29a0-4997-bd6a-26a0215a2fde")]
        let folder = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try FileManager.default.createDirectory(at:folder,withIntermediateDirectories:true)
        defer { try? FileManager.default.removeItem(at:folder) }
        let schema = try String(contentsOf:XCTUnwrap(Bundle.main.url(forResource:"user-schema-v1",withExtension:"sql")),encoding:.utf8)
        let url = folder.appendingPathComponent("user.sqlite")
        let repo = try SQLiteProgressRepository(url:url,schema:schema,datasetID:"ko-ja-core")
        let set = try await repo.createVocabularySet(level:.lowerIntermediate,ids:ids)
        var pass = try await repo.beginVocabularySet(set.id,contentVersion:14,restart:false)
        let first = try XCTUnwrap(pass.currentID)
        let card = try await content.vocabularyCard(id:first)
        XCTAssertFalse(card.meanings.isEmpty)
        XCTAssertNotNil(card.meanings.first?.example)
        XCTAssertTrue(AudioPolicy.permitsTTS(card.audio))
        pass = try await repo.updateVocabularySession(pass.id,expectedRevision:pass.revision,action:.expose(revision:card.revision,contentVersion:14))
        pass = try await repo.updateVocabularySession(pass.id,expectedRevision:pass.revision,action:.reveal)
        let cold = try SQLiteProgressRepository(url:url,schema:schema,datasetID:"ko-ja-core")
        let restored = try await cold.beginVocabularySet(set.id,contentVersion:15,restart:false)
        XCTAssertEqual(restored,pass)
        pass = try await cold.updateVocabularySession(pass.id,expectedRevision:pass.revision,action:.decide(.learn))
        while let id = pass.currentID {
            let c = try await content.vocabularyCard(id:id)
            pass = try await cold.updateVocabularySession(pass.id,expectedRevision:pass.revision,action:.expose(revision:c.revision,contentVersion:14))
            pass = try await cold.updateVocabularySession(pass.id,expectedRevision:pass.revision,action:.reveal)
            pass = try await cold.updateVocabularySession(pass.id,expectedRevision:pass.revision,action:.decide(.known))
        }
        pass = try await cold.updateVocabularySession(pass.id,expectedRevision:pass.revision,action:.nextRound)
        XCTAssertEqual(pass.order,[first])
        pass = try await cold.updateVocabularySession(pass.id,expectedRevision:pass.revision,action:.expose(revision:card.revision,contentVersion:14))
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
        review = try await cold.exposeReview(sessionID:review.id,contentID:reviewedID,contentRevision:reviewCard.revision,contentVersion:14,now:due,timeZoneID:"Asia/Tokyo")
        review = try await cold.revealReview(sessionID:review.id,contentID:reviewedID,now:due)
        _ = try await cold.submitReview(sessionID:review.id,contentID:reviewedID,rating:.remembered,now:due,timeZoneID:"Asia/Tokyo")
        _ = try await cold.submitReview(sessionID:review.id,contentID:reviewedID,rating:.remembered,now:due,timeZoneID:"Asia/Tokyo")
        let reopen = try SQLiteProgressRepository(url:url,schema:schema,datasetID:"ko-ja-core")
        let after = try await reopen.reviewState(for:reviewedID,skill:"vocabulary")
        XCTAssertEqual(after?.reviewCount,1);XCTAssertEqual(after?.stage,1)
        let savedPass = try await reopen.vocabularySession(pass.id)
        XCTAssertEqual(savedPass,pass)
    }
    func testActualNewConjugationsAndInputGrading() async throws {
        let content = try SQLiteContentRepository(url:XCTUnwrap(Bundle.main.url(forResource:"content",withExtension:"sqlite")),allowFixture:false)
        do {
            let id = ContentID(rawValue:"bb6c3b0f-5d4c-4a96-a923-c039ab75731c")
            let questions = try await content.productionQuestions(id:id)
            let q = try XCTUnwrap(questions.first)
            XCTAssertEqual(q.generated,"잠가요")
            XCTAssertEqual(ProductionAnswer.judge(q.generated,accepted:q.accepted,spacingWarning:q.spacingWarning),.correct)
            let detail = try await content.vocabularyDetail(id:id)
            XCTAssertFalse(detail.conjugations.isEmpty)
        }
        do {
            let id = ContentID(rawValue:"875ad319-df01-454f-a1a2-8004ca8f0bb1")
            let questions = try await content.productionQuestions(id:id)
            let q = try XCTUnwrap(questions.first)
            XCTAssertEqual(q.generated,"헹궈요")
            XCTAssertEqual(ProductionAnswer.judge(q.generated,accepted:q.accepted,spacingWarning:q.spacingWarning),.correct)
            let detail = try await content.vocabularyDetail(id:id)
            XCTAssertFalse(detail.conjugations.isEmpty)
        }
        do {
            let id = ContentID(rawValue:"c1672e06-7d3a-4e1d-9160-3ac7d0625be6")
            let questions = try await content.productionQuestions(id:id)
            let q = try XCTUnwrap(questions.first)
            XCTAssertEqual(q.generated,"부어요")
            XCTAssertEqual(ProductionAnswer.judge(q.generated,accepted:q.accepted,spacingWarning:q.spacingWarning),.correct)
            let detail = try await content.vocabularyDetail(id:id)
            XCTAssertFalse(detail.conjugations.isEmpty)
        }
        do {
            let id = ContentID(rawValue:"dde26ad6-8abb-4b70-831d-676420eb5058")
            let questions = try await content.productionQuestions(id:id)
            let q = try XCTUnwrap(questions.first)
            XCTAssertEqual(q.generated,"알아들어요")
            XCTAssertEqual(ProductionAnswer.judge(q.generated,accepted:q.accepted,spacingWarning:q.spacingWarning),.correct)
            let detail = try await content.vocabularyDetail(id:id)
            XCTAssertFalse(detail.conjugations.isEmpty)
        }
        do {
            let id = ContentID(rawValue:"28213817-b996-4c2d-849c-f895446399fe")
            let questions = try await content.productionQuestions(id:id)
            let q = try XCTUnwrap(questions.first)
            XCTAssertEqual(q.generated,"되물어요")
            XCTAssertEqual(ProductionAnswer.judge(q.generated,accepted:q.accepted,spacingWarning:q.spacingWarning),.correct)
            let detail = try await content.vocabularyDetail(id:id)
            XCTAssertFalse(detail.conjugations.isEmpty)
        }
        do {
            let id = ContentID(rawValue:"ae6501d6-544c-4688-b730-76bd19fd3da7")
            let questions = try await content.productionQuestions(id:id)
            let q = try XCTUnwrap(questions.first)
            XCTAssertEqual(q.generated,"가려워요")
            XCTAssertEqual(ProductionAnswer.judge(q.generated,accepted:q.accepted,spacingWarning:q.spacingWarning),.correct)
            let detail = try await content.vocabularyDetail(id:id)
            XCTAssertFalse(detail.conjugations.isEmpty)
        }
        do {
            let id = ContentID(rawValue:"aa8931b8-1bb9-4840-b8e3-402277b03df9")
            let questions = try await content.productionQuestions(id:id)
            let q = try XCTUnwrap(questions.first)
            XCTAssertEqual(q.generated,"타올라요")
            XCTAssertEqual(ProductionAnswer.judge(q.generated,accepted:q.accepted,spacingWarning:q.spacingWarning),.correct)
            let detail = try await content.vocabularyDetail(id:id)
            XCTAssertFalse(detail.conjugations.isEmpty)
        }
        do {
            let id = ContentID(rawValue:"dd394569-5f67-41d9-8af4-2aa819651646")
            let questions = try await content.productionQuestions(id:id)
            let q = try XCTUnwrap(questions.first)
            XCTAssertEqual(q.generated,"덮어요")
            XCTAssertEqual(ProductionAnswer.judge(q.generated,accepted:q.accepted,spacingWarning:q.spacingWarning),.correct)
            let detail = try await content.vocabularyDetail(id:id)
            XCTAssertFalse(detail.conjugations.isEmpty)
        }
    }
    func testLowerIntermediateSearchAndFourRealListeningTasks() async throws {
        let content = try SQLiteContentRepository(url:XCTUnwrap(Bundle.main.url(forResource:"content",withExtension:"sqlite")),allowFixture:false)
        let count = try await content.vocabularyCount(level:.lowerIntermediate)
        XCTAssertEqual(count,1181)
        let hits = try await content.lookup("返送",offset:0)
        XCTAssertTrue(hits.contains { $0.title == "반송하다" })
        do {
            let questions = try await content.listeningQuestions(level:.beginner,ids:[ContentID(rawValue:"499a1477-6fb9-4116-a332-12698dd62d46"),ContentID(rawValue:"20ca4689-5519-4774-bf1b-a681d116a7b9")])
            XCTAssertEqual(questions.count,2)
            for q in questions {
                try q.validate()
                XCTAssertTrue(AudioPolicy.permitsTTS(q.audio))
                if q.task == .dictation {
                    XCTAssertEqual(ProductionAnswer.judge(q.transcript,accepted:q.accepted,spacingWarning:true),.correct)
                }
            }
        }
        do {
            let questions = try await content.listeningQuestions(level:.lowerIntermediate,ids:[ContentID(rawValue:"e0a86ad9-87ff-41fc-8c04-5c5ebadb2dbe"),ContentID(rawValue:"fb59f63c-9e72-49be-9a4e-40770bc3494b")])
            XCTAssertEqual(questions.count,2)
            for q in questions {
                try q.validate()
                XCTAssertTrue(AudioPolicy.permitsTTS(q.audio))
                if q.task == .dictation {
                    XCTAssertEqual(ProductionAnswer.judge(q.transcript,accepted:q.accepted,spacingWarning:true),.correct)
                }
            }
        }
    }
}
