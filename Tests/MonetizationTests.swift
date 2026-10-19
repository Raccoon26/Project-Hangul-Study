import XCTest
@testable import HangulStudy

final class MonetizationTests: XCTestCase {
    private let now = Date(timeIntervalSince1970:2_000_000_000)
    private func boundary(items: Int = 20, seconds: Double = 720, resumed: Bool = false) -> AdBoundary {
        AdBoundary(sessionID:UUID(),uniqueItems:items,foregroundSeconds:seconds,resumed:resumed)
    }
    func testOnlyConfirmedFreeStatePermitsAds() {
        for state in [AdEntitlementState.checking,.verified,.offlineProtected,.verificationFailed] {
            XCTAssertFalse(state.permitsAds)
        }
        XCTAssertTrue(AdEntitlementState.free.permitsAds)
    }
    func testPurchaseSuccessImmediatelyBlocksAds() {
        XCTAssertEqual(AdEntitlementState.free.applying(.verifiedActive,hasVerifiedCache:false),.verified)
    }
    func testPendingAndCancellationNeverGrantEntitlement() {
        for event in [AdEntitlementState.Event.pending,.cancelled] {
            XCTAssertEqual(AdEntitlementState.free.applying(event,hasVerifiedCache:false),.free)
        }
    }
    func testUnverifiedDoesNotGrantAndProtectsPreviousVerifiedPurchase() {
        XCTAssertEqual(AdEntitlementState.free.applying(.unverified,hasVerifiedCache:false),.verificationFailed)
        XCTAssertEqual(AdEntitlementState.checking.applying(.unverified,hasVerifiedCache:true),.offlineProtected)
        XCTAssertEqual(AdEntitlementState.verified.applying(.unverified,hasVerifiedCache:true),.verified)
    }
    func testVerifiedRevocationOverridesCache() {
        XCTAssertEqual(AdEntitlementState.offlineProtected.applying(.verifiedRevoked,hasVerifiedCache:true),.free)
    }
    func testShortSessionsNeverQualifyEvenWithBacklog() {
        let cap = AdFrequencyState(completedItems:200)
        for seconds in [0.0,180,300,600,719] {
            XCTAssertFalse(cap.permits(boundary(seconds:seconds),entitlement:.free,now:now))
        }
        for items in [0,1,2,4,7,19] {
            XCTAssertFalse(cap.permits(boundary(items:items,seconds:900),entitlement:.free,now:now))
        }
    }
    func testResumeAndInvalidElapsedTimeNeverQualify() {
        let cap = AdFrequencyState(completedItems:200)
        XCTAssertFalse(cap.permits(boundary(resumed:true),entitlement:.free,now:now))
        XCTAssertFalse(cap.permits(boundary(seconds:.infinity),entitlement:.free,now:now))
        XCTAssertFalse(cap.permits(boundary(seconds:.nan),entitlement:.free,now:now))
    }
    func testLongBoundaryNeedsLearningVolumeAndTimeCap() {
        var cap = AdFrequencyState()
        let b = boundary()
        XCTAssertTrue(cap.record(boundary())); XCTAssertTrue(cap.record(boundary()))
        XCTAssertFalse(cap.permits(b,entitlement:.free,now:now))
        XCTAssertTrue(cap.record(b)); XCTAssertTrue(cap.permits(b,entitlement:.free,now:now))
        cap.presented(at:now)
        cap.completedItems = 100
        XCTAssertFalse(cap.permits(boundary(),entitlement:.free,now:now.addingTimeInterval(1799)))
        XCTAssertTrue(cap.permits(boundary(),entitlement:.free,now:now.addingTimeInterval(1800)))
        XCTAssertFalse(cap.permits(boundary(),entitlement:.free,now:now.addingTimeInterval(-3600)))
    }
    func testPaidUserNeverEligibleForLongBoundary() {
        let cap = AdFrequencyState(completedItems:1000)
        for state in [AdEntitlementState.verified,.offlineProtected,.checking,.verificationFailed] {
            XCTAssertFalse(cap.permits(boundary(),entitlement:state,now:now))
        }
    }
    func testDuplicateCompletionAndColdFrequencyRestore() throws {
        var cap = AdFrequencyState(); let b = boundary()
        XCTAssertTrue(cap.record(b)); XCTAssertFalse(cap.record(b)); XCTAssertEqual(cap.completedItems,20)
        cap.presented(at:now)
        let restored = try JSONDecoder().decode(AdFrequencyState.self,from:JSONEncoder().encode(cap))
        XCTAssertEqual(restored,cap); XCTAssertEqual(restored.completedItems,0)
    }
    func testProductionMissingAndTestIDsRejected() {
        XCTAssertFalse(MonetizationConfiguration(appID:"",interstitialID:"",development:false).enabled)
        let bundle = Bundle.main
        let app = bundle.object(forInfoDictionaryKey:"GADApplicationIdentifier") as? String ?? ""
        let unit = bundle.object(forInfoDictionaryKey:"AdMobInterstitialIdentifier") as? String ?? ""
        #if DEBUG
        XCTAssertTrue(MonetizationConfiguration(appID:app,interstitialID:unit,development:true).enabled)
        XCTAssertFalse(MonetizationConfiguration(appID:app,interstitialID:unit,development:false).enabled)
        #endif
        XCTAssertFalse(MonetizationConfiguration(appID:"$(ADMOB_APP_ID)",interstitialID:unit,development:false).enabled)
    }
    func testBoundaryHistoryIsBounded() {
        var cap = AdFrequencyState()
        for _ in 0..<200 { _ = cap.record(boundary()) }
        XCTAssertEqual(cap.recentBoundaries.count,100)
    }
}
