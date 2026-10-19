import Foundation
import SQLite3

enum DatabaseError: Error, LocalizedError {
    case sqlite(String)
    case invalidData(String)
    case unsupportedVersion(Int)
    var errorDescription: String? {
        switch self {
        case .sqlite(let message), .invalidData(let message): return message
        case .unsupportedVersion(let version): return "Unsupported database version: \(version)"
        }
    }
}

enum SQLValue: Equatable, Sendable {
    case text(String), integer(Int64), real(Double), null
    var string: String? { if case .text(let value) = self { return value }; return nil }
    var int: Int? { if case .integer(let value) = self { return Int(exactly: value) }; return nil }
}

typealias SQLRow = [String: SQLValue]
extension Dictionary where Key == String, Value == SQLValue {
    func text(_ key: String) throws -> String {
        guard let value = self[key]?.string else { throw DatabaseError.invalidData("Missing text: \(key)") }
        return value
    }
    func integer(_ key: String) throws -> Int {
        guard let value = self[key]?.int else { throw DatabaseError.invalidData("Missing integer: \(key)") }
        return value
    }
}

/// Confined to the owning repository actor; never expose a connection to views.
final class SQLiteConnection {
    private var handle: OpaquePointer?
    private let fileURL: URL
    init(url: URL, readOnly: Bool) throws {
        fileURL = url
        let flags = readOnly ? SQLITE_OPEN_READONLY : SQLITE_OPEN_READWRITE | SQLITE_OPEN_CREATE
        let result = sqlite3_open_v2(url.path, &handle, flags | SQLITE_OPEN_FULLMUTEX, nil)
        guard result == SQLITE_OK else {
            let message = handle.map { String(cString: sqlite3_errmsg($0)) } ?? "Cannot open database"
            if let handle = handle { sqlite3_close(handle) }
            handle = nil
            throw DatabaseError.sqlite(message)
        }
        sqlite3_busy_timeout(handle, 5_000)
        do { try executeScript("PRAGMA foreign_keys=ON;") }
        catch { sqlite3_close(handle); handle = nil; throw error }
    }
    deinit { sqlite3_close(handle) }
    private func failure() -> DatabaseError {
        .sqlite(handle.map { String(cString: sqlite3_errmsg($0)) } ?? "Closed database")
    }
    func executeScript(_ sql: String) throws {
        guard sqlite3_exec(handle, sql, nil, nil, nil) == SQLITE_OK else { throw failure() }
    }
    func query(_ sql: String, _ bindings: [SQLValue] = []) throws -> [SQLRow] {
        var statement: OpaquePointer?
        guard sqlite3_prepare_v2(handle, sql, -1, &statement, nil) == SQLITE_OK else { throw failure() }
        defer { sqlite3_finalize(statement) }
        guard sqlite3_bind_parameter_count(statement) == Int32(bindings.count) else {
            throw DatabaseError.invalidData("Binding count mismatch")
        }
        let transient = unsafeBitCast(-1, to: sqlite3_destructor_type.self)
        for (index, value) in bindings.enumerated() {
            let position = Int32(index + 1)
            let result: Int32
            switch value {
            case .text(let text):
                guard let count = Int32(exactly: text.utf8.count) else { throw DatabaseError.invalidData("Text exceeds SQLite binding limit") }
                result = sqlite3_bind_text(statement, position, text, count, transient)
            case .integer(let number): result = sqlite3_bind_int64(statement, position, number)
            case .real(let number): result = sqlite3_bind_double(statement, position, number)
            case .null: result = sqlite3_bind_null(statement, position)
            }
            guard result == SQLITE_OK else { throw failure() }
        }
        var rows: [SQLRow] = []
        while true {
            let result = sqlite3_step(statement)
            if result == SQLITE_DONE { return rows }
            guard result == SQLITE_ROW else { throw failure() }
            var row: SQLRow = [:]
            for index in 0..<sqlite3_column_count(statement) {
                let key = String(cString: sqlite3_column_name(statement, index))
                switch sqlite3_column_type(statement, index) {
                case SQLITE_TEXT:
                    if let value = sqlite3_column_text(statement, index) {
                        let count = Int(sqlite3_column_bytes(statement, index))
                        row[key] = .text(String(decoding: UnsafeBufferPointer(start:value, count:count), as:UTF8.self))
                    }
                case SQLITE_INTEGER: row[key] = .integer(sqlite3_column_int64(statement, index))
                case SQLITE_FLOAT: row[key] = .real(sqlite3_column_double(statement, index))
                default: row[key] = .null
                }
            }
            rows.append(row)
        }
    }
    func execute(_ sql: String, _ bindings: [SQLValue] = []) throws { _ = try query(sql, bindings) }
    /// SQLite backup API captures committed WAL pages; never copy only the .sqlite file.
    func backupBeforeMigration(toVersion version: Int) throws -> URL {
        let target = fileURL.deletingLastPathComponent().appendingPathComponent(
            fileURL.lastPathComponent + ".before-v\(version)-\(UUID().uuidString).backup")
        do {
            let destination = try SQLiteConnection(url: target, readOnly: false)
            guard let backup = sqlite3_backup_init(destination.handle, "main", handle, "main") else {
                throw destination.failure()
            }
            let stepResult = sqlite3_backup_step(backup, -1)
            let finishResult = sqlite3_backup_finish(backup)
            guard stepResult == SQLITE_DONE, finishResult == SQLITE_OK else {
                throw DatabaseError.sqlite("Cannot create a consistent migration backup")
            }
            return target
        } catch {
            try? FileManager.default.removeItem(at: target)
            throw error
        }
    }
    func transaction<T>(_ body: () throws -> T) throws -> T {
        try executeScript("BEGIN IMMEDIATE")
        do {
            let result = try body()
            try executeScript("COMMIT")
            return result
        } catch {
            try? executeScript("ROLLBACK")
            throw error
        }
    }
}
