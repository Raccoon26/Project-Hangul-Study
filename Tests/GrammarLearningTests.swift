import XCTest
@testable import HangulStudy

final class GrammarLearningTests: XCTestCase {
    private let ids = [ContentID(rawValue:"11111111-1111-4111-8111-111111111111"),ContentID(rawValue:"22222222-2222-4222-8222-222222222222")]
    private var question: GrammarQuestion {
        GrammarQuestion(id:ContentID(rawValue:"33333333-3333-4333-8333-333333333333"),revision:1,
            prompt:"形を選ぶ",korean:"가다",explanation:"語幹に고 싶다を付けます。",
            choices:[QuizChoice(id:"right",text:"가고 싶다"),QuizChoice(id:"wrong",text:"가다 싶다")],correctID:"right",purpose:"form")
    }
    private func start() -> GrammarSession {
        let now=Date(timeIntervalSince1970:100)
        return GrammarSession(id:UUID(),lessonID:ids[0],ids:ids,contentVersion:8,seed:41,startedAt:now,updatedAt:now,order:ids)
    }
    private func study(_ initial: GrammarSession, known: Bool, correct: Bool = true) throws -> GrammarSession {
        var s=try GrammarLearning.apply(.expose([question]),to:initial)
        for _ in 0..<3 { s=try GrammarLearning.apply(.next,to:s) }
        s=try GrammarLearning.apply(.answer(correct ? "right" : "wrong"),to:s)
        s=try GrammarLearning.apply(.next,to:s)
        return try GrammarLearning.apply(.decide(known),to:s)
    }
    func testOnlyDeferredGrammarReturnsAndSetFinishes() throws {
        var s=try study(start(),known:false,correct:false)
        s=try study(s,known:true)
        XCTAssertEqual(s.deferred,[ids[0]])
        XCTAssertTrue(s.nextRound)
        s=try GrammarLearning.apply(.nextRound,to:s)
        XCTAssertEqual(s.order,[ids[0]])
        s=try study(s,known:true)
        XCTAssertTrue(s.completed);XCTAssertEqual(s.round,2)
        XCTAssertEqual(s.exposures,3);XCTAssertEqual(s.correctCount,2);XCTAssertEqual(s.wrongCount,1)
    }
    func testAllKnownAllUnknownAndDeterministicShuffle() throws {
        let known=try study(study(start(),known:true),known:true)
        XCTAssertTrue(known.completed)
        let unknown=try study(study(start(),known:false),known:false)
        let a=try GrammarLearning.apply(.nextRound,to:unknown)
        let b=try GrammarLearning.apply(.nextRound,to:unknown)
        XCTAssertEqual(a.order,b.order);XCTAssertEqual(Set(a.order),Set(ids))
        XCTAssertNotEqual(a.order.first,unknown.order.last)
    }
    func testQuestionGateJudgeAndSnapshotResume() throws {
        var s=start()
        XCTAssertThrowsError(try GrammarLearning.apply(.decide(true),to:s))
        s=try GrammarLearning.apply(.expose([question]),to:s)
        XCTAssertThrowsError(try GrammarLearning.apply(.answer("right"),to:s))
        for _ in 0..<3 { s=try GrammarLearning.apply(.next,to:s) }
        XCTAssertThrowsError(try GrammarLearning.apply(.next,to:s))
        XCTAssertThrowsError(try GrammarLearning.apply(.answer("unknown"),to:s))
        s=try GrammarLearning.apply(.answer("wrong"),to:s)
        let restored=try JSONDecoder().decode(GrammarSession.self,from:JSONEncoder().encode(s))
        XCTAssertEqual(restored,s);XCTAssertEqual(restored.selected,"wrong")
        XCTAssertFalse(question.isCorrect("wrong"));XCTAssertTrue(question.isCorrect("right"))
        XCTAssertThrowsError(try GrammarLearning.apply(.answer("right"),to:restored))
    }
    func testCorruptEmptyAndDuplicateStatesRejected() throws {
        var s=start();s.order=[ids[0],ids[0]];XCTAssertThrowsError(try s.validate())
        s=start();s.page=3;XCTAssertThrowsError(try s.validate())
        s=start();s.deferred=[ids[1]];XCTAssertThrowsError(try s.validate())
    }
    private func repository(_ dir: URL) throws -> SQLiteProgressRepository {
        let schema=try XCTUnwrap(Bundle.main.url(forResource:"user-schema-v1",withExtension:"sql"))
        return try SQLiteProgressRepository(url:dir.appendingPathComponent("user.sqlite"),schema:String(contentsOf:schema,encoding:.utf8),datasetID:"ko-ja-core")
    }
    func testProductionGrammarRepositoryPassSRSAndColdResume() async throws {
        try await exerciseProductionLesson(level:.intro,after:-1,version:11)
    }
    func testDATA04AllNewLessonsPassResumeAndEnrollSharedSRS() async throws {
        for level in [LearningLevel.intro, .beginner] {
            for after in 1...4 {
                try await exerciseProductionLesson(level:level,after:after,version:11)
            }
        }
    }
    private func exerciseProductionLesson(level: LearningLevel, after: Int, version: Int) async throws {
        let dir=FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try FileManager.default.createDirectory(at:dir,withIntermediateDirectories:true)
        defer { try? FileManager.default.removeItem(at:dir) }
        let content=try SQLiteContentRepository(url:XCTUnwrap(Bundle.main.url(forResource:"content",withExtension:"sqlite")),allowFixture:false)
        let lessons=try await content.grammarLessons(level:level,after:after,limit:1)
        let lesson=try XCTUnwrap(lessons.first)
        let members=try await content.grammarIDs(lesson:lesson.id)
        let repo=try repository(dir)
        var s=try await repo.beginGrammar(lesson:lesson.id,ids:members,contentVersion:version,restart:false)
        while let id=s.currentID {
            let card=try await content.grammarCard(id:id)
            XCTAssertFalse(card.examples.isEmpty);XCTAssertFalse(card.questions.isEmpty)
            s=try await repo.updateGrammar(id:s.id,revision:s.revision,action:.expose(card.questions),contentRevision:card.revision,contentVersion:version)
            for _ in 0..<3 { s=try await repo.updateGrammar(id:s.id,revision:s.revision,action:.next,contentRevision:card.revision,contentVersion:version) }
            while let q=s.question {
                s=try await repo.updateGrammar(id:s.id,revision:s.revision,action:.answer(q.correctID),contentRevision:card.revision,contentVersion:version)
                let cold=try repository(dir)
                // A new content version and reordered candidate members cannot reset an active snapshot.
                let resumed=try await cold.beginGrammar(lesson:lesson.id,ids:Array(members.reversed()),contentVersion:version+1,restart:false)
                XCTAssertEqual(resumed,s)
                s=try await repo.updateGrammar(id:s.id,revision:s.revision,action:.next,contentRevision:card.revision,contentVersion:version)
            }
            s=try await repo.updateGrammar(id:s.id,revision:s.revision,action:.decide(true),contentRevision:card.revision,contentVersion:version)
        }
        XCTAssertTrue(s.completed)
        let cold=try repository(dir)
        let kept=try await cold.grammarSession(id:s.id);XCTAssertEqual(kept,s)
        var due=Date.distantPast
        for id in members {
            let result=try await cold.reviewState(for:id,skill:"grammar")
            let state=try XCTUnwrap(result);XCTAssertEqual(state.stage,0)
            due=max(due,state.nextReviewAt)
        }
        var review=try await cold.beginGrammarReview(now:due)
        let id=try XCTUnwrap(review.currentID), card=try await content.grammarCard(id:id)
        let prepared=try await cold.prepareGrammarReview(sessionID:review.id,contentID:id,question:card.questions[0])
        review=try await cold.exposeReview(sessionID:review.id,contentID:id,contentRevision:card.revision,contentVersion:version,now:due,timeZoneID:"Asia/Tokyo")
        do { _=try await cold.revealReview(sessionID:review.id,contentID:id,now:due);XCTFail("Cannot bypass the grammar question") } catch { }
        _=try await cold.answerGrammarReview(sessionID:review.id,contentID:id,choice:prepared.question.correctID,contentRevision:card.revision,contentVersion:version)
        _=try await cold.submitReview(sessionID:review.id,contentID:id,rating:.remembered,now:due,timeZoneID:"Asia/Tokyo")
        let advanced=try await cold.reviewState(for:id,skill:"grammar");XCTAssertEqual(advanced?.stage,1)
        let vocabulary=try await cold.reviewState(for:id,skill:"vocabulary");XCTAssertNil(vocabulary)
    }
    func testDATA09UnitsPrerequisitesNotesAndVocabularyAreReachable() async throws {
        let content=try SQLiteContentRepository(url:XCTUnwrap(Bundle.main.url(forResource:"content",withExtension:"sqlite")),allowFixture:false)
        let lessons=try await content.grammarLessons(level:.lowerIntermediate,after:-1,limit:30)
        XCTAssertEqual(lessons.count,18)
        XCTAssertEqual(Set(lessons.compactMap(\.courseTitle)).count,3)
        XCTAssertEqual(Set(lessons.compactMap(\.unitTitle)).count,6)
        var ids=Set<ContentID>()
        for lesson in lessons {
            let members=try await content.grammarIDs(lesson:lesson.id)
            XCTAssertEqual(members.count,3)
            for id in members {
                XCTAssertTrue(ids.insert(id).inserted)
                let card=try await content.grammarCard(id:id)
                XCTAssertEqual(card.questions.count,4)
                XCTAssertGreaterThanOrEqual(card.examples.compactMap(\.learningPoint).count,4)
                XCTAssertFalse(card.prerequisites.isEmpty)
                XCTAssertFalse(card.relatedWords.isEmpty)
                for word in card.relatedWords {
                    let detail=try await content.vocabularyDetail(id:word.reference.contentID)
                    if [PartOfSpeech.verb.japaneseName,PartOfSpeech.adjective.japaneseName].contains(detail.card.partOfSpeech) {
                        XCTAssertEqual(detail.conjugations.count,3)
                    } else {
                        XCTAssertTrue(detail.conjugations.isEmpty)
                    }
                    if detail.hasProductionPractice {
                        let questions=try await content.productionQuestions(id:word.reference.contentID)
                        XCTAssertFalse(questions.isEmpty)
                    }
                }
            }
        }
        XCTAssertEqual(ids.count,54)
    }
    func testDATA09LowerIntermediateGrammarSRSAndVersionedColdResume() async throws {
        try await exerciseProductionLesson(level:.lowerIntermediate,after:46,version:23)
    }
    func testGrammarSRSUsesSharedStageAndFailureRules() throws {
        var s=try StepReviewScheduler.initial(at:Date(),neededRepetition:true,timeZoneID:"Asia/Tokyo")
        s=try StepReviewScheduler.next(previous:s,result:.remembered,at:s.nextReviewAt,timeZoneID:"Asia/Tokyo")
        XCTAssertEqual(s.stage,1)
        s=try StepReviewScheduler.next(previous:s,result:.difficult,at:s.nextReviewAt,timeZoneID:"Asia/Tokyo")
        XCTAssertEqual(s.stage,0);XCTAssertEqual(s.failureCount,1)
    }
}
