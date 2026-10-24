import Foundation
import UIKit
import Combine
#if !HANGUL_ADS_DISABLED
import GoogleMobileAds
import UserMessagingPlatform

/// No learning repository dependency. Ads never own completion, navigation or progress.
@MainActor
final class AdService: NSObject, ObservableObject, FullScreenContentDelegate {
    @Published private(set) var privacyBusy = false
    @Published private(set) var privacyMessage: String?
    @Published private(set) var privacyRequired = false
    let configuration: MonetizationConfiguration
    private let purchases: PurchaseService
    private let defaults: UserDefaults
    private static let frequencyKey = "monetization.frequency.v1"
    private var frequency: AdFrequencyState
    private var purchaseObservation: AnyCancellable?
    private var interstitial: InterstitialAd?
    private var presentedAd: InterstitialAd?
    private var loadedAt: Date?
    private var loading = false
    private var sdkStarted = false
    private var consentUpdated = false
    private var consentUpdating = false
    private var generation = 0
    private var presenting = false
    private var privacyPresentationID: UUID?
    private var requestAttemptedAt: Date?

    init(purchases: PurchaseService, configuration: MonetizationConfiguration = .current,
         defaults: UserDefaults = .standard) {
        self.purchases = purchases; self.configuration = configuration; self.defaults = defaults
        frequency = defaults.data(forKey:Self.frequencyKey).flatMap { try? JSONDecoder().decode(AdFrequencyState.self, from:$0) } ?? AdFrequencyState()
        super.init()
        purchaseObservation = purchases.$state.sink { [weak self] state in
            if !state.permitsAds { self?.discard() }
        }
    }
    private var mayRequestAds: Bool {
        // Official demo units ONLY in Debug. No publisher account/UMP message exists yet.
        // Release never takes this path, and always requires a fresh UMP check.
        configuration.enabled && (configuration.development ||
            (consentUpdated && ConsentInformation.shared.canRequestAds))
    }
    private func discard() { generation += 1; interstitial = nil; loadedAt = nil }
    private func saveFrequency() {
        if let data = try? JSONEncoder().encode(frequency) { defaults.set(data, forKey:Self.frequencyKey) }
    }
    /// Once per launch, asynchronously, without showing any permission/form at startup.
    func updatePrivacyInformation() async {
        guard configuration.enabled, !consentUpdated, !consentUpdating else { return }
        consentUpdating = true; defer { consentUpdating = false }
        let error: Error? = await withCheckedContinuation { continuation in
            ConsentInformation.shared.requestConsentInfoUpdate(with:RequestParameters()) { error in
                continuation.resume(returning:error)
            }
        }
        consentUpdated = error == nil
        privacyRequired = ConsentInformation.shared.privacyOptionsRequirementStatus == .required
        if error != nil { privacyMessage = "広告の設定を確認できませんでした。学習はそのまま利用できます。" }
    }
    /// User-initiated only; never overlays onboarding or a learning card.
    func showPrivacyOptions() async {
        guard configuration.enabled, !privacyBusy, !presenting else { return }
        privacyBusy = true; privacyMessage = nil; discard()
        let presentationID = UUID(); privacyPresentationID = presentationID
        defer { privacyBusy = false; privacyPresentationID = nil }
        await updatePrivacyInformation()
        guard consentUpdated, privacyPresentationID == presentationID,
              UIApplication.shared.applicationState == .active else { return }
        do {
            if ConsentInformation.shared.canRequestAds && privacyRequired {
                try await ConsentForm.presentPrivacyOptionsForm(from:nil)
            } else {
                try await ConsentForm.loadAndPresentIfRequired(from:nil)
            }
            privacyRequired = ConsentInformation.shared.privacyOptionsRequirementStatus == .required
            privacyMessage = "広告のプライバシー設定を確認しました。"
        } catch { privacyMessage = "現在、広告の設定を表示できません。時間を置いてお試しください。" }
    }
    /// A delayed consent response must not open a form over a different learning screen.
    func cancelPrivacyPresentation() { privacyPresentationID = nil }
    /// Opportunistic preload. No spinner, no automatic presentation when the request finishes.
    func prepare() async {
        guard configuration.enabled, purchases.state.permitsAds, !purchases.busy, !loading, !presenting, !privacyBusy else { return }
        if !configuration.development { await updatePrivacyInformation() }
        guard mayRequestAds, purchases.state.permitsAds,
              !loading, !presenting, !privacyBusy else { return }
        if interstitial != nil, let loadedAt, Date().timeIntervalSince(loadedAt) < 50 * 60 { return }
        // No polling or retry loop; at most one request per ten minutes on a learning entry.
        if let attempted = requestAttemptedAt, Date().timeIntervalSince(attempted) < 10 * 60 { return }
        requestAttemptedAt = Date(); loading = true
        defer { loading = false }
        discard(); let requestGeneration = generation
        if !sdkStarted {
            sdkStarted = true
            MobileAds.shared.requestConfiguration.setPublisherFirstPartyIDEnabled(false)
            MobileAds.shared.start(completionHandler:nil)
        }
        let request = Request()
        let extras = Extras(); extras.additionalParameters = ["npa":"1"]
        request.register(extras)
        do {
            let loaded = try await InterstitialAd.load(with:configuration.interstitialID, request:request)
            guard requestGeneration == generation, purchases.state.permitsAds,
                  mayRequestAds, !privacyBusy else { return }
            loaded.fullScreenContentDelegate = self
            interstitial = loaded; loadedAt = Date()
        } catch { interstitial = nil; loadedAt = nil }
    }
    /// Synchronous optional side effect AFTER the learning transaction returned success.
    /// Never wait for an ad and never present from a load callback.
    func completed(_ boundary: AdBoundary, stopAudio: () -> Void) {
        guard frequency.record(boundary) else { return }
        saveFrequency()
        let now = Date()
        guard mayRequestAds, !purchases.busy,
              !privacyBusy, !presenting,
              frequency.permits(boundary, entitlement:purchases.state, now:now),
              UIApplication.shared.applicationState == .active,
              let ad = interstitial, let loadedAt, now.timeIntervalSince(loadedAt) >= 0,
              now.timeIntervalSince(loadedAt) < 50 * 60,
              let controller = Self.visibleController(), !controller.isBeingDismissed,
              !controller.isBeingPresented, controller.viewIfLoaded?.window != nil else { return }
        do { try ad.canPresent(from:controller) } catch { discard(); return }
        // Consume before presentation: double callbacks, process death or a failed show
        // cannot bypass the cap. Conservative counting may skip an additional ad.
        guard purchases.state.permitsAds else { discard(); return }
        frequency.presented(at:now); saveFrequency()
        presenting = true; presentedAd = ad; interstitial = nil; self.loadedAt = nil
        stopAudio()
        ad.present(from:controller)
    }
    private static func visibleController() -> UIViewController? {
        let scenes = UIApplication.shared.connectedScenes.compactMap { $0 as? UIWindowScene }
            .filter { $0.activationState == .foregroundActive }
        guard let root = scenes.flatMap(\.windows).first(where: \.isKeyWindow)?.rootViewController else { return nil }
        var current = root
        while let next = current.presentedViewController { current = next }
        if current is UIAlertController { return nil }
        return current
    }
    func adDidDismissFullScreenContent(_ ad: FullScreenPresentingAd) {
        guard let current = presentedAd, (ad as AnyObject) === current else { return }
        presenting = false; presentedAd = nil
    }
    func ad(_ ad: FullScreenPresentingAd, didFailToPresentFullScreenContentWithError error: Error) {
        guard let current = presentedAd, (ad as AnyObject) === current else { return }
        presenting = false; presentedAd = nil; discard()
    }
}
#else
/// The ads-disabled build must not load the SDK: its load-time initializer can
/// terminate the process before a runtime configuration guard can run.
@MainActor
final class AdService: ObservableObject {
    @Published private(set) var privacyBusy = false
    @Published private(set) var privacyMessage: String?
    @Published private(set) var privacyRequired = false
    let configuration: MonetizationConfiguration
    private let defaults: UserDefaults
    private static let frequencyKey = "monetization.frequency.v1"
    private var frequency: AdFrequencyState

    init(purchases: PurchaseService, configuration: MonetizationConfiguration = .current,
         defaults: UserDefaults = .standard) {
        self.configuration = configuration; self.defaults = defaults
        frequency = defaults.data(forKey:Self.frequencyKey).flatMap {
            try? JSONDecoder().decode(AdFrequencyState.self,from:$0)
        } ?? AdFrequencyState()
    }
    func prepare() async {}
    func updatePrivacyInformation() async {}
    func showPrivacyOptions() async {}
    func cancelPrivacyPresentation() {}
    func completed(_ boundary: AdBoundary, stopAudio: () -> Void) {
        // Retain the existing frequency history across future ads-enabled builds.
        guard frequency.record(boundary), let data = try? JSONEncoder().encode(frequency) else { return }
        defaults.set(data,forKey:Self.frequencyKey)
    }
}
#endif
