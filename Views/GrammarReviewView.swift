import SwiftUI

@MainActor
struct GrammarReviewView: View {
    @StateObject private var model: GrammarReviewViewModel
    @Environment(\.dismiss) private var dismiss
    @Environment(\.scenePhase) private var phase
    @EnvironmentObject private var audio: KoreanAudioService
    init(services: AppContainer, practiceID: UUID? = nil) { _model = StateObject(wrappedValue: GrammarReviewViewModel(services:services, practiceID:practiceID)) }
    var body: some View {
        VStack(spacing:0) {
            HStack {
                Button { audio.stop(); dismiss() } label: { Image(systemName:"xmark").frame(width:44,height:44) }.accessibilityLabel("文法の復習を閉じる")
                Text(model.practiceID == nil ? "今日の復習・文法" : "選んだ文法の練習").font(.subheadline)
                Spacer()
                if let s = model.session { Text("\(min(s.processedCount+1,s.ids.count))/\(s.ids.count)").font(.caption).monospacedDigit() }
            }.padding(.horizontal,12)
            if let s = model.session { ProgressView(value:Double(s.processedCount),total:Double(s.ids.count)).padding(.horizontal,24) }
            ScrollViewReader { proxy in
                ScrollView {
                    VStack(alignment:.leading,spacing:24) {
                        if model.empty { Text("今の復習はありません").font(.title2) }
                        else if model.session?.completed == true {
                            Text("復習完了").font(.largeTitle)
                            if let s = model.session, s.deferredCount > 0 {
                                Text("\(s.completedCount)項目を確認し、利用できない\(s.deferredCount)項目を保留しました。記録と復習予定は残し、教材更新後に再確認します。")
                            } else {
                                Text(model.practiceID == nil ? "次の復習予定を保存しました。" : "練習結果を保存しました。復習予定は変更していません。")
                            }
                            if model.due > 0 { Text("残り\(model.due)項目。続けても、あとで再開しても大丈夫です。").foregroundStyle(.secondary) }
                        } else if let q = model.question {
                            GrammarQuestionView(question:q.question,selected:q.selected,seed:stableSeed) { choice in Task { await model.answer(choice,expectedQuestionID:q.question.id) } }
                            if q.selected != nil, let card = model.card {
                                DisclosureGroup("意味・形・例文を確認") {
                                    VStack(alignment:.leading,spacing:20) {
                                        Text(card.meaning).font(.title2)
                                        Text(card.explanation)
                                        Text(card.form)
                                        GrammarExplanationView(card:card,page:2)
                                    }.padding(.top,12)
                                }
                            }
                        }
                        if model.busy { ProgressView() }
                        if let error = model.error {
                            Text(error); Button("記録を読み直す") { Task { await model.open() } }
                            if let id = model.unavailableID {
                                Button("この教材を保留して続ける") { audio.stop(); Task { await model.deferUnavailable(expectedID:id) } }
                                Text("学習済みにはせず、記録と復習予定を残します。").font(.footnote)
                            }
                        }
                    }.frame(maxWidth:600,alignment:.leading).padding(24).frame(maxWidth:.infinity).id("top")
                }.onChange(of:model.session?.currentID) { _ in proxy.scrollTo("top",anchor:.top) }
            }
        }.background(Color(uiColor:.systemBackground))
            .safeAreaInset(edge:.bottom) {
                VStack(spacing:8) {
                    Divider()
                    if model.error == nil {
                        if model.empty || model.session?.completed == true {
                            Button(model.due > 0 ? "次の復習へ" : "学習一覧へ") {
                                if model.due > 0 { Task { await model.open() } } else { dismiss() }
                            }.buttonStyle(.borderedProminent)
                        } else if let q = model.question, let selected = q.selected {
                            ForEach(ReviewRating.allCases,id:\.self) { rating in
                                Button { Task { await model.rate(rating,expectedQuestionID:q.question.id) } } label: { Text(rating.title).frame(maxWidth:.infinity,minHeight:28) }
                                    .buttonStyle(.bordered).accessibilityHint(model.practiceID == nil ? rating.hint : "今回の練習結果を記録します。復習予定は変更しません")
                                    .disabled(rating == .remembered && !q.question.isCorrect(selected))
                            }
                            if !q.question.isCorrect(selected) { Text(model.practiceID == nil ? "今回は「難しい」か「もう少し」で復習間隔を調整します。" : "今回は「難しい」か「もう少し」で記録します。").font(.caption).foregroundStyle(.secondary) }
                        }
                    }
                }.controlSize(.large).padding(16).background(Color(uiColor:.systemBackground))
            }
            .disabled(model.busy).interactiveDismissDisabled(model.busy)
            .task { await model.open() }.onDisappear { audio.stop() }
            .onChange(of:model.session?.currentID) { _ in audio.stop() }
            .onChange(of:phase) { if $0 != .active { audio.stop() } }
    }
    private var stableSeed: UInt64 {
        (model.session?.id.uuidString ?? "").utf8.reduce(UInt64(0)) { ($0 &* 31) &+ UInt64($1) }
    }
}
