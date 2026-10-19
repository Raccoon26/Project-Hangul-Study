import XCTest
@testable import HangulStudy

final class SRSTests: XCTestCase {
    private let zone = "Asia/Tokyo"
    private func date(_ value: String) throws -> Date { try XCTUnwrap(ISO8601DateFormatter().date(from: value)) }
    private func initial(_ value: String = "2026-10-01T12:00:00Z") throws -> SRSState {
        try StepReviewScheduler.initial(at: date(value), neededRepetition: false, timeZoneID: zone)
    }
    func testInitialKnownWordIsLowStageAndDueTomorrow() throws {
        let state = try initial()
        XCTAssertEqual(state.stage, 0); XCTAssertEqual(state.reviewCount, 0)
        XCTAssertNil(state.lastResult); XCTAssertNil(state.lastReviewedAt)
        XCTAssertEqual(state.nextReviewAt, try date("2026-10-01T15:00:00Z"))
        let repeated = try StepReviewScheduler.initial(at: state.firstLearnedAt, neededRepetition: true, timeZoneID: zone)
        XCTAssertTrue(repeated.neededRepetition); XCTAssertEqual(repeated.stage, 0)
    }
    func testRememberedAdvancesAndCapsAtMaintenanceWithoutRemoval() throws {
        var state = try initial()
        for index in 1...10 {
            let reviewed = state.nextReviewAt
            state = try StepReviewScheduler.next(previous: state, result: .remembered, at: reviewed, timeZoneID: zone)
            XCTAssertEqual(state.stage, min(index, 6))
            XCTAssertEqual(state.reviewCount, index)
            XCTAssertGreaterThan(state.nextReviewAt, reviewed)
        }
        XCTAssertEqual(state.consecutiveSuccesses, 10)
        let calendar = try StepReviewScheduler.calendar(timeZoneID: zone)
        XCTAssertEqual(calendar.dateComponents([.day], from: try XCTUnwrap(state.lastReviewedAt), to: state.nextReviewAt).day, 120)
    }
    func testUnsureKeepsStageButLimitsIntervalToThreeDays() throws {
        var state = try initial(); state.stage = 5
        let now = try date("2026-10-05T12:00:00Z")
        let next = try StepReviewScheduler.next(previous: state, result: .unsure, at: now, timeZoneID: zone)
        XCTAssertEqual(next.stage, 5); XCTAssertEqual(next.consecutiveSuccesses, 0)
        XCTAssertEqual(next.nextReviewAt, try date("2026-10-07T15:00:00Z"))
        XCTAssertEqual(next.lastResult, .unsure)
    }
    func testDifficultResetsAndCannotRepeatOnSameLocalDate() throws {
        var state = try initial(); state.stage = 6
        let now = try date("2026-10-05T12:00:00Z")
        let next = try StepReviewScheduler.next(previous: state, result: .difficult, at: now, timeZoneID: zone)
        XCTAssertEqual(next.stage, 0); XCTAssertEqual(next.failureCount, 1)
        XCTAssertEqual(next.nextReviewAt, try date("2026-10-05T15:00:00Z"))
        XCTAssertEqual(next.reviewCount, 1)
    }
    func testMidnightChangesCalendarDayNotFixedTwentyFourHours() throws {
        let before = try initial("2026-10-01T14:59:59Z")
        let after = try initial("2026-10-01T15:00:00Z")
        XCTAssertEqual(before.nextReviewAt, try date("2026-10-01T15:00:00Z"))
        XCTAssertEqual(after.nextReviewAt, try date("2026-10-02T15:00:00Z"))
    }
    func testDSTUsesCalendarDays() throws {
        let spring = try StepReviewScheduler.initial(at: date("2026-03-08T05:00:00Z"), neededRepetition: false, timeZoneID: "America/New_York")
        XCTAssertEqual(spring.nextReviewAt, try date("2026-03-09T04:00:00Z"))
        XCTAssertEqual(spring.nextReviewAt.timeIntervalSince(spring.firstLearnedAt), 23 * 3600)
        let autumn = try StepReviewScheduler.initial(at: date("2026-11-01T04:00:00Z"), neededRepetition: false, timeZoneID: "America/New_York")
        XCTAssertEqual(autumn.nextReviewAt.timeIntervalSince(autumn.firstLearnedAt), 25 * 3600)
    }
    func testTravelPreservesAbsoluteExistingDueAndUsesNewZoneForNextSchedule() throws {
        let previous = try initial()
        let encoded = try JSONEncoder().encode(previous)
        let restored = try JSONDecoder().decode(SRSState.self, from: encoded)
        XCTAssertEqual(restored, previous)
        let next = try StepReviewScheduler.next(previous: restored, result: .difficult,
            at: date("2026-10-03T12:00:00Z"), timeZoneID: "America/Los_Angeles")
        XCTAssertEqual(next.nextReviewAt, try date("2026-10-04T07:00:00Z"))
        XCTAssertEqual(next.schedulingTimeZone, "America/Los_Angeles")
    }
    func testInvalidZoneAndCorruptStateAreRejected() throws {
        XCTAssertThrowsError(try StepReviewScheduler.initial(at: Date(), neededRepetition: false, timeZoneID: "invalid"))
        var state = try initial(); state.stage = 99
        XCTAssertThrowsError(try StepReviewScheduler.next(previous: state, result: .remembered, at: Date(), timeZoneID: zone))
    }

