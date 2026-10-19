import Foundation

/// Only StoreKit verification grants entitlement. A prior verified cache protects ads
/// during uncertainty, but is deliberately a different state from verified ownership.
enum AdEntitlementState: Equatable {
    case checking, free, verified, offlineProtected, verificationFailed
    enum Event { case verifiedActive, verifiedRevoked, cancelled, pending, unverified }
    func applying(_ event: Event, hasVerifiedCache: Bool) -> Self {
        switch event {
        case .verifiedActive: return .verified
        case .verifiedRevoked: return .free
        case .cancelled, .pending: return self
        case .unverified:
            if self == .verified { return .verified }
            return hasVerifiedCache ? .offlineProtected : .verificationFailed
        }
    }
    var permitsAds: Bool { self == .free }
    var protectsPurchase: Bool { self == .verified || self == .offlineProtected }
}

struct MonetizationConfiguration {
    let appID: String
    let interstitialID: String
    let development: Bool
    static let productID = "remove_ads"
    static var current: Self {
        #if DEBUG
        let development = true
        #else
        let development = false
        #endif
        return Self(appID: Bundle.main.object(forInfoDictionaryKey: "GADApplicationIdentifier") as? String ?? "",
                    interstitialID: Bundle.main.object(forInfoDictionaryKey: "AdMobInterstitialIdentifier") as? String ?? "",
                    development: development)
    }
    var enabled: Bool {
        let app = appID.range(of: "^ca-app-pub-[0-9]{16}~[0-9]{10}$", options: .regularExpression) != nil
        let unit = interstitialID.range(of: "^ca-app-pub-[0-9]{16}/[0-9]{10}$", options: .regularExpression) != nil
        let testPublisher = "3940256099942544"
        if development { return app && unit && appID.contains(testPublisher) && interstitialID.contains(testPublisher) }
        return app && unit && !appID.contains(testPublisher) && !interstitialID.contains(testPublisher)
            && appID.split(separator:"~").first == interstitialID.split(separator:"/").first
    }
}

struct AdBoundary: Equatable {
    let sessionID: UUID
    let uniqueItems: Int
    let foregroundSeconds: TimeInterval
    let resumed: Bool
}

struct AdFrequencyState: Codable, Equatable {
    var completedItems = 0
    var lastPresentation: Date?
    var recentBoundaries: [UUID] = []

    /// Must be called only after a committed completion; duplicate callbacks do nothing.
    mutating func record(_ boundary: AdBoundary) -> Bool {
        guard !recentBoundaries.contains(boundary.sessionID) else { return false }
        recentBoundaries.append(boundary.sessionID)
        recentBoundaries = Array(recentBoundaries.suffix(100))
        completedItems = min(10_000, completedItems + max(0, boundary.uniqueItems))
        return true
    }
    func permits(_ boundary: AdBoundary, entitlement: AdEntitlementState, now: Date) -> Bool {
        guard entitlement.permitsAds, !boundary.resumed, boundary.uniqueItems >= 20,
              boundary.foregroundSeconds >= 12 * 60, boundary.foregroundSeconds.isFinite,
              completedItems >= 60 else { return false }
        // Clock rollback is conservative: it cannot bypass the cap.
        return lastPresentation.map { now.timeIntervalSince($0) >= 30 * 60 } ?? true
    }
    mutating func presented(at now: Date) { lastPresentation = now; completedItems = 0 }
}
