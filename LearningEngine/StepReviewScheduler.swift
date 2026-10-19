import Foundation

/// Version this policy before changing any scheduling semantics.
enum StepReviewScheduler {
    static let algorithm = "calendar_steps"
    static let version = 1
    static let days = [1, 3, 7, 14, 30, 60, 120]
    static func calendar(timeZoneID: String) throws -> Calendar {
        guard let zone = TimeZone(identifier: timeZoneID) else { throw ReviewError.invalidState }
        var calendar = Calendar(identifier: .gregorian)
        calendar.timeZone = zone
        return calendar
    }
    static func due(after days: Int, at date: Date, timeZoneID: String) throws -> Date {
        guard date.timeIntervalSince1970.isFinite else { throw ReviewError.invalidState }
        let calendar = try calendar(timeZoneID: timeZoneID)
        guard days > 0, let result = calendar.date(byAdding: .day, value: days, to: calendar.startOfDay(for: date)), result > date else { throw ReviewError.invalidState }
        return result
    }
    static func initial(at date: Date, neededRepetition: Bool, timeZoneID: String) throws -> SRSState {
        let state = SRSState(stage: 0, nextReviewAt: try due(after: 1, at: date, timeZoneID: timeZoneID),
            lastReviewedAt: nil, reviewCount: 0, consecutiveSuccesses: 0, failureCount: 0,
            lastResult: nil, firstLearnedAt: date, difficulty: nil, neededRepetition: neededRepetition,
            schedulingTimeZone: timeZoneID)
        try state.validate(); return state
    }
    static func next(previous: SRSState, result: ReviewRating, at date: Date, timeZoneID: String) throws -> SRSState {
        try previous.validate()
        guard date.timeIntervalSince1970.isFinite, date >= previous.firstLearnedAt,
              previous.lastReviewedAt.map({ date >= $0 }) ?? true else { throw ReviewError.invalidState }
        var state = previous
        let interval: Int
        switch result {
        case .remembered:
            state.stage = min(state.stage + 1, days.count - 1)
            state.consecutiveSuccesses += 1
            interval = days[state.stage]
        case .unsure:
            state.consecutiveSuccesses = 0
            interval = min(days[state.stage], 3)
        case .difficult:
            state.stage = 0; state.consecutiveSuccesses = 0; state.failureCount += 1
            interval = 1
        }
        state.reviewCount += 1; state.lastResult = result; state.lastReviewedAt = date
        state.nextReviewAt = try due(after: interval, at: date, timeZoneID: timeZoneID)
        state.schedulingTimeZone = timeZoneID
        try state.validate(); return state
    }
}
