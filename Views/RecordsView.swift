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
                    Section {
                        LearningValueRow("学習アクション",value:String(window.actions))
                        LearningValueRow("予定された復習の完了",value:String(window.reviews))
                        LearningValueRow("問題の正答率",value:ActivityWindow.accuracy(correct:window.correct,wrong:window.incorrect))
                        LearningValueRow("活用・入力（初回回答）",value:ActivityWindow.accuracy(correct:window.productionCorrect,wrong:window.productionWrong))
                        LearningValueRow("リスニング（初回回答）",value:ActivityWindow.accuracy(correct:window.listeningCorrect,wrong:window.listeningWrong))
                    } header: { Text(window.title).foregroundStyle(Color.primary).fixedSize(horizontal:false,vertical:true) }
                }
                Section {
                    LearningValueRow("まだ見ていない",value:String(unseenWords))
                    LearningValueRow("学習で確認した",value:String(statistics.seenWords))
                    LearningValueRow("回読を通過した",value:String(statistics.passedWords))
                    LearningValueRow("長期復習の途中",value:String(statistics.reviewingWords))
                    LearningValueRow("長い間隔で復習",value:String(statistics.stableWords))
                    Text("回読通過と長期復習は重なる記録です。長い間隔は30日以上の段階を目安にしており、永久に覚えたという意味ではありません。").font(.footnote).foregroundStyle(Color.primary).fixedSize(horizontal:false,vertical:true)
                } header: { Text("単語の学習").foregroundStyle(Color.primary).fixedSize(horizontal:false,vertical:true) }
                Section {
                    LearningValueRow("学習で確認した",value:String(statistics.studiedGrammar))
                    LearningValueRow("長期復習の途中",value:String(statistics.reviewingGrammar))
                    LearningValueRow("長い間隔で復習",value:String(statistics.stableGrammar))
                } header: { Text("文法の学習").foregroundStyle(Color.primary).fixedSize(horizontal:false,vertical:true) }
            } else if loading { ProgressView("記録を確認中") }
            if let services = model.container {
                Section {
                    NavigationLink("苦手な項目を確認") { SavedContentView(services:services,initial:.difficult) }.learningRow()
                    NavigationLink("維持学習") { MaintenanceView(services:services) }.learningRow()
                }
            }
            Section {
                Text("期間は現在の端末の時間帯で今日を含めて計算します。単語の表示・説明の確認・回答などを学習アクションとして数えます。自己評価は正答率に含みません。途中までの学習も保存されます。学習時間は計測していません。以前のバージョンの入力練習は、再入力も正答率に含まれる場合があります。").font(.footnote).foregroundStyle(Color.primary).fixedSize(horizontal:false,vertical:true).accessibilityIdentifier("statistics-note")
            }
            if let error = error { Text(error); Button("読み直す") { Task { await load() } } }
        }.navigationTitle("記録").navigationBarTitleDisplayMode(.inline).task { await load() }
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

/// Keep the label and value readable without competing for one narrow line.
@MainActor
struct LearningValueRow: View {
    let title: String
    let value: String
    let valueIdentifier: String
    @Environment(\.dynamicTypeSize) private var dynamicTypeSize
    init(_ title: String, value: String, valueIdentifier: String = "") {
        self.title = title; self.value = value; self.valueIdentifier = valueIdentifier
    }
    var body: some View {
        // Preserve the same Text/AX identities while the arrangement changes.
        let layout = dynamicTypeSize.isAccessibilitySize
            ? AnyLayout(VStackLayout(alignment:.leading,spacing:8))
            : AnyLayout(HStackLayout(alignment:.firstTextBaseline,spacing:16))
        layout {
            label.frame(maxWidth:.infinity,alignment:.leading)
            number.frame(maxWidth:dynamicTypeSize.isAccessibilitySize ? .infinity : nil,alignment:.leading)
        }.font(.body).foregroundStyle(Color.primary).fixedSize(horizontal:false,vertical:true)
    }
    private var label: some View { Text(title).fixedSize(horizontal:false,vertical:true) }
    private var number: some View {
        Text(value).fixedSize(horizontal:false,vertical:true).accessibilityIdentifier(valueIdentifier)
    }
}
