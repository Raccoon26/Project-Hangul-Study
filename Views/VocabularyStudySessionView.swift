import SwiftUI

@MainActor
struct VocabularyStudySessionView: View {
    @Environment(\.dismiss) private var dismiss
    @Environment(\.scenePhase) private var scenePhase
    @EnvironmentObject private var audio: KoreanAudioService
    @EnvironmentObject private var purchases: PurchaseService
    @EnvironmentObject private var ads: AdService
    @State private var openedAt = Date()
    @State private var activeSince = ProcessInfo.processInfo.systemUptime
    @State private var interrupted = false
    @State private var visible = false
    @StateObject private var model: VocabularyStudyViewModel
    init(services: AppContainer, set: VocabularyStudySet) {
        _model = StateObject(wrappedValue: VocabularyStudyViewModel(services: services, set: set))
    }
    var body: some View {
        VStack(spacing: 0) {
            header
            if let state = model.session, !state.completed {
                ProgressView(value: Double(state.position), total: Double(state.order.count))
                    .padding(.horizontal, 24).accessibilityLabel("この周の進み具合")
                    .accessibilityValue("\(state.position) / \(state.order.count)語を確認済み")
            }
            ScrollViewReader { proxy in
                ScrollView {
                    VStack(alignment: .leading, spacing: 24) {
                        if let state = model.session {
                            if state.completed { completion(state) }
                            else if state.needsNextRound { roundSummary(state) }
                            else if let card = model.card { VocabularyCardContentView(card: card, revealed: state.revealed).id(card.id) }
                        }
                        if model.busy && model.card == nil { ProgressView("読み込み中") }
                        if let error = model.errorMessage {
                            Text(error).foregroundStyle(.secondary)
                            Button("記録を読み直す") { Task { await model.reload() } }
                                .buttonStyle(.bordered).controlSize(.large).disabled(model.busy)
                        }
                    }.frame(maxWidth: 600, alignment: .leading).padding(24)
                        .frame(maxWidth: .infinity).id("word-top")
                }.onChange(of: model.session?.currentID) { _ in
                    proxy.scrollTo("word-top", anchor: .top)
                }.onChange(of: model.session?.id) { _ in proxy.scrollTo("word-top", anchor: .top) }
            }
        }.background(Color(uiColor: .systemBackground))
            .safeAreaInset(edge: .bottom, spacing: 0) { actions }
            .interactiveDismissDisabled(model.busy)
            .task { visible = true; await model.open(); await ads.prepare() }
            .onDisappear { visible = false; interrupted = true; audio.stop() }
            .onChange(of: scenePhase) { if $0 != .active { interrupted = true; audio.stop() } }
            .onChange(of: model.session?.currentID) { _ in audio.stop() }
            .onChange(of: model.session?.id) { _ in
                activeSince = ProcessInfo.processInfo.systemUptime
                if model.session?.completed == false { Task { await ads.prepare() } }
            }
            .onChange(of:purchases.state) { state in
                if visible && state.permitsAds && model.session?.completed == false { Task { await ads.prepare() } }
            }
    }
    private var header: some View {
        HStack(spacing: 12) {
            Button { audio.stop(); dismiss() } label: { Image(systemName: "xmark").frame(width: 44, height: 44) }
                .accessibilityLabel("学習を閉じる。保存した位置から再開できます").disabled(model.busy)
            VStack(alignment: .leading, spacing: 3) {
                Text(model.set.title).font(.subheadline.weight(.medium))
                if let state = model.session { Text("\(state.round)周目").font(.caption).foregroundStyle(.secondary) }
            }
            Spacer(minLength: 0)
            if let state = model.session, !state.completed {
                Text("\(min(state.position + 1, state.order.count)) / \(state.order.count)").font(.caption).monospacedDigit()
            }
        }.padding(.horizontal, 12).padding(.vertical, 8)
    }
    private func roundSummary(_ state: VocabularySession) -> some View {
        VStack(alignment: .leading, spacing: 20) {
            Text("\(state.round)周目を終えました").font(.title2.weight(.semibold))
            Text("次は\(state.deferred.count)語").font(.largeTitle.weight(.medium))
            Text("「覚える」を選んだ単語だけを、もう一度確認しましょう。").foregroundStyle(.secondary)
            if state.deferred.count == 1 {
                Text("最後の1語です。少し間を置いてから続けても大丈夫です。").font(.subheadline).foregroundStyle(.secondary)
            }
        }
    }
    private func completion(_ state: VocabularySession) -> some View {
        VStack(alignment: .leading, spacing: 24) {
            Text("完了").font(.largeTitle.weight(.semibold)).accessibilityAddTraits(.isHeader)
            Text("\(state.round)周で\(state.vocabularyIDs.count)語を確認しました").font(.title2)
            Text("今回の確認は完了です。復習予定に登録しました。「今日の復習」でまた確認しましょう。").foregroundStyle(.secondary)
            if !model.hasNext { Text("収録中の単語はすべてセットに追加されています。").foregroundStyle(.secondary) }
            Button("もう一度見る") { audio.stop(); Task { await model.open(restart: true) } }
                .buttonStyle(.bordered).controlSize(.large).disabled(model.busy)
        }
    }
    private var actions: some View {
        VStack(spacing: 0) {
            Divider()
            Group {
                if let state = model.session, model.errorMessage == nil {
                    if state.completed {
                        Button { audio.stop(); if model.hasNext { Task { await model.nextSet() } } else { dismiss() } } label: {
                            Text(model.hasNext ? "次のセットへ" : "学習一覧へ").frame(maxWidth: .infinity, minHeight: 28)
                        }.buttonStyle(.borderedProminent)
                    } else if state.needsNextRound {
                        Button { perform(.nextRound, revision:state.revision) } label: {
                            Text("\(state.round + 1)周目へ").frame(maxWidth: .infinity, minHeight: 28)
                        }.buttonStyle(.borderedProminent)
                    } else if model.card != nil {
                        if state.revealed {
                            ViewThatFits(in: .horizontal) {
                                HStack(spacing: 12) { decisionButtons(revision:state.revision) }
                                VStack(spacing: 10) { decisionButtons(revision:state.revision) }
                            }
                        } else {
                            Button { perform(.reveal, revision:state.revision) } label: { Text("意味を見る").frame(maxWidth: .infinity, minHeight: 28) }
                                .buttonStyle(.borderedProminent)
                        }
                    }
                }
            }.controlSize(.large).disabled(model.busy).frame(maxWidth: 600).padding(16)
        }.frame(maxWidth: .infinity).background(Color(uiColor: .systemBackground))
    }
    @ViewBuilder private func decisionButtons(revision: Int) -> some View {
        Button { perform(.decide(.learn), revision:revision) } label: { Text("覚える").frame(maxWidth: .infinity, minHeight: 28) }
            .buttonStyle(.bordered).accessibilityHint("次の周でもう一度確認します")
        Button { perform(.decide(.known), revision:revision) } label: { Text("覚えてる").frame(maxWidth: .infinity, minHeight: 28) }
            .buttonStyle(.borderedProminent).accessibilityHint("この学習では通過します。後で学び直せます")
    }
    private func perform(_ action: VocabularyAction, revision: Int) {
        audio.stop()
        let previous = model.session
        Task {
            await model.act(action, expectedRevision:revision)
            guard visible, model.errorMessage == nil, let before = previous,
                  before.revision == revision, !before.completed,
                  let completed = model.session, completed.id == before.id,
                  completed.completed else { return }
            ads.completed(AdBoundary(sessionID:completed.id, uniqueItems:completed.vocabularyIDs.count,
                foregroundSeconds:ProcessInfo.processInfo.systemUptime - activeSince,
                resumed:interrupted || completed.startedAt < openedAt), stopAudio:audio.stop)
        }
    }
}
