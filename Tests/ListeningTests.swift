import XCTest
@testable import HangulStudy

final class ListeningTests: XCTestCase {
    private func question(_ task: ListeningTask = .dictation) -> ListeningQuestion {
        ListeningQuestion(id:ContentID(rawValue:UUID().uuidString),itemID:ContentID(rawValue:UUID().uuidString),revision:1,sourceID:ContentID(rawValue:UUID().uuidString),level:.intro,task:task,prompt:"聞いて答えてください",transcript:"물을 마셔요.",translation:"水を飲みます。",explanation:"물は水です。",choices:task == .dictation ? [] : [QuizChoice(id:"a",text:"水を飲みます。"),QuizChoice(id:"b",text:"ご飯を食べます。")],correctID:task == .dictation ? nil : "a",accepted:task == .dictation ? ["물을 마셔요.","물을 마셔요"] : [],recordingRequired:false,recording:nil)
    }
    private func session(_ questions: [ListeningQuestion]) -> ListeningSession {
        ListeningSession(id:UUID(),scope:"test",questions:questions,contentVersion:10,isReview:false,startedAt:Date(),updatedAt:Date())
    }
    func testAllChoiceTasksAndDictationReuse() throws {
        for task in [ListeningTask.meaning,.korean,.comprehension] {
            let q = question(task); try q.validate()
            XCTAssertEqual(q.judge("a"),.correct); XCTAssertEqual(q.judge("b"),.incorrect)
            XCTAssertEqual(q.judge("missing"),.incorrect)
        }
        let q = question()
        XCTAssertEqual(q.judge("  물을   마셔요\n"),.correct)
        XCTAssertEqual(q.judge("물을마셔요"),.spacing)
        XCTAssertEqual(q.judge("무를 마셔요"),.incorrect)
        XCTAssertEqual(q.judge("물을 마셔오"),.incorrect)
        XCTAssertEqual(q.judge("  "),.incorrect)
        XCTAssertEqual(q.judge("물을 마셔요."),.correct)
    }
    func testPlaybackGateAndBoundedRetry() throws {
        var s = session([question(),question(),question()])
        XCTAssertThrowsError(try s.apply(.submit("물을 마셔요"),at:Date()))
        try s.apply(.played(.slow),at:Date())
        try s.apply(.submit("틀려요"),at:Date())
        XCTAssertEqual(s.retry,[0]); XCTAssertEqual(s.slowCount,1)
        XCTAssertThrowsError(try s.apply(.submit("물을 마셔요"),at:Date()))
        try s.apply(.next,at:Date())
        for _ in 0..<2 {
            XCTAssertFalse(s.heard)
            try s.apply(.played(.normal),at:Date())
            try s.apply(.submit("물을 마셔요"),at:Date())
            try s.apply(.next,at:Date())
        }
        XCTAssertTrue(s.retrying); XCTAssertEqual(s.position,0)
        try s.apply(.played(.normal),at:Date())
        try s.apply(.submit("또 틀려요"),at:Date())
        try s.apply(.next,at:Date())
        XCTAssertTrue(s.completed); XCTAssertEqual(s.correct,2); XCTAssertEqual(s.wrong,1)
        XCTAssertThrowsError(try s.apply(.next,at:Date()))
    }
    func testAllWrongAndRetrySuccessAreNotFirstPassMastery() throws {
        var s = session((0..<12).map { _ in question() })
        for _ in 0..<12 {
            try s.apply(.played(.normal),at:Date()); try s.apply(.submit("wrong"),at:Date()); try s.apply(.next,at:Date())
        }
        for _ in 0..<12 {
            try s.apply(.played(.normal),at:Date()); try s.apply(.submit("물을 마셔요"),at:Date()); try s.apply(.next,at:Date())
        }
        XCTAssertTrue(s.completed); XCTAssertEqual(s.correct,0); XCTAssertEqual(s.wrong,12); XCTAssertEqual(s.retrySuccess,12)
    }
    func testListeningRatingsUseSharedSchedulingAndNeverGraduateRetry() throws {
        let date = Date(timeIntervalSince1970:2_000_000_000)
        var state = try StepReviewScheduler.initial(at:date,neededRepetition:true,timeZoneID:"Asia/Tokyo")
        for _ in 0..<3 { state = try StepReviewScheduler.next(previous:state,result:.remembered,at:state.nextReviewAt,timeZoneID:"Asia/Tokyo") }
        XCTAssertEqual(state.stage,3)
        let unsure = try StepReviewScheduler.next(previous:state,result:.unsure,at:state.nextReviewAt,timeZoneID:"America/Los_Angeles")
        XCTAssertEqual(unsure.stage,3)
        let failed = try StepReviewScheduler.next(previous:state,result:.difficult,at:state.nextReviewAt,timeZoneID:"Asia/Tokyo")
        XCTAssertEqual(failed.stage,0); XCTAssertEqual(failed.failureCount,1)
    }
    func testSnapshotKeepsFeedbackQueueAndDeterministicOptions() throws {
        var s = session([question(.meaning),question()])
        try s.apply(.played(.normal),at:Date()); try s.apply(.submit("b"),at:Date())
        let restored = try JSONDecoder().decode(ListeningSession.self,from:JSONEncoder().encode(s))
        try restored.validate()
        XCTAssertEqual(restored.answer,"b"); XCTAssertEqual(restored.retry,[0]); XCTAssertEqual(restored.result,.incorrect)
        let q = s.questions[0]
        XCTAssertEqual(QuizOptions.ordered(q.choices,seed:42,contentID:q.id),QuizOptions.ordered(q.choices,seed:42,contentID:q.id))
    }
    func testRealContentDiskResumeAndSRS() async throws {
        let url = try XCTUnwrap(Bundle.main.url(forResource:"content",withExtension:"sqlite"))
        let content = try SQLiteContentRepository(url:url,allowFixture:false)
        let intro = try await content.listeningQuestions(level:.intro,ids:nil)
        let beginner = try await content.listeningQuestions(level:.beginner,ids:nil)
        XCTAssertEqual(intro.count,20); XCTAssertEqual(beginner.count,20)
        XCTAssertTrue(intro.allSatisfy { $0.level == .intro })
        XCTAssertEqual(Set((intro+beginner).map(\.task.rawValue)),Set(["meaning","korean","dictation","comprehension"]))
        let folder = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try FileManager.default.createDirectory(at:folder,withIntermediateDirectories:true)
        defer { try? FileManager.default.removeItem(at:folder) }
        let schema = try String(contentsOf:XCTUnwrap(Bundle.main.url(forResource:"user-schema-v1",withExtension:"sql")),encoding:.utf8)
        let userURL = folder.appendingPathComponent("user.sqlite")
        let repo = try SQLiteProgressRepository(url:userURL,schema:schema,datasetID:"ko-ja-core")
        var s = try await repo.beginListening(scope:"practice:intro",questions:intro,version:10,review:false)
        let q = try XCTUnwrap(s.current)
        s = try await repo.updateListening(s,action:.played(.slow),now:Date())
        let previous = s
        let correct = q.correctID ?? q.accepted[0]
        s = try await repo.updateListening(s,action:.submit(correct),now:Date())
        do { _ = try await repo.updateListening(previous,action:.submit(correct),now:Date()); XCTFail("stale answer accepted") } catch {}
        let cold = try SQLiteProgressRepository(url:userURL,schema:schema,datasetID:"ko-ja-core")
        let restored = try await cold.beginListening(scope:"practice:intro",questions:Array(beginner.reversed()),version:11,review:false)
        XCTAssertEqual(restored.id,s.id); XCTAssertEqual(restored.answer,s.answer); XCTAssertEqual(restored.questions.map(\.id),s.questions.map(\.id))
        let loadedState = try await cold.reviewState(for:q.itemID,skill:"listening")
        let initial = try XCTUnwrap(loadedState)
        XCTAssertEqual(initial.stage,0)
        let due = try await cold.listeningDue(now:initial.nextReviewAt)
        XCTAssertTrue(due.1.contains(q.itemID))
        let futureQuestions = try await content.listeningQuestions(level:nil,ids:due.1)
        var review = try await cold.beginListening(scope:"review",questions:futureQuestions,version:10,review:true)
        review = try await cold.updateListening(review,action:.played(.normal),now:initial.nextReviewAt)
        review = try await cold.updateListening(review,action:.submit(correct),now:initial.nextReviewAt)
        let advanced = try await cold.reviewState(for:q.itemID,skill:"listening")
        XCTAssertEqual(advanced?.stage,1); XCTAssertEqual(advanced?.reviewCount,1)
    }

