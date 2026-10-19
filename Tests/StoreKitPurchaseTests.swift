import XCTest
import StoreKitTest
import StoreKit
@testable import HangulStudy

/// Runs only on macOS/Xcode with an iOS 17+ test destination. No real payment.
@available(iOS 17.0, *)
@MainActor
final class StoreKitPurchaseTests: XCTestCase {
    func testLocalNonConsumablePurchaseColdEntitlementAndRestore() async throws {
        let url = try XCTUnwrap(Bundle(for:Self.self).url(forResource:"RemoveAds",withExtension:"storekit"))
        let store = try SKTestSession(contentsOf:url)
        store.resetToDefaultState()
        store.disableDialogs = true
        store.clearTransactions()
        PurchaseCacheStore().write(nil)
        defer { store.clearTransactions(); PurchaseCacheStore().write(nil) }
        let service = PurchaseService()
        await service.refresh(authoritativeSync:true)
        XCTAssertEqual(service.state,.free)
        await service.loadProduct()
        let product = try XCTUnwrap(service.product)
        XCTAssertEqual(product.id,MonetizationConfiguration.productID)
        XCTAssertFalse(product.displayPrice.isEmpty)
        await service.purchase()
        XCTAssertEqual(service.state,.verified)
        XCTAssertFalse(service.state.permitsAds)
        XCTAssertFalse(service.busy)
        let cold = PurchaseService()
        XCTAssertEqual(cold.state,.offlineProtected)
        await cold.refresh()
        XCTAssertEqual(cold.state,.verified)
        await cold.restore()
        XCTAssertEqual(cold.state,.verified)
    }
}
