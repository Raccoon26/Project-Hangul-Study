import SwiftUI

@MainActor
struct RecordsView: View {
    @EnvironmentObject private var model: AppModel
    @Environment(\.scenePhase) private var phase
    @State private var statistics: LearningStatistics?
    @State private var unseenWords = 0
    @State private var error: String?
    @State private var loading = false
    var body: some View {
        List {
            if let statistics = statistics {
                ForEach(statistics.windows) { window in
                    Section(window.title) {
                        LabeledContent("学習アクション",value:String(window.actions))
                        LabeledContent("予定された復習の完了",value:String(window.reviews))
                        LabeledContent("問題の正答率",value:ActivityWindow.accuracy(correct:window.correct,wrong:window.incorrect))
                        LabeledContent("活用・入力（初回回答）",value:ActivityWindow.accuracy(correct:window.productionCorrect,wrong:window.productionWrong))
                        LabeledContent("リスニング（初回回答）",value:ActivityWindow.accuracy(correct:window.listeningCorrect,wrong:window.listeningWrong))
                    }
                }
                Section("単語の学習") {
                    LabeledContent("まだ見ていない",value:String(unseenWords))
                    LabeledContent("学習で確認した",value:String(statistics.seenWords))
                    LabeledContent("回読を通過した",value:String(statistics.passedWords))
                    LabeledContent("長期復習の途中",value:String(statistics.reviewingWords))
                    LabeledContent("長い間隔で復習",value:String(statistics.stableWords))
                    Text("回読通過と長期復習は重なる記録です。長い間隔は30日以上の段階を目安にしており、永久に覚えたという意味ではありません。").font(.footnote).foregroundStyle(.secondary)
                }
                Section("文法の学習") {
                    LabeledContent("学習で確認した",value:String(statistics.studiedGrammar))
                    LabeledContent("長期復習の途中",value:String(statistics.reviewingGrammar))
                    LabeledContent("長い間隔で復習",value:String(statistics.stableGrammar))
                }
            } else if loading { ProgressView("記録を確認中") }
            if let services = model.container {
                Section {
                    NavigationLink("苦手な項目を確認") { SavedContentView(services:services,initial:.difficult) }
                    NavigationLink("維持学習") { MaintenanceView(services:services) }
                }
            }
            Section {
                Text("期間は現在の端末の時間帯で今日を含めて計算します。単語の表示・説明の確認・回答などを学習アクションとして数えます。自己評価は正答率に含みません。途中までの学習も保存されます。学習時間は計測していません。以前のバージョンの入力練習は、再入力も正答率に含まれる場合があります。").font(.footnote).foregroundStyle(.secondary)
            }
            if let error = error { Text(error); Button("読み直す") { Task { await load() } } }
        }.navigationTitle("記録").task { await load() }
            .onChange(of:phase) { if $0 == .active { Task { await load() } } }
            .onReceive(NotificationCenter.default.publisher(for:.NSCalendarDayChanged)) { _ in Task { await load() } }
            .onReceive(NotificationCenter.default.publisher(for:UIApplication.significantTimeChangeNotification)) { _ in Task { await load() } }
    }
    private func load() async {
        guard !loading, let services = model.container else { return }; loading = true
        defer { loading = false }
        do {
            let loaded = try await services.progress.statistics(now:Date(),timeZone:.current)
            var count = 0
            for level in LearningLevel.allCases {
                var after = ""
                while true {
                    try Task.checkCancellation()
                    let ids = try await services.content.curriculumIDs(level:level,kind:"vocabulary",after:after)
                    if ids.isEmpty { break }
                    count += try await services.progress.unseenVocabulary(in:ids)
                    after = ids.last?.rawValue ?? after
                    if ids.count < 200 { break }
                }
            }
            statistics = loaded; unseenWords = count; error = nil
        } catch { self.error = "記録を読み込めませんでした。保存済みの記録は変更していません。" }
    }
}
