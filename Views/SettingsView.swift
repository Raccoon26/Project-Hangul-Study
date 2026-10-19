import SwiftUI

@MainActor
struct SettingsView: View {
    @EnvironmentObject private var model: AppModel
    @EnvironmentObject private var preferences: LearningPreferencesStore
    @Environment(\.scenePhase) private var phase
    @Environment(\.openURL) private var openURL
    var body: some View {
        Form {
            Section("短い復習") {
                Picker("新しく始める復習の量",selection:Binding(get:{preferences.value.amount},set:{preferences.setAmount($0)})) {
                    ForEach(StudyAmount.allCases,id:\.rawValue) { Text($0.title).tag($0) }
                }
                Text("短い単語復習の目安です。途中で閉じても保存されます。始めている復習の内容は変更しません。").font(.footnote).foregroundStyle(.secondary)
            }
            Section("学習のリマインダー") {
                Toggle("毎日通知する",isOn:Binding(get:{preferences.value.reminderEnabled},set:{enabled in Task { await preferences.setReminder(enabled) }}))
                    .disabled(preferences.busy)
                DatePicker("時間",selection:Binding(get:{preferences.reminderDate},set:{date in Task { await preferences.setTime(date) }}),displayedComponents:.hourAndMinute)
                    .disabled(preferences.busy)
                Text("端末の時刻で通知します。復習の有無にかかわらず、学習のきっかけをお知らせします。").font(.footnote).foregroundStyle(.secondary)
                if preferences.denied {
                    Text("通知はiPhoneの設定で許可できます。通知なしでもすべての学習を利用できます。").font(.footnote)
                    Button("iPhoneの設定を開く") { if let url = URL(string:UIApplication.openSettingsURLString) { openURL(url) } }.frame(minHeight:44)
                }
                if let message = preferences.message { Text(message).font(.footnote) }
            }
            Section("表示・音声") {
                Text("文字サイズと外観はiPhoneの設定に従います。")
                Text("音声は各画面で通常・ゆっくりを選べます。単語と文法は音声なしでも学習できます。個別発音の確認には検証済みの録音を使用します。").foregroundStyle(.secondary)
            }
            Section { NavigationLink("広告を削除・購入を復元") { RemoveAdsView() } }
            Section("データ") {
                Text("教材と学習記録はこの端末で利用できます。音声は端末の韓国語音声の利用状況によります。")
                Text("アプリを削除すると端末内の記録も削除されます。別の端末への同期はありません。").foregroundStyle(.secondary)
                LabeledContent("教材バージョン",value:String(model.container?.metadata.contentVersion ?? 0))
                if model.container?.metadata.isFixture == true { FixtureNotice() }
            }
        }.navigationTitle("設定")
            .task { await preferences.reconcile() }
            .onChange(of:phase) { if $0 == .active { Task { await preferences.reconcile() } } }
    }
}
