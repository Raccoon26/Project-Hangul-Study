import SwiftUI
import StoreKit

@MainActor
struct RemoveAdsView: View {
    @EnvironmentObject private var purchases: PurchaseService
    @EnvironmentObject private var ads: AdService
    @Environment(\.scenePhase) private var phase
    var body: some View {
        Form {
            Section {
                Text("広告を削除").font(.title2.weight(.semibold))
                Text("買い切りの一度きりの購入です。すべての広告を削除します。学習内容や機能は無料でも同じように利用できます。")
                switch purchases.state {
                case .verified:
                    Label("広告削除済み", systemImage:"checkmark")
                case .offlineProtected:
                    Text("以前確認した購入を保護しています。現在、広告は表示しません。購入状態は「購入を復元」から確認できます。")
                case .checking:
                    Text("購入状態を確認しています。学習はそのまま利用できます。")
                case .free, .verificationFailed:
                    if let product = purchases.product {
                        Button("広告を削除 — \(product.displayPrice)") { Task { await purchases.purchase() } }
                            .frame(minHeight:44).disabled(purchases.busy)
                    } else {
                        Button("価格を読み込む") { Task { await purchases.loadProduct() } }
                            .frame(minHeight:44).disabled(purchases.loadingProduct || purchases.busy)
                    }
                }
                if purchases.busy { Text("App Storeで確認中です…").foregroundStyle(.secondary) }
                Button("購入を復元") { Task { await purchases.restore() } }
                    .frame(minHeight:44).disabled(purchases.busy)
                if let message = purchases.message { Text(message).font(.footnote).foregroundStyle(.secondary) }
            }
            if ads.configuration.enabled {
                Section("広告のプライバシー") {
                    Button("プライバシー設定を確認・変更") { Task { await ads.showPrivacyOptions() } }
                        .frame(minHeight:44).disabled(ads.privacyBusy || purchases.busy)
                    Text("必要な同意を確認できない場合、広告は表示しません。学習機能には影響しません。")
                        .font(.footnote).foregroundStyle(.secondary)
                    if let message = ads.privacyMessage { Text(message).font(.footnote) }
                }
            }
        }.navigationTitle("広告を削除").navigationBarTitleDisplayMode(.inline)
            .onDisappear { ads.cancelPrivacyPresentation() }
            .onChange(of:phase) { if $0 != .active { ads.cancelPrivacyPresentation() } }
            .task {
                if !purchases.state.protectsPurchase { await purchases.loadProduct() }
                if !purchases.state.protectsPurchase { await ads.updatePrivacyInformation() }
            }
    }
}
