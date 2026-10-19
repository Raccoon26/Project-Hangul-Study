import XCTest
@testable import HangulStudy

final class VocabularyPassTests: XCTestCase {
    private let setID = UUID(uuidString: "6296f6f4-5a33-4386-8eeb-33842eb48c11")!
    private func ids(_ count: Int = 20) -> [ContentID] {
        (1...count).map { ContentID(rawValue: String(format: "10000000-0000-4000-8000-%012d", $0)) }
    }
    private func start(_ count: Int = 20) throws -> VocabularySession {
        try VocabularyPassEngine.start(setID: setID, ids: ids(count), contentVersion: 5, seed: 42)
    }
    private func decide(_ state: VocabularySession, _ decision: VocabularyDecision) throws -> VocabularySession {
        let exposed = try VocabularyPassEngine.applying(.expose(revision: 1, contentVersion: 5), to: state)
        let revealed = try VocabularyPassEngine.applying(.reveal, to: exposed)
        return try VocabularyPassEngine.applying(.decide(decision), to: revealed)
    }
    func testTwentyEightThreeZero() throws {
        var state = try start()
        let originalIDs = state.vocabularyIDs
        for remainingCount in [8, 3, 0] {
            let toLearn = Set(state.order.prefix(remainingCount))
            let seen = state.order
            for id in seen {
                XCTAssertEqual(state.currentID, id)
                state = try decide(state, toLearn.contains(id) ? .learn : .known)
            }
            XCTAssertEqual(Set(state.deferred), toLearn)
            if remainingCount > 0 {
                XCTAssertTrue(state.needsNextRound)
                state = try VocabularyPassEngine.applying(.nextRound, to: state)
                XCTAssertEqual(Set(state.order), toLearn)
                XCTAssertEqual(state.position, 0)
                XCTAssertFalse(state.revealed)
            }
        }
        XCTAssertTrue(state.completed)
        XCTAssertEqual(state.round, 3)
        XCTAssertEqual(state.totalExposures, 31)
        XCTAssertEqual(state.vocabularyIDs, originalIDs)
    }
    func testAllKnownFinishesFirstRoundWithoutPermanentMasteryFlag() throws {
        var state = try start()
        for _ in 0..<20 { state = try decide(state, .known) }
        XCTAssertTrue(state.completed); XCTAssertEqual(state.round, 1)
        XCTAssertEqual(state.totalExposures, 20); XCTAssertTrue(state.deferred.isEmpty)
        XCTAssertThrowsError(try VocabularyPassEngine.applying(.nextRound, to: state))
    }
    func testAllUnknownRemainForNextRoundAndDoNotReappearWithinRound() throws {
        var state = try start()
        let firstOrder = state.order
        for id in firstOrder {
            XCTAssertEqual(state.currentID, id)
            state = try decide(state, .learn)
        }
        XCTAssertNil(state.currentID); XCTAssertFalse(state.completed)
        let next = try VocabularyPassEngine.applying(.nextRound, to: state)
        XCTAssertEqual(Set(next.order), Set(firstOrder))
        XCTAssertNotEqual(next.order, firstOrder)
        XCTAssertNotEqual(next.order.first, firstOrder.last)
    }
    func testMustExposeAndRevealBeforeJudgment() throws {
        let state = try start()
        XCTAssertThrowsError(try VocabularyPassEngine.applying(.reveal, to: state))
        XCTAssertThrowsError(try VocabularyPassEngine.applying(.decide(.known), to: state))
        let exposed = try VocabularyPassEngine.applying(.expose(revision: 1, contentVersion: 5), to: state)
        XCTAssertThrowsError(try VocabularyPassEngine.applying(.decide(.learn), to: exposed))
        XCTAssertEqual(try VocabularyPassEngine.applying(.expose(revision: 1, contentVersion: 5), to: exposed), exposed)
    }
    func testSeedIsDeterministicAndNotDependentOnNewSessionUUID() throws {
        var first = try start(), second = try start()
        for _ in 0..<20 { first = try decide(first, .learn); second = try decide(second, .learn) }
        let a = try VocabularyPassEngine.applying(.nextRound, to: first)
        let b = try VocabularyPassEngine.applying(.nextRound, to: second)
        XCTAssertEqual(a.order, b.order)
    }
    func testSingleRemainingRequiresExplicitNextRound() throws {
        var state = try start(1)
        state = try decide(state, .learn)
        XCTAssertNil(state.currentID); XCTAssertTrue(state.needsNextRound)
        state = try VocabularyPassEngine.applying(.nextRound, to: state)
        XCTAssertEqual(state.currentID, ids(1).first)
        XCTAssertFalse(state.revealed)
    }
    func testTwoRemainingNeverImmediatelyRepeatLast() throws {
        var state = try start(2)
        for _ in 0..<2 { state = try decide(state, .learn) }
        let last = state.order.last
        state = try VocabularyPassEngine.applying(.nextRound, to: state)
        XCTAssertNotEqual(last, state.currentID)
    }
    func testCodableRestoresThirteenthCardRevealAndStableIDSnapshot() throws {
        var state = try start()
        for _ in 0..<12 { state = try decide(state, .learn) }
        state = try VocabularyPassEngine.applying(.expose(revision: 1, contentVersion: 5), to: state)
        state = try VocabularyPassEngine.applying(.reveal, to: state)
        let restored = try JSONDecoder().decode(VocabularySession.self, from: JSONEncoder().encode(state))
        try restored.validate()
        XCTAssertEqual(restored, state)
        XCTAssertEqual(restored.currentID, ids()[12]); XCTAssertTrue(restored.revealed)
        let reorderedContent = Array(ids().reversed()) + [ContentID(rawValue: UUID().uuidString.lowercased())]
        XCTAssertTrue(reorderedContent.contains(try XCTUnwrap(restored.currentID)))
        XCTAssertEqual(restored.vocabularyIDs, ids())
    }
    func testRejectsDuplicateEmptyOversizedAndCorruptSnapshots() throws {
        XCTAssertThrowsError(try VocabularyPassEngine.start(setID: setID, ids: [], contentVersion: 5, seed: 0))
        XCTAssertThrowsError(try VocabularyPassEngine.start(setID: setID, ids: ids(26), contentVersion: 5, seed: 0))
        XCTAssertThrowsError(try VocabularyPassEngine.start(setID: setID, ids: ids(1) + ids(1), contentVersion: 5, seed: 0))
        var corrupt = try start(); corrupt.position = 13
        XCTAssertThrowsError(try corrupt.validate())
    }

