import SwiftUI
import UserNotifications

enum StudyAmount: String, CaseIterable, Codable {
    case light, standard, extended
    var title: String { switch self { case .light: return "軽く · 5語"; case .standard: return "ふつう · 10語"; case .extended: return "多め · 20語" } }
    var count: Int { switch self { case .light: return 5; case .standard: return 10; case .extended: return 20 } }
}
struct LearningPreferences: Codable, Equatable {
    var amount: StudyAmount = .light
    var reminderEnabled = false
    var hour = 20
    var minute = 0
    var valid: Bool { (0...23).contains(hour) && (0...59).contains(minute) }
}
enum ReminderAuthorization { case notDetermined, allowed, denied }
@MainActor
protocol ReminderBackend {
    func authorization() async -> ReminderAuthorization
    func request() async throws -> Bool
    func schedule(hour: Int, minute: Int) async throws
    func cancel()
}
@MainActor
final class SystemReminderBackend: ReminderBackend {
    private let center = UNUserNotificationCenter.current()
    private let identifier = "learning.daily.reminder"
    func authorization() async -> ReminderAuthorization {
        let settings = await center.notificationSettings()
        switch settings.authorizationStatus {
        case .notDetermined: return .notDetermined
        case .authorized, .provisional, .ephemeral: return .allowed
        default: return .denied
        }
    }
    func request() async throws -> Bool { try await center.requestAuthorization(options:[.alert,.sound]) }
    func schedule(hour: Int, minute: Int) async throws {
        let content = UNMutableNotificationContent()
        content.title = "韓国語の学習"
        // A repeating reminder must not assert there are due items when there may be none.
        content.body = "少しだけ、韓国語を復習しませんか。続きからいつでも始められます。"
        var components = DateComponents(); components.hour = hour; components.minute = minute
        let trigger = UNCalendarNotificationTrigger(dateMatching:components,repeats:true)
        try await center.add(UNNotificationRequest(identifier:identifier,content:content,trigger:trigger))
    }
    func cancel() { center.removePendingNotificationRequests(withIdentifiers:[identifier]); center.removeDeliveredNotifications(withIdentifiers:[identifier]) }
}
@MainActor
final class LearningPreferencesStore: ObservableObject {
    static let key = "learning.preferences.v1"
    @Published private(set) var value: LearningPreferences
    @Published private(set) var busy = false
    @Published private(set) var denied = false
    @Published private(set) var message: String?
    private let defaults: UserDefaults
    private let reminders: any ReminderBackend
    init(defaults: UserDefaults = .standard, reminders: (any ReminderBackend)? = nil) {
        self.defaults = defaults; self.reminders = reminders ?? SystemReminderBackend()
        if let data = defaults.data(forKey:Self.key), let stored = try? JSONDecoder().decode(LearningPreferences.self,from:data), stored.valid { value = stored }
        else { value = LearningPreferences() }
    }
    func setAmount(_ amount: StudyAmount) { value.amount = amount; persist() }
    var reminderDate: Date {
        Calendar.current.date(from:DateComponents(year:2001,month:1,day:1,hour:value.hour,minute:value.minute)) ?? Date()
    }
    func setTime(_ date: Date) async {
        guard !busy else { return }
        let parts = Calendar.current.dateComponents([.hour,.minute],from:date)
        value.hour = parts.hour ?? 20; value.minute = parts.minute ?? 0; persist()
        if value.reminderEnabled { await setReminder(true) }
    }
    func setReminder(_ enabled: Bool) async {
        guard !busy else { return }; busy = true; message = nil
        defer { busy = false }
        if !enabled { reminders.cancel(); value.reminderEnabled = false; persist(); return }
        do {
            let status = await reminders.authorization()
            let allowed: Bool
            switch status {
            case .allowed: allowed = true
            case .denied: allowed = false
            case .notDetermined: allowed = try await reminders.request()
            }
            denied = !allowed
            guard allowed else {
                reminders.cancel(); value.reminderEnabled = false; persist()
                message = "通知は許可されていません。学習はそのまま続けられます。"; return
            }
            try await reminders.schedule(hour:value.hour,minute:value.minute)
            value.reminderEnabled = true; persist()
        } catch {
            reminders.cancel(); value.reminderEnabled = false; persist()
            message = "通知を設定できませんでした。時間を確認して、もう一度お試しください。"
        }
    }
    /// No permission request at launch or on return from system Settings.
    func reconcile() async {
        guard !busy else { return }; busy = true
        defer { busy = false }
        let status = await reminders.authorization()
        denied = status == .denied
        if !value.reminderEnabled { reminders.cancel(); return }
        if value.reminderEnabled {
            guard status == .allowed else { reminders.cancel(); value.reminderEnabled = false; persist(); return }
            do { try await reminders.schedule(hour:value.hour,minute:value.minute) }
            catch { reminders.cancel(); value.reminderEnabled = false; persist(); message = "通知を設定できませんでした。" }
        }
    }
    private func persist() {
        // This value consists only of validated enums, booleans and bounded integers.
        if let data = try? JSONEncoder().encode(value) { defaults.set(data,forKey:Self.key) }
    }
}