    func testData06RealItemsGradingAndAudioPolicy() async throws {
        let url = try XCTUnwrap(Bundle.main.url(forResource:"content",withExtension:"sqlite"))
        let content = try SQLiteContentRepository(url:url,allowFixture:false)
        var all: [ListeningQuestion] = []
        for level in [LearningLevel.intro,.beginner] {
            let batches = try await content.listeningBatches(level:level,after:2)
            for (batch, _) in batches {
                let ids = try await content.listeningBatchIDs(level:level,batch:batch)
                let questions = try await content.listeningQuestions(level:level,ids:ids)
                XCTAssertLessThanOrEqual(questions.count,20)
                all += questions
            }
        }
        XCTAssertEqual(all.count,80)
        for task in [ListeningTask.meaning,.korean,.dictation,.comprehension] {
            XCTAssertEqual(all.filter { $0.task == task }.count,20)
        }
        for q in all {
            try q.validate()
            XCTAssertTrue(AudioPolicy.permitsTTS(q.audio))
            XCTAssertEqual(q.audio.text,q.transcript)
            if q.task == .dictation {
                XCTAssertEqual(q.judge(q.transcript),.correct)
                XCTAssertEqual(q.judge("  " + q.transcript.replacingOccurrences(of:" ",with:"   ") + "\n"),.correct)
                XCTAssertEqual(q.judge(q.transcript.decomposedStringWithCanonicalMapping),.correct)
                XCTAssertEqual(q.judge(q.transcript.replacingOccurrences(of:" ",with:"")),.spacing)
                XCTAssertEqual(q.judge(""),.incorrect)
                XCTAssertEqual(q.judge(q.transcript + "가"),.incorrect)
            } else {
                for choice in q.choices {
                    XCTAssertEqual(q.judge(choice.id),choice.id == q.correctID ? .correct : .incorrect)
                }
            }
        }
    }