    private var directory: URL!
    override func setUpWithError() throws {
        directory = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try FileManager.default.createDirectory(at: directory, withIntermediateDirectories: true)
    }
    override func tearDownWithError() throws { try FileManager.default.removeItem(at: directory) }
    private func repository() throws -> SQLiteProgressRepository {
        let schema = try XCTUnwrap(Bundle.main.url(forResource: "user-schema-v1", withExtension: "sql"))
        return try SQLiteProgressRepository(url: directory.appendingPathComponent("user.sqlite"), schema: String(contentsOf: schema, encoding: .utf8), datasetID: "ko-ja-core")
    }
    private func completeSet(_ repo: SQLiteProgressRepository, count: Int = 2) async throws -> VocabularySession {
        let ids = (0..<count).map { _ in ContentID(rawValue: UUID().uuidString.lowercased()) }
        let set = try await repo.createVocabularySet(level: .intro, ids: ids)
        var state = try await repo.beginVocabularySet(set.id, contentVersion: 5, restart: false)
        for _ in ids {
            state = try await repo.updateVocabularySession(state.id, expectedRevision: state.revision, action: .expose(revision: 1, contentVersion: 5))
            state = try await repo.updateVocabularySession(state.id, expectedRevision: state.revision, action: .reveal)
            state = try await repo.updateVocabularySession(state.id, expectedRevision: state.revision, action: .decide(.known))
        }
        return state
    }
    func testPassCompletionEnrollsInitiallyKnownWordsAndRepeatDoesNotReset() async throws {
        let repo = try repository()
        let pass = try await completeSet(repo)
        for id in pass.vocabularyIDs {
            let state = try await repo.reviewState(for: id, skill: "vocabulary")
            XCTAssertEqual(state?.stage, 0); XCTAssertEqual(state?.reviewCount, 0)
        }
        let id = try XCTUnwrap(pass.vocabularyIDs.first)
        let before = try await repo.reviewState(for: id, skill: "vocabulary")
        try await repo.backfillVocabularyReviews(timeZoneID: zone)
        let after = try await repo.reviewState(for: id, skill: "vocabulary")
        XCTAssertEqual(before, after)
        XCTAssertTrue(pass.completed)
    }
    func testSecondPassCompletionPreservesAdvancedReviewSchedule() async throws {
        let repo = try repository(), pass = try await completeSet(repo, count: 1)
        let id = pass.vocabularyIDs[0]
        let initialValue = try await repo.reviewState(for: id, skill: "vocabulary")
        let due = try XCTUnwrap(initialValue).nextReviewAt
        var review = try await repo.beginReview(now: due, limit: 20)
        review = try await repo.exposeReview(sessionID: review.id, contentID: id, contentRevision: 1, contentVersion: 5, now: due, timeZoneID: zone)
        review = try await repo.revealReview(sessionID: review.id, contentID: id, now: due)
        _ = try await repo.submitReview(sessionID: review.id, contentID: id, rating: .remembered, now: due, timeZoneID: zone)
        let advanced = try await repo.reviewState(for: id, skill: "vocabulary")
        var again = try await repo.beginVocabularySet(pass.setID, contentVersion: 6, restart: true)
        again = try await repo.updateVocabularySession(again.id, expectedRevision: again.revision, action: .expose(revision: 1, contentVersion: 6))
        again = try await repo.updateVocabularySession(again.id, expectedRevision: again.revision, action: .reveal)
        _ = try await repo.updateVocabularySession(again.id, expectedRevision: again.revision, action: .decide(.known))
        let after = try await repo.reviewState(for: id, skill: "vocabulary")
        XCTAssertEqual(advanced, after)
        XCTAssertEqual(after?.stage, 1)
    }
    func testNeededRepetitionIsRecordedForFutureInitialPolicy() async throws {
        let repo = try repository()
        let id = ContentID(rawValue: UUID().uuidString.lowercased())
        let set = try await repo.createVocabularySet(level: .intro, ids: [id])
        var pass = try await repo.beginVocabularySet(set.id, contentVersion: 5, restart: false)
        for decision in [VocabularyDecision.learn, .known] {
            pass = try await repo.updateVocabularySession(pass.id, expectedRevision: pass.revision, action: .expose(revision: 1, contentVersion: 5))
            pass = try await repo.updateVocabularySession(pass.id, expectedRevision: pass.revision, action: .reveal)
            pass = try await repo.updateVocabularySession(pass.id, expectedRevision: pass.revision, action: .decide(decision))
            if !pass.completed { pass = try await repo.updateVocabularySession(pass.id, expectedRevision: pass.revision, action: .nextRound) }
        }
        let state = try await repo.reviewState(for: id, skill: "vocabulary")
        XCTAssertEqual(state?.neededRepetition, true)
        XCTAssertEqual(state?.stage, 0)
    }
    func testClockRewindDoesNotSilentlyRewriteHistory() throws {
        var state = try initial()
        state = try StepReviewScheduler.next(previous: state, result: .remembered, at: state.nextReviewAt, timeZoneID: zone)
        XCTAssertThrowsError(try StepReviewScheduler.next(previous: state, result: .unsure,
            at: try XCTUnwrap(state.lastReviewedAt).addingTimeInterval(-1), timeZoneID: zone))
    }
    func testDueBoundaryAndFutureExcluded() async throws {
        let repo = try repository(), pass = try await completeSet(repo, count: 1)
        let maybeState = try await repo.reviewState(for: pass.vocabularyIDs[0], skill: "vocabulary")
        let state = try XCTUnwrap(maybeState)
        let before = try await repo.reviewSummary(now: state.nextReviewAt.addingTimeInterval(-1), timeZoneID: zone)
        let due = try await repo.reviewSummary(now: state.nextReviewAt, timeZoneID: zone)
        XCTAssertEqual(before.due, 0); XCTAssertEqual(due.due, 1)
    }
    func testRevealGateResumeRatingIdempotencyAndStatePersistence() async throws {
        let repo = try repository(), pass = try await completeSet(repo)
        let maybeState = try await repo.reviewState(for: pass.vocabularyIDs[0], skill: "vocabulary")
        let state = try XCTUnwrap(maybeState)
        let now = state.nextReviewAt.addingTimeInterval(3600)
        var session = try await repo.beginReview(now: now, limit: 20)
        let first = try XCTUnwrap(session.currentID)
        do { _ = try await repo.submitReview(sessionID: session.id, contentID: first, rating: .remembered, now: now, timeZoneID: zone); XCTFail("Unrevealed review accepted") }
        catch { XCTAssertEqual(error as? ReviewError, .staleCard) }
        session = try await repo.exposeReview(sessionID: session.id, contentID: first, contentRevision: 1, contentVersion: 5, now: now, timeZoneID: zone)
        session = try await repo.revealReview(sessionID: session.id, contentID: first, now: now)
        let reopened = try repository()
        let resumed = try await reopened.beginReview(now: now.addingTimeInterval(86400 * 4), limit: 20)
        XCTAssertEqual(resumed.id, session.id); XCTAssertEqual(resumed.currentID, first)
        XCTAssertTrue(resumed.revealed)
        let answered = try await reopened.submitReview(sessionID: resumed.id, contentID: first, rating: .difficult, now: now, timeZoneID: zone)
        XCTAssertNotEqual(answered.currentID, first)
        _ = try await reopened.submitReview(sessionID: resumed.id, contentID: first, rating: .remembered, now: now, timeZoneID: zone)
        let saved = try await reopened.reviewState(for: first, skill: "vocabulary")
        XCTAssertEqual(saved?.reviewCount, 1); XCTAssertEqual(saved?.lastResult, .difficult)
        let summary = try await reopened.reviewSummary(now: now, timeZoneID: zone)
        XCTAssertEqual(summary.completedToday, 1); XCTAssertEqual(summary.due, 1)
        let restoredPass = try await reopened.vocabularySession(pass.id)
        XCTAssertEqual(restoredPass, pass)
    }
    func testBacklogLimitedWithoutDroppingUnstartedDueItems() async throws {
        let repo = try repository()
        _ = try await completeSet(repo, count: 25)
        _ = try await completeSet(repo, count: 25)
        let now = Date().addingTimeInterval(86400 * 10)
        let summary = try await repo.reviewSummary(now: now, timeZoneID: zone)
        XCTAssertEqual(summary.due, 50); XCTAssertEqual(summary.overdue, 50)
        let session = try await repo.beginReview(now: now, limit: 20)
        XCTAssertEqual(session.ids.count, 20)
        let after = try await repo.reviewSummary(now: now, timeZoneID: zone)
        XCTAssertEqual(after.due, 50)
    }
    func testLegacyCompletedPassBackfillIsIdempotent() async throws {
        let repo = try repository(), pass = try await completeSet(repo)
        let db = try SQLiteConnection(url: directory.appendingPathComponent("user.sqlite"), readOnly: false)
        try db.transaction {
            try db.execute("DELETE FROM srs_enrolled_passes")
            try db.execute("DELETE FROM srs_state")
        }
        try await repo.backfillVocabularyReviews(timeZoneID: zone)
        try await repo.backfillVocabularyReviews(timeZoneID: zone)
        let count = try db.query("SELECT COUNT(*) AS n FROM srs_state").first?.integer("n")
        XCTAssertEqual(count, pass.vocabularyIDs.count)
        let saved = try await repo.reviewState(for: pass.vocabularyIDs[0], skill: "vocabulary")
        XCTAssertEqual(saved?.firstLearnedAt, pass.completedAt)
    }
    func testDATA08DeferredReviewsPreserveSchedulesAndRetryAfterContentUpdate() async throws {
        let schema = try String(contentsOf:XCTUnwrap(Bundle.main.url(forResource:"user-schema-v1",withExtension:"sql")),encoding:.utf8)
        for storedSkill in ["vocabulary","grammar","vocabulary_practice","grammar_practice"] {
            let folder = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
            try FileManager.default.createDirectory(at:folder,withIntermediateDirectories:true)
            defer { try? FileManager.default.removeItem(at:folder) }
            let url = folder.appendingPathComponent("user.sqlite")
            let repo = try SQLiteProgressRepository(url:url,schema:schema,datasetID:"ko-ja-core")
            let db = try SQLiteConnection(url:url,readOnly:false)
            let kind = storedSkill.replacingOccurrences(of:"_practice",with:"")
            let ids = [ContentID(rawValue:UUID().uuidString),ContentID(rawValue:UUID().uuidString)]
            let id = UUID(), now = Date()
            let state = try StepReviewScheduler.initial(at:now.addingTimeInterval(-86400*3),neededRepetition:false,timeZoneID:zone)
            let json = String(decoding:try JSONEncoder().encode(state),as:UTF8.self)
            try db.execute("INSERT INTO review_sessions VALUES(?,?,'active',1,1,NULL)",[.text(id.uuidString),.text(storedSkill)])
            for (n,word) in ids.enumerated() {
                try db.execute("INSERT INTO review_items(session_id,content_id,ordinal) VALUES(?,?,?)",[.text(id.uuidString),.text(word.rawValue),.integer(Int64(n))])
                try db.execute("INSERT INTO srs_state VALUES(?,?,'calendar_steps',1,?,?,NULL,1)",[.text(word.rawValue),.text(kind),.text(json),.real(state.nextReviewAt.timeIntervalSince1970)])
            }
            try await repo.configureReviewContentVersion(19)
            var session = try await repo.deferUnavailableReview(sessionID:id,contentID:ids[0],contentVersion:19,now:now)
            XCTAssertEqual(session.ids,ids); XCTAssertEqual(session.currentID,ids[1])
            let duplicate = try await repo.deferUnavailableReview(sessionID:id,contentID:ids[0],contentVersion:19,now:now)
            XCTAssertEqual(duplicate.deferredCount,1); XCTAssertEqual(duplicate.currentID,ids[1])
            session = try await repo.deferUnavailableReview(sessionID:id,contentID:ids[1],contentVersion:19,now:now)
            XCTAssertTrue(session.completed); XCTAssertEqual(session.completedCount,0); XCTAssertEqual(session.deferredCount,2)
            let cold = try SQLiteProgressRepository(url:url,schema:schema,datasetID:"ko-ja-core")
            let restored = try await cold.reviewSession(id)
            XCTAssertEqual(restored.ids,ids); XCTAssertTrue(restored.completed); XCTAssertEqual(restored.deferredCount,2)
            for word in ids {
                let saved = try await cold.reviewState(for:word,skill:kind)
                XCTAssertEqual(saved,state)
            }
            let before: ReviewSummary
            if kind == "vocabulary" { before = try await cold.reviewSummary(now:now,timeZoneID:zone) }
            else { before = try await cold.grammarReviewSummary(now:now) }
            XCTAssertEqual(before.due,0)
            try await cold.configureReviewContentVersion(20)
            let after: ReviewSummary
            if kind == "vocabulary" { after = try await cold.reviewSummary(now:now,timeZoneID:zone) }
            else { after = try await cold.grammarReviewSummary(now:now) }
            XCTAssertEqual(after.due,2)
            XCTAssertEqual(try db.query("SELECT COUNT(*) AS n FROM study_events").first?.integer("n"),0)
            XCTAssertEqual(try db.query("SELECT COUNT(result) AS n FROM review_items").first?.integer("n"),0)
        }
    }

}
