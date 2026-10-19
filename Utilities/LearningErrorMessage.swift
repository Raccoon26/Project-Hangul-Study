import Foundation

/// Explicit allow-list: database paths, SQL, decoding details and SDK errors stay internal.
enum LearningErrorMessage {
    static func message(for error: Error) -> String {
        if let error = error as? LessonError { return error.errorDescription ?? fallback }
        if let error = error as? VocabularyStudyError { return error.errorDescription ?? fallback }
        if let error = error as? GrammarError { return error.errorDescription ?? fallback }
        if let error = error as? ReviewError { return error.errorDescription ?? fallback }
        return fallback
    }
    private static let fallback = "処理を完了できませんでした。記録を削除せず、読み直してからもう一度お試しください。"
}