    func testData06ProductionRetryColdResumeAndNoDoubleSRS() async throws {
        let content = try SQLiteContentRepository(url:XCTUnwrap(Bundle.main.url(forResource:"content",withExtension:"sqlite")),allowFixture:false)
        let ids = try await content.listeningBatchIDs(level:.beginner,batch:3)
        let questions = try await content.listeningQuestions(level:.beginner,ids:ids)
        XCTAssertEqual(questions.count,20)
        let folder = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try FileManager.default.createDirectory(at:folder,withIntermediateDirectories:true)
        defer { try? FileManager.default.removeItem(at:folder) }
        let schema = try String(contentsOf:XCTUnwrap(Bundle.main.url(forResource:"user-schema-v1",withExtension:"sql")),encoding:.utf8)
        let path = folder.appendingPathComponent("user.sqlite")
        let repo = try SQLiteProgressRepository(url:path,schema:schema,datasetID:"ko-ja-core")
        var s = try await repo.beginListening(scope:"practice:beginner:3",questions:questions,version:13,review:false)
        for _ in 0..<20 {
            let q = try XCTUnwrap(s.current)
            s = try await repo.updateListening(s,action:.played(.normal),now:Date())
            let stale = s
            let wrong = q.task == .dictation ? "다른 문장" : try XCTUnwrap(q.choices.first { $0.id != q.correctID }).id
            s = try await repo.updateListening(s,action:.submit(wrong),now:Date())
            do { _ = try await repo.updateListening(stale,action:.submit(wrong),now:Date()); XCTFail("duplicate accepted") } catch {}
            s = try await repo.updateListening(s,action:.next,now:Date())
        }
        XCTAssertTrue(s.retrying); XCTAssertEqual(s.wrong,20)
        let cold = try SQLiteProgressRepository(url:path,schema:schema,datasetID:"ko-ja-core")
        let restored = try await cold.beginListening(scope:"practice:beginner:3",questions:Array(questions.reversed()),version:14,review:false)
        XCTAssertEqual(restored.id,s.id); XCTAssertEqual(restored.retry,s.retry)
        XCTAssertEqual(restored.position,s.position); XCTAssertEqual(restored.questions.map(\.id),s.questions.map(\.id))
        s = restored
        for _ in 0..<20 {
            let q = try XCTUnwrap(s.current)
            let before = try await cold.reviewState(for:q.itemID,skill:"listening")
            s = try await cold.updateListening(s,action:.played(.slow),now:Date())
            s = try await cold.updateListening(s,action:.submit(q.correctID ?? q.transcript),now:Date())
            let after = try await cold.reviewState(for:q.itemID,skill:"listening")
            XCTAssertEqual(after?.stage,before?.stage)
            XCTAssertEqual(after?.nextReviewAt,before?.nextReviewAt)
            XCTAssertEqual(after?.reviewCount,before?.reviewCount)
            s = try await cold.updateListening(s,action:.next,now:Date())
        }
        XCTAssertTrue(s.completed); XCTAssertEqual(s.correct,0)
        XCTAssertEqual(s.wrong,20); XCTAssertEqual(s.retrySuccess,20)
        let active = try await cold.activeListening(scope:"practice:beginner:3")
        XCTAssertNil(active)
    }
    func testDATA08AllLowerIntermediateDictationBatchesAndAnswers() async throws {
        let content = try SQLiteContentRepository(url:XCTUnwrap(Bundle.main.url(forResource:"content",withExtension:"sqlite")),allowFixture:false)
        var after = -1
        var ids = Set<ContentID>()
        var newCount = 0
        while true {
            let batches = try await content.listeningBatches(level:.lowerIntermediate,after:after)
            if batches.isEmpty { break }
            for (batch,count) in batches {
                let batchIDs = try await content.listeningBatchIDs(level:.lowerIntermediate,batch:batch)
                let questions = try await content.listeningQuestions(level:.lowerIntermediate,ids:batchIDs)
                XCTAssertEqual(questions.count,count)
                XCTAssertLessThanOrEqual(count,20)
                for q in questions {
                    try q.validate()
                    XCTAssertTrue(ids.insert(q.itemID).inserted)
                    // Frozen DATA08 cohort ends at batch102; DATA10 adds other task types afterward.
                    if (11...102).contains(batch) {
                        XCTAssertEqual(q.task,.dictation)
                        XCTAssertEqual(q.judge(q.transcript),.correct)
                        XCTAssertTrue(AudioPolicy.permitsTTS(q.audio))
                        newCount += 1
                    }
                }
            }
            after = try XCTUnwrap(batches.last).0
        }
        XCTAssertEqual(ids.count,1943)
        XCTAssertEqual(newCount,1821)
    }

