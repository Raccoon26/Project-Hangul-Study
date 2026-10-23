import Foundation
import StoreKit
import Security
import Combine

struct VerifiedPurchaseCache: Codable, Equatable {
    let productID: String
    let transactionID: UInt64
    let purchaseDate: Date
}

enum PurchaseCacheRead {
    case missing, verified(VerifiedPurchaseCache), unavailable(OSStatus)
    var value: VerifiedPurchaseCache? {
        if case .verified(let value) = self { return value }; return nil
    }
    var initialState: AdEntitlementState {
        switch self {
        case .missing: return .checking
        case .verified: return .offlineProtected
        case .unavailable: return .verificationFailed
        }
    }
}
protocol PurchaseCacheStoring {
    func load() -> PurchaseCacheRead
    @discardableResult func write(_ value: VerifiedPurchaseCache?) -> OSStatus
}
extension PurchaseCacheStoring {
    func read() -> VerifiedPurchaseCache? { load().value }
}

/// Device-only cache. Never used as proof of purchase, and never written for pending,
/// cancelled or unverified results. StoreKit's locally verified transactions are authoritative.
struct PurchaseCacheStore: PurchaseCacheStoring {
    #if DEBUG
    private let service = "HangulStudy.purchase.debug.v1"
    #else
    private let service = "HangulStudy.purchase.release.v1"
    #endif
    private var query: [String: Any] {
        [kSecClass as String:kSecClassGenericPassword, kSecAttrService as String:service,
         kSecAttrAccount as String:MonetizationConfiguration.productID]
    }
    func load() -> PurchaseCacheRead {
        var lookup = query
        lookup[kSecReturnData as String] = true
        lookup[kSecMatchLimit as String] = kSecMatchLimitOne
        var result: CFTypeRef?
        let status = SecItemCopyMatching(lookup as CFDictionary, &result)
        if status == errSecItemNotFound { return .missing }
        guard status == errSecSuccess else { return .unavailable(status) }
        guard let data = result as? Data,
              let value = try? JSONDecoder().decode(VerifiedPurchaseCache.self, from:data),
              value.productID == MonetizationConfiguration.productID else { return .unavailable(errSecDecode) }
        return .verified(value)
    }
    @discardableResult func write(_ value: VerifiedPurchaseCache?) -> OSStatus {
        guard let value else {
            let status = SecItemDelete(query as CFDictionary)
            return status == errSecItemNotFound ? errSecSuccess : status
        }
        guard let data = try? JSONEncoder().encode(value) else { return errSecParam }
        let attributes: [String:Any] = [kSecValueData as String:data,
            kSecAttrAccessible as String:kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly]
        let status = SecItemUpdate(query as CFDictionary, attributes as CFDictionary)
        if status == errSecItemNotFound {
            var insert = query; attributes.forEach { insert[$0.key] = $0.value }
            return SecItemAdd(insert as CFDictionary, nil)
        }
        return status
    }
}

@MainActor
final class PurchaseService: ObservableObject {
    @Published private(set) var state: AdEntitlementState
    @Published private(set) var product: Product?
    @Published private(set) var busy = false
    @Published private(set) var loadingProduct = false
    @Published private(set) var message: String?
    private let cache: any PurchaseCacheStoring
    private var cacheSaveFailed = false
    private var listener: Task<Void, Never>?
    private var refreshTask: Task<Void, Never>?
    private var generation = 0
    private var started = false
    init(cache: any PurchaseCacheStoring = PurchaseCacheStore()) {
        self.cache = cache; state = cache.load().initialState
    }
    deinit { listener?.cancel(); refreshTask?.cancel() }

