import Foundation

enum StudyDay {
    static func key(for date: Date, timeZoneID: String) throws -> String {
        guard date.timeIntervalSince1970.isFinite, let zone = TimeZone(identifier: timeZoneID) else { throw DatabaseError.invalidData("Invalid time zone") }
        let formatter = DateFormatter()
        formatter.locale = Locale(identifier: "en_US_POSIX")
        formatter.calendar = Calendar(identifier: .gregorian)
        formatter.timeZone = zone
        formatter.dateFormat = "yyyy-MM-dd"
        return formatter.string(from: date)
    }
}