    private func repository(at directory: URL) throws -> SQLiteProgressRepository {
        let schema = try XCTUnwrap(Bundle.main.url(forResource: "user-schema-v1", withExtension: "sql"))
        return try SQLiteProgressRepository(url: directory.appendingPathComponent("progress.sqlite"),
            schema: String(contentsOf: schema, encoding: .utf8), datasetID: "ko-ja-core")
    }
    func testRepositoryColdReopenAndContentVersionUpdateRetainCurrentCard() async throws {
        let directory = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try FileManager.default.createDirectory(at: directory, withIntermediateDirectories: true)
        defer { try? FileManager.default.removeItem(at: directory) }
        let repo = try repository(at: directory)
        let set = try await repo.createVocabularySet(level: .intro, ids: ids())
        var state = try await repo.beginVocabularySet(set.id, contentVersion: 5, restart: false)
        for _ in 0..<12 {
            state = try await repo.updateVocabularySession(state.id, expectedRevision: state.revision, action: .expose(revision: 1, contentVersion: 5))
            state = try await repo.updateVocabularySession(state.id, expectedRevision: state.revision, action: .reveal)
            state = try await repo.updateVocabularySession(state.id, expectedRevision: state.revision, action: .decide(.learn))
        }
        state = try await repo.updateVocabularySession(state.id, expectedRevision: state.revision, action: .expose(revision: 1, contentVersion: 5))
        state = try await repo.updateVocabularySession(state.id, expectedRevision: state.revision, action: .reveal)
        let reopened = try repository(at: directory)
        let resumed = try await reopened.beginVocabularySet(set.id, contentVersion: 6, restart: false)
        XCTAssertEqual(resumed, state); XCTAssertEqual(resumed.currentID, ids()[12])
        let summary = try await reopened.summary(now: Date())
        XCTAssertEqual(summary.studyCount, 13); XCTAssertEqual(summary.correctCount, 0)
        let repeated = try await reopened.updateVocabularySession(resumed.id, expectedRevision: resumed.revision, action: .expose(revision: 2, contentVersion: 6))
        XCTAssertEqual(repeated.totalExposures, 13)
    }
    func testRepositoryAtomicCompletionStaleSubmissionAndRepeatHistory() async throws {
        let directory = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try FileManager.default.createDirectory(at: directory, withIntermediateDirectories: true)
        defer { try? FileManager.default.removeItem(at: directory) }
        let repo = try repository(at: directory)
        let set = try await repo.createVocabularySet(level: .intro, ids: ids(1))
        var state = try await repo.beginVocabularySet(set.id, contentVersion: 5, restart: false)
        state = try await repo.updateVocabularySession(state.id, expectedRevision: state.revision, action: .expose(revision: 1, contentVersion: 5))
        state = try await repo.updateVocabularySession(state.id, expectedRevision: state.revision, action: .reveal)
        let previous = state
        state = try await repo.updateVocabularySession(state.id, expectedRevision: state.revision, action: .decide(.known))
        XCTAssertTrue(state.completed)
        do {
            _ = try await repo.updateVocabularySession(previous.id, expectedRevision: previous.revision, action: .decide(.learn))
            XCTFail("Stale action must not change the next card")
        } catch { XCTAssertEqual(error as? VocabularyStudyError, .staleState) }
        let again = try await repo.beginVocabularySet(set.id, contentVersion: 6, restart: true)
        XCTAssertNotEqual(again.id, state.id); XCTAssertFalse(again.completed)
        let retained = try await repo.vocabularySession(state.id)
        XCTAssertEqual(retained, state)
        let sets = try await repo.vocabularySets(level: .intro, after: 0, limit: 50)
        XCTAssertEqual(sets.first?.completedCount, 1)
        let db = try SQLiteConnection(url: directory.appendingPathComponent("progress.sqlite"), readOnly: true)
        XCTAssertEqual(try db.query("SELECT acquisition_status FROM item_progress").first?.text("acquisition_status"), "unassessed")
        XCTAssertEqual(try db.query("SELECT COUNT(*) AS n FROM srs_state").first?.integer("n"), 1)
    }
    func testCatalogContentReorderingAndNewVocabularyDoNotChangeStartedSet() async throws {
        let directory = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try FileManager.default.createDirectory(at: directory, withIntermediateDirectories: true)
        defer { try? FileManager.default.removeItem(at: directory) }
        let source = try XCTUnwrap(Bundle.main.url(forResource: "content", withExtension: "sqlite"))
        let copy = directory.appendingPathComponent("content.sqlite")
        try FileManager.default.copyItem(at: source, to: copy)
        let originalContent = try SQLiteContentRepository(url: copy, allowFixture: false)
        let progress = try repository(at: directory)
        let originalCatalog = VocabularySetCatalog(content: originalContent, progress: progress)
        let first = try await originalCatalog.createNext()
        let started = try await progress.beginVocabularySet(first.id, contentVersion: 5, restart: false)
        let newID = UUID().uuidString.lowercased(), meaningID = UUID().uuidString.lowercased()
        let writer = try SQLiteConnection(url: copy, readOnly: false)
        try writer.transaction {
            try writer.execute("UPDATE vocabulary SET sort_key='changed-'||id")
            try writer.execute("UPDATE content_metadata SET content_version=content_version+1")
            try writer.execute("INSERT INTO content_items(id,kind,revision,is_active,level,created_at,updated_at) VALUES(?,'vocabulary',1,1,'intro','2026-10-01T00:00:00Z','2026-10-01T00:00:00Z')", [.text(newID)])
            try writer.execute("INSERT INTO content_items(id,kind,revision,is_active,level,created_at,updated_at) VALUES(?,'meaning',1,1,'intro','2026-10-01T00:00:00Z','2026-10-01T00:00:00Z')", [.text(meaningID)])
            try writer.execute("INSERT INTO vocabulary(id,headword,part_of_speech,sort_key) VALUES(?,'테스트','noun','000-new-first')", [.text(newID)])
            try writer.execute("INSERT INTO meanings(id,vocabulary_id,meaning_ja,ordinal) VALUES(?,?,'テスト専用',0)", [.text(meaningID), .text(newID)])
        }
        let updatedContent = try SQLiteContentRepository(url: copy, allowFixture: false)
        let next = try await VocabularySetCatalog(content: updatedContent, progress: progress).createNext()
        XCTAssertEqual(next.vocabularyIDs.first?.rawValue, newID)
        XCTAssertTrue(Set(next.vocabularyIDs).isDisjoint(with: Set(first.vocabularyIDs)))
        let resumed = try await progress.beginVocabularySet(first.id, contentVersion: 6, restart: false)
        XCTAssertEqual(resumed, started)
        let word = try await updatedContent.vocabularyCard(id: try XCTUnwrap(resumed.currentID))
        XCTAssertEqual(word.id, started.currentID)
    }
    func testProductionCatalogAllocatesDisjointSetsAndReadsRealMeaningsExamplesNotes() async throws {
        let directory = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try FileManager.default.createDirectory(at: directory, withIntermediateDirectories: true)
        defer { try? FileManager.default.removeItem(at: directory) }
        let contentURL = try XCTUnwrap(Bundle.main.url(forResource: "content", withExtension: "sqlite"))
        let content = try SQLiteContentRepository(url: contentURL, allowFixture: false)
        let progress = try repository(at: directory)
        let catalog = VocabularySetCatalog(content: content, progress: progress)
        let first = try await catalog.createNext(), second = try await catalog.createNext()
        XCTAssertEqual(first.vocabularyIDs.count, 20); XCTAssertEqual(second.vocabularyIDs.count, 20)
        XCTAssertTrue(Set(first.vocabularyIDs).isDisjoint(with: Set(second.vocabularyIDs)))
        let count = try await content.vocabularyCount(level: .intro)
        XCTAssertGreaterThanOrEqual(count, 226)
        for id in first.vocabularyIDs {
            let card = try await content.vocabularyCard(id: id)
            XCTAssertEqual(card.id, id); XCTAssertFalse(card.meanings.isEmpty)
            XCTAssertNotNil(card.meanings.first?.example)
            XCTAssertTrue(AudioPolicy.permitsTTS(card.audio))
        }
    }
    func testData02BeginnerUsesExistingPassSRSAndColdResume() async throws {
        let directory = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try FileManager.default.createDirectory(at: directory, withIntermediateDirectories: true)
        defer { try? FileManager.default.removeItem(at: directory) }
        let url = try XCTUnwrap(Bundle.main.url(forResource: "content", withExtension: "sqlite"))
        let content = try SQLiteContentRepository(url: url, allowFixture: false)
        let progress = try repository(at: directory)
        let catalog = VocabularySetCatalog(content: content, progress: progress)
        let intro = try await catalog.createNext(level: .intro)
        let beginner = try await catalog.createNext(level: .beginner)
        XCTAssertEqual(beginner.vocabularyIDs.count, 20)
        XCTAssertEqual(beginner.level, .beginner)
        XCTAssertTrue(Set(intro.vocabularyIDs).isDisjoint(with: Set(beginner.vocabularyIDs)))
        var pass = try await progress.beginVocabularySet(beginner.id, contentVersion: 6, restart: false)
        while let id = pass.currentID {
            let card = try await content.vocabularyCard(id: id)
            XCTAssertNotNil(card.meanings.first?.example)
            XCTAssertTrue(AudioPolicy.permitsTTS(card.audio))
            pass = try await progress.updateVocabularySession(pass.id, expectedRevision: pass.revision,
                action: .expose(revision: card.revision, contentVersion: 6))
            pass = try await progress.updateVocabularySession(pass.id, expectedRevision: pass.revision, action: .reveal)
            pass = try await progress.updateVocabularySession(pass.id, expectedRevision: pass.revision, action: .decide(.known))
        }
        XCTAssertTrue(pass.completed)
        let reopened = try repository(at: directory)
        let restored = try await reopened.vocabularySession(pass.id)
        XCTAssertEqual(restored, pass)
        for id in beginner.vocabularyIDs {
            let state = try await reopened.reviewState(for: id, skill: "vocabulary")
            XCTAssertEqual(state?.stage, 0)
            XCTAssertNotNil(state?.nextReviewAt)
        }
        let next = try await VocabularySetCatalog(content: content, progress: reopened).createNext(level: .beginner)
        XCTAssertTrue(Set(next.vocabularyIDs).isDisjoint(with: Set(beginner.vocabularyIDs)))
    }

