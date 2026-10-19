import Foundation

struct ActivityWindow: Identifiable, Sendable {
    let days: Int
    let actions: Int
    let correct: Int
    let incorrect: Int
    let reviews: Int
    let productionCorrect: Int
    let productionWrong: Int
    let listeningCorrect: Int
    let listeningWrong: Int
    var id: Int { days }
    var title: String { days == 1 ? "今日" : "最近\(days)日" }
    static func accuracy(correct: Int, wrong: Int) -> String {
        guard correct + wrong > 0 else { return "まだ記録がありません" }
        return "\(Int((100.0 * Double(correct) / Double(correct + wrong)).rounded()))% · \(correct) / \(correct + wrong)"
    }
}
struct LearningStatistics: Sendable {
    let windows: [ActivityWindow]
    let seenWords: Int
    let passedWords: Int
    let reviewingWords: Int
    let stableWords: Int
    let studiedGrammar: Int
    let reviewingGrammar: Int
    let stableGrammar: Int
}
enum StatisticsCalendar {
    static func start(days: Int, now: Date, timeZone: TimeZone) -> Date {
        var calendar = Calendar(identifier:.gregorian); calendar.timeZone = timeZone
        let today = calendar.startOfDay(for:now)
        return calendar.date(byAdding:.day,value:-(max(1,days)-1),to:today) ?? today
    }
}