    func testDATA08AllDictationsAllowTerminalPunctuationOmissionOnly() async throws {
        XCTAssertEqual(ProductionAnswer.judgeDictation("물을 마셔요",accepted:["물을 마셔요."]),.correct)
        XCTAssertEqual(ProductionAnswer.judgeDictation("물을마셔요",accepted:["물을 마셔요."]),.spacing)
        XCTAssertEqual(ProductionAnswer.judgeDictation("물을 마셔오",accepted:["물을 마셔요."]),.incorrect)
        XCTAssertEqual(ProductionAnswer.judgeDictation(".물을 마셔요",accepted:["물을 마셔요."]),.incorrect)
        XCTAssertEqual(ProductionAnswer.judgeDictation("물을, 마셔요",accepted:["물을 마셔요."]),.incorrect)
        XCTAssertEqual(ProductionAnswer.judge("물을 마셔요",accepted:["물을 마셔요."],spacingWarning:true),.incorrect)
        let content = try SQLiteContentRepository(url:XCTUnwrap(Bundle.main.url(forResource:"content",withExtension:"sqlite")),allowFixture:false)
        var checked = 0
        for level in [LearningLevel.intro,.beginner,.lowerIntermediate] {
            var after = -1
            while true {
                let batches = try await content.listeningBatches(level:level,after:after)
                if batches.isEmpty { break }
                for (batch,_) in batches {
                    let ids = try await content.listeningBatchIDs(level:level,batch:batch)
                    let questions = try await content.listeningQuestions(level:level,ids:ids)
                    for q in questions where q.task == .dictation {
                        var answer = q.transcript
                        while let last = answer.last, ".!?".contains(last) { answer.removeLast() }
                        XCTAssertEqual(q.judge(answer),.correct)
                        checked += 1
                    }
                }
                after = try XCTUnwrap(batches.last).0
            }
        }
        XCTAssertEqual(checked,1880)
    }

