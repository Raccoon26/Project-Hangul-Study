import SwiftUI

@main
@MainActor
struct HangulStudyApp: App {
    @StateObject private var model = AppModel()
    @StateObject private var preferences = LearningPreferencesStore()
    @StateObject private var audio = KoreanAudioService()
    @StateObject private var purchases: PurchaseService
    @StateObject private var ads: AdService
    init() {
        let purchases = PurchaseService()
        _purchases = StateObject(wrappedValue:purchases)
        _ads = StateObject(wrappedValue:AdService(purchases:purchases))
    }
    @Environment(\.scenePhase) private var phase
    var body: some Scene {
        WindowGroup {
            RootView()
                .environmentObject(model)
                .environmentObject(audio).environmentObject(preferences)
                .environmentObject(purchases).environmentObject(ads)
                .tint(.indigo)
                .task { purchases.start(); await preferences.reconcile() }
                .onChange(of:phase) { if $0 == .active { Task { await preferences.reconcile() } } }
        }
    }
}