    func start() {
        guard !started else { return }; started = true
        listener = Task { [weak self] in
            for await result in Transaction.updates {
                guard !Task.isCancelled else { return }
                await self?.receive(result)
            }
        }
        refreshTask = Task { [weak self] in await self?.refresh() }
    }
    func loadProduct() async {
        guard !loadingProduct, product == nil else { return }
        loadingProduct = true; message = nil; defer { loadingProduct = false }
        do {
            product = try await Product.products(for:[MonetizationConfiguration.productID])
                .first { $0.id == MonetizationConfiguration.productID && $0.type == .nonConsumable }
            if product == nil { message = "現在、購入情報を取得できません。時間を置いてお試しください。学習はそのまま利用できます。" }
        } catch { message = "購入情報を取得できませんでした。接続を確認して、もう一度お試しください。" }
    }
    func purchase() async {
        guard !busy, let product, !state.protectsPurchase, state != .checking else { return }
        busy = true; message = nil; defer { busy = false }
        do {
            switch try await product.purchase() {
            case .success(let verification): await receive(verification)
            case .pending: state = state.applying(.pending, hasVerifiedCache:cache.read() != nil); message = "購入の承認を待っています。承認されると広告が削除されます。"
            case .userCancelled: state = state.applying(.cancelled, hasVerifiedCache:cache.read() != nil)
            @unknown default: message = "購入状態を確認できませんでした。「購入を復元」から確認できます。"
            }
        } catch { message = "購入を完了できませんでした。時間を置いて、もう一度お試しください。" }
    }
    func restore() async {
        guard !busy else { return }; busy = true; message = nil
        defer { busy = false }
        do {
            try await AppStore.sync()
            await refresh(authoritativeSync:true)
            if state == .verified && !cacheSaveFailed { message = "購入を復元しました。広告は表示されません。" }
            else if state == .free { message = "復元できる購入は見つかりませんでした。購入時のApple Accountをご確認ください。" }
        } catch { message = "購入を復元できませんでした。接続とApple Accountをご確認ください。以前確認した購入は保護されます。" }
    }
    func refresh(authoritativeSync: Bool = false) async {
        let scanGeneration = generation
        var owned: Transaction?
        var unverifiable = false
        for await result in Transaction.currentEntitlements {
            switch result {
            case .verified(let transaction):
                if matches(transaction), transaction.revocationDate == nil, !transaction.isUpgraded { owned = transaction }
            case .unverified(let transaction, _):
                if transaction.productID == MonetizationConfiguration.productID { unverifiable = true }
            }
        }
        // A transaction update or purchase arriving during the scan wins over stale results.
        guard generation == scanGeneration else { return }
        if let owned { apply(owned); return }
        if unverifiable { state = cache.read() == nil ? .verificationFailed : .offlineProtected; return }
        // Latest verified revocation must beat the offline cache, including missed updates.
        if let latest = await Transaction.latest(for:MonetizationConfiguration.productID) {
            guard generation == scanGeneration else { return }
            switch latest {
            case .verified(let transaction):
                if matches(transaction) { apply(transaction); return }
            case .unverified:
                state = cache.read() == nil ? .verificationFailed : .offlineProtected
                return
            }
        }
        guard generation == scanGeneration else { return }
        if authoritativeSync {
            state = cache.write(nil) == errSecSuccess ? .free : .verificationFailed
        } else {
            switch cache.load() {
            case .missing: state = .free
            case .verified: state = .offlineProtected
            case .unavailable: state = .verificationFailed
            }
        }
    }
    private func matches(_ transaction: Transaction) -> Bool {
        transaction.productID == MonetizationConfiguration.productID && transaction.productType == .nonConsumable
    }
    private func apply(_ transaction: Transaction) {
        generation += 1
        if transaction.revocationDate != nil || transaction.isUpgraded {
            cache.write(nil); state = state.applying(.verifiedRevoked, hasVerifiedCache:false)
        } else {
            cacheSaveFailed = cache.write(VerifiedPurchaseCache(productID:transaction.productID,
                transactionID:transaction.id, purchaseDate:transaction.purchaseDate)) != errSecSuccess
            state = state.applying(.verifiedActive, hasVerifiedCache:true)
            if cacheSaveFailed { message = "購入は確認できましたが、端末に保護用の記録を保存できませんでした。再起動後は購入状態を再確認します。学習はそのまま利用できます。" }
        }
    }
    private func receive(_ result: VerificationResult<Transaction>) async {
        switch result {
        case .verified(let transaction):
            guard matches(transaction) else { return }
            apply(transaction)
            if state == .verified && !cacheSaveFailed { message = "広告を削除しました。ご購入ありがとうございます。" }
            await transaction.finish()
        case .unverified(let transaction, _):
            guard transaction.productID == MonetizationConfiguration.productID else { return }
            // Do not grant or finish an unverified transaction.
            generation += 1
            state = state.applying(.unverified, hasVerifiedCache:cache.read() != nil)
            message = "購入を確認できませんでした。時間を置いて「購入を復元」をお試しください。"
        }
    }
}