    func testDATA08UnavailableListeningDueIsReleaseScopedAndPreservesSnapshots() async throws {
        let contentURL = try XCTUnwrap(Bundle.main.url(forResource:"content",withExtension:"sqlite"))
        let contentDB = try SQLiteConnection(url:contentURL,readOnly:true)
        let ids = try contentDB.query("SELECT id FROM listening_items ORDER BY id LIMIT 45").map { ContentID(rawValue:try $0.text("id")) }
        let folder = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try FileManager.default.createDirectory(at:folder,withIntermediateDirectories:true)
        defer { try? FileManager.default.removeItem(at:folder) }
        let schema = try String(contentsOf:XCTUnwrap(Bundle.main.url(forResource:"user-schema-v1",withExtension:"sql")),encoding:.utf8)
        let repo = try SQLiteProgressRepository(url:folder.appendingPathComponent("user.sqlite"),schema:schema,datasetID:"ko-ja-core")
        let db = try SQLiteConnection(url:folder.appendingPathComponent("user.sqlite"),readOnly:false)
        let now = Date(), state = try StepReviewScheduler.initial(at:Date().addingTimeInterval(-86400*3),neededRepetition:false,timeZoneID:"Asia/Tokyo")
        let json = String(decoding:try JSONEncoder().encode(state),as:UTF8.self)
        for id in ids { try db.execute("INSERT INTO srs_state VALUES(?,'listening','calendar_steps',1,?,?,NULL,1)",[.text(id.rawValue),.text(json),.real(state.nextReviewAt.timeIntervalSince1970)]) }
        try await repo.configureReviewContentVersion(19)
        try await repo.deferUnavailableListening(ids:Array(ids.prefix(20)),contentVersion:19)
        try await repo.deferUnavailableListening(ids:Array(ids[20..<25]),contentVersion:19)
        let due = try await repo.listeningDue(now:now)
        XCTAssertEqual(due.0,20); XCTAssertEqual(due.1,Array(ids.suffix(20)))
        let content = try SQLiteContentRepository(url:contentURL,allowFixture:false)
        let questions = try await content.listeningQuestions(level:nil,ids:due.1)
        let session = try await repo.beginListening(scope:"review",questions:questions,version:19,review:true)
        try await repo.configureReviewContentVersion(20)
        let after = try await repo.listeningDue(now:now)
        XCTAssertEqual(after.0,45)
        let saved = try await repo.activeListening(scope:"review")
        XCTAssertEqual(saved?.questions.map(\.id),session.questions.map(\.id))
        XCTAssertEqual(saved?.contentVersion,19)
        XCTAssertEqual(try db.query("SELECT COUNT(*) AS n FROM srs_state WHERE state_json=?",[.text(json)]).first?.integer("n"),45)
    }

    func testDATA10ABatchAll120QuestionsUseRealFourTaskGrading() async throws {
        let content = try SQLiteContentRepository(url:XCTUnwrap(Bundle.main.url(forResource:"content",withExtension:"sqlite")),allowFixture:false)
        var tasks = [String:Int](), sources = [ContentID:Int](), seen = Set<ContentID>()
        for batch in 103...108 {
            let ids = try await content.listeningBatchIDs(level:.lowerIntermediate,batch:batch)
            let questions = try await content.listeningQuestions(level:.lowerIntermediate,ids:ids)
            XCTAssertEqual(questions.count,20)
            XCTAssertEqual(Set(questions.map(\.sourceID)).count,20)
            for q in questions {
                try q.validate()
                XCTAssertTrue(seen.insert(q.itemID).inserted)
                tasks[q.task.rawValue,default:0] += 1
                sources[q.sourceID,default:0] += 1
                XCTAssertFalse(q.recordingRequired)
                XCTAssertNil(q.recording)
                XCTAssertTrue(AudioPolicy.permitsTTS(q.audio))
                XCTAssertEqual(q.level,.lowerIntermediate)
                if q.task == .dictation {
                    XCTAssertEqual(q.accepted,[q.transcript])
                    XCTAssertEqual(q.judge(q.transcript),.correct)
                    var omitted = q.transcript
                    while let last = omitted.last, ".!?".contains(last) { omitted.removeLast() }
                    XCTAssertEqual(q.judge(omitted),.correct)
                    XCTAssertEqual(q.judge(q.transcript.replacingOccurrences(of:" ",with:"")),.spacing)
                    if let boundary = q.transcript.firstIndex(where:{ ".!?".contains($0) }) {
                        var changed = q.transcript
                        changed.replaceSubrange(boundary...boundary,with:",")
                        XCTAssertEqual(q.judge(changed),.incorrect)
                    }
                } else {
                    XCTAssertEqual(q.choices.count,3)
                    let correct = try XCTUnwrap(q.correctID)
                    XCTAssertEqual(q.judge(correct),.correct)
                    for c in q.choices where c.id != correct { XCTAssertEqual(q.judge(c.id),.incorrect) }
                    let text = try XCTUnwrap(q.choices.first(where:{$0.id == correct})).text
                    if q.task == .meaning { XCTAssertEqual(text,q.translation) }
                    if q.task == .korean { XCTAssertEqual(text,q.transcript) }
                }
                var state = session([q])
                let answer: String
                if q.task == .dictation { answer = q.transcript }
                else { answer = try XCTUnwrap(q.correctID) }
                XCTAssertThrowsError(try state.apply(.submit(answer),at:Date()))
                try state.apply(.played(.normal),at:Date())
                try state.apply(.submit(answer),at:Date())
                XCTAssertEqual(state.result,.correct)
                try state.apply(.next,at:Date())
                XCTAssertTrue(state.completed)
            }
        }
        XCTAssertEqual(seen.count,120)
        XCTAssertEqual(sources.count,60)
        XCTAssertTrue(sources.values.allSatisfy({$0 == 2}))
        XCTAssertEqual(tasks,["comprehension":60,"dictation":30,"meaning":18,"korean":12])
    }

}