    // Authored for Xcode: Linux SQL tests do not execute this Swift integration flow.
    func testData03ProductionTwoRoundsColdResumeAndDueReview() async throws {
        let directory = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try FileManager.default.createDirectory(at: directory, withIntermediateDirectories: true)
        defer { try? FileManager.default.removeItem(at: directory) }
        let url = try XCTUnwrap(Bundle.main.url(forResource: "content", withExtension: "sqlite"))
        let content = try SQLiteContentRepository(url: url, allowFixture: false)
        let metadata = try await content.metadata()
        let progress = try repository(at: directory)
        // Published UUIDs, not row positions or a second vocabulary data source.
        let words = [ContentID(rawValue: "af95f164-5e0e-43c5-8852-a480238e4b74"),
                     ContentID(rawValue: "00a8044a-1f84-4d6b-bd78-672cff4a6f10")]
        let set = try await progress.createVocabularySet(level: .beginner, ids: words)
        var pass = try await progress.beginVocabularySet(set.id, contentVersion: metadata.contentVersion, restart: false)
        while let id = pass.currentID {
            let card = try await content.vocabularyCard(id: id)
            XCTAssertNotNil(card.meanings.first?.example)
            XCTAssertTrue(AudioPolicy.permitsTTS(card.audio))
            pass = try await progress.updateVocabularySession(pass.id, expectedRevision: pass.revision,
                action: .expose(revision: card.revision, contentVersion: metadata.contentVersion))
            pass = try await progress.updateVocabularySession(pass.id, expectedRevision: pass.revision, action: .reveal)
            pass = try await progress.updateVocabularySession(pass.id, expectedRevision: pass.revision,
                action: .decide(id == words[0] ? .learn : .known))
        }
        XCTAssertTrue(pass.needsNextRound)
        let reopened = try repository(at: directory)
        let restored = try await reopened.beginVocabularySet(set.id, contentVersion: metadata.contentVersion, restart: false)
        XCTAssertEqual(restored, pass)
        pass = try await reopened.updateVocabularySession(pass.id, expectedRevision: pass.revision, action: .nextRound)
        XCTAssertEqual(pass.order, [words[0]])
        pass = try await reopened.updateVocabularySession(pass.id, expectedRevision: pass.revision,
            action: .expose(revision: 1, contentVersion: metadata.contentVersion))
        pass = try await reopened.updateVocabularySession(pass.id, expectedRevision: pass.revision, action: .reveal)
        pass = try await reopened.updateVocabularySession(pass.id, expectedRevision: pass.revision, action: .decide(.known))
        XCTAssertTrue(pass.completed)
        var due = Date.distantPast
        for id in words {
            let value = try await reopened.reviewState(for: id, skill: "vocabulary")
            let state = try XCTUnwrap(value)
            XCTAssertEqual(state.stage, 0)
            due = max(due, state.nextReviewAt)
        }
        let summary = try await reopened.reviewSummary(now: due, timeZoneID: "Asia/Tokyo")
        XCTAssertEqual(summary.due, 2)
        var review = try await reopened.beginReview(now: due, limit: 20)
        let current = try XCTUnwrap(review.currentID)
        XCTAssertTrue(words.contains(current))
        review = try await reopened.exposeReview(sessionID: review.id, contentID: current,
            contentRevision: 1, contentVersion: metadata.contentVersion, now: due, timeZoneID: "Asia/Tokyo")
        review = try await reopened.revealReview(sessionID: review.id, contentID: current, now: due)
        _ = try await reopened.submitReview(sessionID: review.id, contentID: current,
            rating: .remembered, now: due, timeZoneID: "Asia/Tokyo")
        let cold = try repository(at: directory)
        let advanced = try await cold.reviewState(for: current, skill: "vocabulary")
        XCTAssertEqual(advanced?.stage, 1)
        let keptPass = try await cold.vocabularySession(pass.id)
        XCTAssertEqual(keptPass, pass)
    }

}
