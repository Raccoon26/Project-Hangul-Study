import Foundation

enum UserDatabaseMigration {
    static let currentVersion = 10
    static func migrate(_ db: SQLiteConnection, schema: String) throws {
        let version = try db.query("PRAGMA user_version").first?.integer("user_version") ?? 0
        guard version <= currentVersion else { throw DatabaseError.unsupportedVersion(version) }
        if version == 0 {
            let tables = try db.query("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
            guard tables.isEmpty else { throw DatabaseError.invalidData("Unversioned nonempty database; refusing destructive recovery") }
            try db.transaction { try db.executeScript(schema) }
        }
        if version > 0 && version < currentVersion { _ = try db.backupBeforeMigration(toVersion: currentVersion) }
        if version < currentVersion {
            for target in max(2, version + 1)...currentVersion {
                guard let url = Bundle.main.url(forResource: "user-migration-v\(target)", withExtension: "sql") else {
                    throw DatabaseError.invalidData("Missing user migration v\(target)")
                }
                let migration = try String(contentsOf: url, encoding: .utf8)
                try db.transaction { try db.executeScript(migration) }
            }
        }
        try db.executeScript("PRAGMA journal_mode=WAL; PRAGMA synchronous=FULL;")
    }
}
