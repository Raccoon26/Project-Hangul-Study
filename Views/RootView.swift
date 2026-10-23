import SwiftUI

@MainActor
struct RootView: View {
    @EnvironmentObject private var model: AppModel
    var body: some View {
        Group {
            if model.container != nil {
                TabView {
                    NavigationStack { LearnView().tint(.indigo) }
                        .tabItem { Label("学ぶ", systemImage: "book") }
                    NavigationStack { LookupView().tint(.indigo) }
                        .tabItem { Label("調べる", systemImage: "magnifyingglass") }
                    NavigationStack { RecordsView().tint(.indigo) }
                        .tabItem { Label("記録", systemImage: "chart.bar") }
                    NavigationStack { SettingsView().tint(.indigo) }
                        .tabItem { Label("設定", systemImage: "gearshape") }
                }.tint(.primary)
                .alert("確認", isPresented: Binding(get: { model.errorMessage != nil }, set: { if !$0 { model.errorMessage = nil } })) {
                    Button("閉じる", role: .cancel) { model.errorMessage = nil }
                } message: { Text(model.errorMessage ?? "") }
            } else if let error = model.errorMessage {
                VStack(spacing: 24) {
                    Image(systemName: "exclamationmark.circle").font(.largeTitle)
                    Text("データを開けませんでした").font(.headline)
                    Text(error).font(.body)
                    Button("もう一度試す") { Task { await model.open() } }
                        .buttonStyle(.borderedProminent).controlSize(.large)
                }.padding(24)
            } else {
                ProgressView("読み込み中")
            }
        }.task { await model.open() }
    }
}

@MainActor
struct FixtureNotice: View {
    var body: some View {
        Label("開発用サンプルです。学習教材の完成版ではありません", systemImage: "info.circle")
            .font(.footnote).foregroundStyle(.secondary)
            .fixedSize(horizontal: false, vertical: true)
    }
}
