import Foundation

/// Shared gate for bundled content and future staged packages. No network updater in DEV-02.
enum ContentPackageValidator {
    static let supportedSchema = 4
    static let readerVersion = 7
    static func validate(_ db: SQLiteConnection, allowFixture: Bool) throws -> ContentMetadata {
        let version = try db.query("PRAGMA user_version").first?.integer("user_version") ?? 0
        guard [2, 3, supportedSchema].contains(version) else { throw DatabaseError.unsupportedVersion(version) }
        guard let row = try db.query("SELECT * FROM content_metadata WHERE singleton=1").first else {
            throw DatabaseError.invalidData("Missing content metadata")
        }
        guard try row.integer("schema_version") == version,
              try row.integer("min_reader_version") <= readerVersion else {
            throw DatabaseError.invalidData("Incompatible content package")
        }
        let fixture = try row.integer("is_fixture") == 1
        guard allowFixture || !fixture else { throw DatabaseError.invalidData("Fixture content is disabled") }
        return ContentMetadata(datasetID: try row.text("dataset_id"), contentVersion: try row.integer("content_version"), isFixture: fixture)
    }
}
