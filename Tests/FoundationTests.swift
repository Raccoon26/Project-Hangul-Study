import XCTest
@testable import HangulStudy

final class FoundationTests: XCTestCase {
    private var directory: URL!
    override func setUpWithError() throws {
        directory = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try FileManager.default.createDirectory(at: directory, withIntermediateDirectories: true)
    }
    override func tearDownWithError() throws {
        try FileManager.default.removeItem(at: directory)
    }
    private func schema() throws -> String {
        let url = try XCTUnwrap(Bundle.main.url(forResource: "user-schema-v1", withExtension: "sql"))
        return try String(contentsOf: url, encoding: .utf8)
    }
    private func repository() throws -> SQLiteProgressRepository {
        try SQLiteProgressRepository(url: directory.appendingPathComponent("user.sqlite"), schema: schema(), datasetID: "test")
    }
    private let contentID = ContentID(rawValue: "00000000-0000-4000-8000-000000000001")

    func testFavoriteSurvivesReopenWithoutContentForeignKey() async throws {
        let repo = try repository()
        try await repo.setFavorite(contentID, enabled: true)
        try await repo.setFavorite(contentID, enabled: true)
        let reopened = try repository()
        let ids = try await reopened.favoriteIDs()
        XCTAssertEqual(ids, [contentID])
        try await reopened.setFavorite(contentID, enabled: false)
        let remaining = try await repo.favoriteIDs()
        XCTAssertTrue(remaining.isEmpty)
    }
    func testEventIdempotencyAndCounters() async throws {
        let repo = try repository()
        let event = StudyEvent(id: UUID(), contentID: contentID, contentRevision: 1, contentVersion: 1,
                               occurredAt: Date(timeIntervalSince1970: 0), timeZoneID: "Asia/Tokyo", skill: "recognition",
                               outcome: .correct, durationMilliseconds: 1000, sessionID: nil)
        try await repo.record(event)
        try await repo.record(event)
        let summary = try await repo.summary(now: Date())
        XCTAssertEqual(summary.studyCount, 1)
        XCTAssertEqual(summary.correctCount, 1)
        XCTAssertEqual(summary.incorrectCount, 0)
        XCTAssertEqual(summary.dueCount, 0)
    }
    func testWrongAnswerAndSkippedSemantics() async throws {
        let repo = try repository()
        for outcome in [StudyOutcome.incorrect, .skipped] {
            try await repo.record(StudyEvent(id: UUID(), contentID: contentID, contentRevision: 1, contentVersion: 1,
                                            occurredAt: Date(), timeZoneID: "Asia/Tokyo", skill: "recognition",
                                            outcome: outcome, durationMilliseconds: 10, sessionID: nil))
        }
        let result = try await repo.summary(now: Date())
        XCTAssertEqual(result.studyCount, 1)
        XCTAssertEqual(result.incorrectCount, 1)
    }
    func testFutureSchemaIsNotReset() throws {
        let url = directory.appendingPathComponent("future.sqlite")
        let db = try SQLiteConnection(url: url, readOnly: false)
        try db.executeScript("CREATE TABLE keep_me(value TEXT); INSERT INTO keep_me VALUES('safe'); PRAGMA user_version=999;")
        XCTAssertThrowsError(try UserDatabaseMigration.migrate(db, schema: schema()))
        XCTAssertEqual(try db.query("SELECT value FROM keep_me").first?.text("value"), "safe")
    }
    func testTransactionRollsBack() throws {
        let db = try SQLiteConnection(url: directory.appendingPathComponent("rollback.sqlite"), readOnly: false)
        try db.executeScript("CREATE TABLE sample(id TEXT PRIMARY KEY)")
        XCTAssertThrowsError(try db.transaction {
            try db.execute("INSERT INTO sample VALUES(?)", [.text("same")])
            try db.execute("INSERT INTO sample VALUES(?)", [.text("same")])
        })
        XCTAssertTrue(try db.query("SELECT * FROM sample").isEmpty)
    }
    func testDatasetMismatchDoesNotDestroyFavorites() async throws {
        let repo = try repository()
        try await repo.setFavorite(contentID, enabled: true)
        XCTAssertThrowsError(try SQLiteProgressRepository(url: directory.appendingPathComponent("user.sqlite"), schema: schema(), datasetID: "other"))
        let ids = try await repo.favoriteIDs()
        XCTAssertTrue(ids.contains(contentID))
    }
    func testJapaneseStudyDayBoundary() throws {
        let date = Date(timeIntervalSince1970: 16 * 3600)
        XCTAssertEqual(try StudyDay.key(for: date, timeZoneID: "Asia/Tokyo"), "1970-01-02")
        XCTAssertEqual(try StudyDay.key(for: date, timeZoneID: "UTC"), "1970-01-01")
        XCTAssertThrowsError(try StudyDay.key(for: date, timeZoneID: "invalid"))
    }
    func testContentPagingReadOnlyAndFixtureGate() async throws {
        let url = try XCTUnwrap(Bundle(for: FoundationTests.self).url(forResource: "content-fixture", withExtension: "sqlite"))
        let repo = try SQLiteContentRepository(url: url, allowFixture: true)
        let info = try await repo.metadata()
        XCTAssertTrue(info.isFixture, "Run tests with the shared Debug test scheme")
        let first = try await repo.vocabulary(after: nil, limit: 1)
        let word = try XCTUnwrap(first.first)
        let second = try await repo.vocabulary(after: VocabularyCursor(sortKey: word.sortKey, id: word.id), limit: 1)
        XCTAssertEqual(second.count, 1)
        XCTAssertNotEqual(word.id, second.first?.id)
        XCTAssertThrowsError(try SQLiteContentRepository(url: url, allowFixture: false))
        let db = try SQLiteConnection(url: url, readOnly: true)
        XCTAssertThrowsError(try db.execute("DELETE FROM vocabulary"))
    }
    func testV10UserMigrationPreservesV1AndCreatesBackup() throws {
        let url = directory.appendingPathComponent("legacy.sqlite")
        let db = try SQLiteConnection(url: url, readOnly: false)
        try db.executeScript(schema())
        try db.execute("INSERT INTO favorites VALUES(?,?)", [.text(contentID.rawValue), .real(1)])
        try db.execute("INSERT INTO item_progress(content_id,first_seen_at,last_seen_at,study_count,correct_count,completed_passes) VALUES(?,1,2,3,2,4)", [.text(contentID.rawValue)])
        try UserDatabaseMigration.migrate(db, schema: schema())
        let row = try XCTUnwrap(db.query("SELECT * FROM item_progress").first)
        XCTAssertEqual(try row.integer("study_count"), 3)
        XCTAssertEqual(try row.integer("completed_passes"), 4)
        XCTAssertEqual(try row.text("acquisition_status"), "unassessed")
        XCTAssertEqual(row["perceived_difficulty"], .null)
        XCTAssertEqual(try db.query("PRAGMA user_version").first?.integer("user_version"), 10)
        let files = try FileManager.default.contentsOfDirectory(at: directory, includingPropertiesForKeys: nil)
        let backupURL = try XCTUnwrap(files.first { $0.pathExtension == "backup" })
        let backup = try SQLiteConnection(url: backupURL, readOnly: true)
        XCTAssertEqual(try backup.query("PRAGMA user_version").first?.integer("user_version"), 1)
        XCTAssertEqual(try backup.query("SELECT COUNT(*) AS n FROM favorites").first?.integer("n"), 1)
    }

    func testLevelAndJapanesePrefixSearch() async throws {
        let url = try XCTUnwrap(Bundle(for: FoundationTests.self).url(forResource: "content-fixture", withExtension: "sqlite"))
        let repo = try SQLiteContentRepository(url: url, allowFixture: true)
        let matches = try await repo.vocabulary(matching: VocabularyQuery(level: .intro, prefix: "水"), after: nil, limit: 50)
        XCTAssertEqual(matches.count, 1)
        XCTAssertEqual(matches.first?.headword, "물")
        let none = try await repo.vocabulary(matching: VocabularyQuery(level: .master, prefix: "水"), after: nil, limit: 50)
        XCTAssertTrue(none.isEmpty)
        let korean = try await repo.vocabulary(matching: VocabularyQuery(prefix: " 안녕 "), after: nil, limit: 1)
        XCTAssertEqual(korean.first?.headword, "안녕하세요")
    }

}
