import SwiftUI

@MainActor
struct ReviewSessionView: View {
    @Environment(\.dismiss) private var dismiss
    @Environment(\.scenePhase) private var scenePhase
    @EnvironmentObject private var audio: KoreanAudioService
    @StateObject private var model: ReviewViewModel
    init(services: AppContainer, practiceID: UUID? = nil, sessionLimit: Int = 20) { _model = StateObject(wrappedValue: ReviewViewModel(services: services, practiceID:practiceID, sessionLimit:sessionLimit)) }
    var body: some View {
        VStack(spacing: 0) {
            HStack(spacing: 12) {
                Button { audio.stop(); dismiss() } label: { Image(systemName: "xmark").frame(width: 44, height: 44) }
                    .accessibilityLabel("復習を閉じる。保存した位置から再開できます").disabled(model.busy)
                Text(model.practiceID == nil ? "今日の復習" : "選んだ単語の練習").font(.subheadline.weight(.medium))
                Spacer(minLength: 0)
                if let session = model.session {
                    Text("\(min(session.completedCount + 1, session.ids.count)) / \(session.ids.count)").font(.caption).monospacedDigit()
                }
            }.padding(.horizontal, 12).padding(.vertical, 8)
            if let session = model.session, !session.completed {
                ProgressView(value: Double(session.completedCount), total: Double(session.ids.count))
                    .padding(.horizontal, 24).accessibilityLabel("この復習の進み具合")
            }
            ScrollViewReader { proxy in
                ScrollView {
                    VStack(alignment: .leading, spacing: 24) {
                        if model.nothingDue {
                            Text("今の復習はありません").font(.title2.weight(.semibold))
                            Text("予定日になった単語は、ここに表示されます。").foregroundStyle(.secondary)
                        } else if let session = model.session, session.completed {
                            Text("復習完了").font(.largeTitle.weight(.semibold)).accessibilityAddTraits(.isHeader)
                            Text("\(session.ids.count)語を確認しました").font(.title2)
                            Text(model.practiceID == nil ? "次の復習予定を保存しました。" : "練習結果を保存しました。復習予定は変更していません。").foregroundStyle(.secondary)
                            if model.remainingDue > 0 { Text("残り\(model.remainingDue)語。続けても、あとで再開しても大丈夫です。").foregroundStyle(.secondary) }
                        } else if let card = model.card, let session = model.session {
                            VocabularyCardContentView(card: card, revealed: session.revealed).id(card.id)
                        } else if model.busy { ProgressView("読み込み中") }
                        if let error = model.errorMessage {
                            Text(error).foregroundStyle(.secondary)
                            Button("記録を読み直す") { Task { await model.reload() } }
                                .buttonStyle(.bordered).controlSize(.large).disabled(model.busy)
                        }
                    }.frame(maxWidth: 600, alignment: .leading).padding(24).frame(maxWidth: .infinity).id("review-top")
                }.onChange(of: model.session?.currentID) { _ in proxy.scrollTo("review-top", anchor: .top) }
            }
        }.background(Color(uiColor: .systemBackground))
            .safeAreaInset(edge: .bottom, spacing: 0) { actions }
            .interactiveDismissDisabled(model.busy)
            .task { await model.open() }
            .onDisappear { audio.stop() }
            .onChange(of: scenePhase) { if $0 != .active { audio.stop() } }
            .onChange(of: model.session?.currentID) { _ in audio.stop() }
    }
    private var actions: some View {
        VStack(spacing: 0) {
            Divider()
            Group {
                if model.errorMessage == nil {
                    if model.nothingDue || model.session?.completed == true {
                        Button {
                            audio.stop()
                            if !model.nothingDue && model.remainingDue > 0 { Task { await model.open() } }
                            else { dismiss() }
                        } label: {
                            Text(!model.nothingDue && model.remainingDue > 0 ? "次の復習へ" : "学習一覧へ").frame(maxWidth: .infinity, minHeight: 28)
                        }.buttonStyle(.borderedProminent)
                    } else if let session = model.session, model.card != nil {
                        if session.revealed {
                            // Vertical layout leaves room for Japanese at accessibility sizes.
                            VStack(spacing: 8) {
                                ForEach(ReviewRating.allCases, id: \.self) { rating in
                                    Button { audio.stop(); Task { await model.rate(rating,expectedID:session.currentID) } } label: {
                                        Text(rating.title).frame(maxWidth: .infinity, minHeight: 28)
                                    }.buttonStyle(.bordered).accessibilityHint(model.practiceID == nil ? rating.hint : "今回の練習結果を記録します。復習予定は変更しません")
                                }
                            }
                        } else {
                            Button { audio.stop(); Task { await model.reveal(expectedID:session.currentID) } } label: {
                                Text("意味を見る").frame(maxWidth: .infinity, minHeight: 28)
                            }.buttonStyle(.borderedProminent)
                        }
                    }
                }
            }.controlSize(.large).disabled(model.busy).frame(maxWidth: 600).padding(16)
        }.frame(maxWidth: .infinity).background(Color(uiColor: .systemBackground))
    }
}
