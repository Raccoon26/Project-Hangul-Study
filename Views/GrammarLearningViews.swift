import SwiftUI

@MainActor
struct GrammarCatalogView: View {
    let services: AppContainer
    @State private var level: LearningLevel
    init(services: AppContainer, level: LearningLevel = .intro) {
        self.services = services; _level = State(initialValue:level)
    }
    @State private var lessons: [GrammarLesson] = []
    @State private var statuses: [ContentID: GrammarLessonStatus] = [:]
    @State private var launch: GrammarLesson?
    @State private var busy = false
    @State private var more = false
    @State private var error: String?
    private let levels: [LearningLevel] = [.intro, .beginner, .lowerIntermediate, .intermediate, .upperIntermediate, .advanced, .master]
    var body: some View {
        List {
            Picker("段階", selection: $level) { ForEach(levels, id: \.self) { Text($0.japaneseName).tag($0) } }.disabled(busy)
            Section {
                Text("意味・形・使い方を、少しずつ").foregroundStyle(.secondary)
                ForEach(lessons) { lesson in
                    Button { launch = lesson } label: {
                        VStack(alignment: .leading, spacing: 8) {
                            if let course = lesson.courseTitle {
                                Text([course,lesson.unitTitle].compactMap { $0 }.joined(separator:" · "))
                                    .font(.caption).foregroundStyle(.secondary)
                            }
                            Text(lesson.title).font(.headline).foregroundStyle(.primary)
                            Text("\(lesson.count)項目 · \(status(lesson.id))").font(.subheadline).foregroundStyle(.secondary)
                        }.padding(.vertical, 8).frame(minHeight: 44)
                    }
                }
                if lessons.isEmpty && !busy && error == nil { Text("この段階の文法はまだ収録されていません。入門・初級から学べます。").foregroundStyle(.secondary) }
                if more { Button("続きを表示") { Task { await load(reset: false) } }.disabled(busy) }
                if busy { ProgressView() }
                if let error = error { Text(error); Button("読み直す") { Task { await load(reset: true) } } }
            }
        }.navigationTitle("文法")
            .task(id: level) { await load(reset: true) }
            .fullScreenCover(item: $launch, onDismiss: { Task { await load(reset: true) } }) { GrammarStudyView(services: services, lesson: $0) }
    }
    private func status(_ id: ContentID) -> String {
        guard let state = statuses[id] else { return "未学習" }
        return state.active ? "学習中・続きから" : state.completed > 0 ? "回読完了・復習予定" : "未学習"
    }
    private func load(reset: Bool) async {
        guard !busy else { return }; busy = true; error = nil
        defer { busy = false }
        do {
            let requested = level
            let rows = try await services.content.grammarLessons(level: requested, after: reset ? -1 : (lessons.last?.order ?? -1), limit: 30)
            guard requested == level else { return }
            lessons = reset ? rows : lessons + rows; more = rows.count == 30
            let values = try await services.progress.grammarStatuses(ids: rows.map(\.id))
            if reset { statuses = [:] }
            for s in values { statuses[s.lessonID] = s }
        } catch { self.error = LearningErrorMessage.message(for: error) }
    }
}

@MainActor
struct GrammarStudyView: View {
    @StateObject private var model: GrammarViewModel
    @Environment(\.dismiss) private var dismiss
    @Environment(\.scenePhase) private var phase
    @EnvironmentObject private var audio: KoreanAudioService
    @State private var lookup: LookupReference?
    private let services: AppContainer
    init(services: AppContainer, lesson: GrammarLesson) { self.services = services; _model = StateObject(wrappedValue: GrammarViewModel(services: services, lesson: lesson)) }
    var body: some View {
        VStack(spacing: 0) {
            HStack {
                Button { audio.stop(); dismiss() } label: { Image(systemName: "xmark").frame(width: 44, height: 44) }.accessibilityLabel("学習を閉じて位置を保存")
                Text(model.lesson.title).font(.subheadline)
                Spacer()
                if let s = model.session { Text("\(s.round)周目 · \(min(s.position + 1,s.order.count))/\(s.order.count)").font(.caption).monospacedDigit() }
            }.padding(.horizontal, 12)
            if let s = model.session { ProgressView(value: Double(s.position), total: Double(s.order.count)).padding(.horizontal,24).accessibilityLabel("回読の進み具合") }
            ScrollViewReader { proxy in
                ScrollView {
                    VStack(alignment: .leading, spacing: 24) {
                        if let s = model.session {
                            if s.completed {
                                Text("完了").font(.largeTitle)
                                Text("\(s.round)周で\(s.ids.count)項目を確認しました")
                                Text("\(s.correctCount) / \(s.correctCount + s.wrongCount) 正解")
                                Text("復習予定を保存しました。予定日になったら「今日の復習」で確認できます。").foregroundStyle(.secondary)
                                Button("もう一度学ぶ") { Task { await model.open(restart: true) } }.frame(minHeight:44)
                            } else if s.nextRound {
                                Text("\(s.round)周目が終わりました").font(.title2)
                                Text("次は、まだ覚えたい\(s.deferred.count)項目だけ確認します。")
                            } else if let card = model.card {
                                if s.page < 3 {
                                    GrammarExplanationView(card: card, page: s.page)
                                    if s.page == 2 && !card.relatedWords.isEmpty {
                                        DisclosureGroup("例文の単語を確認") {
                                            ForEach(card.relatedWords) { word in
                                                Button { lookup = word.reference } label: {
                                                    Text(word.title+" · "+word.meaning).frame(minHeight:44)
                                                }
                                            }
                                        }
                                    }
                                }
                                else if s.page == 3, let q = s.question {
                                    GrammarQuestionView(question: q, selected: s.selected, seed: s.seed &+ UInt64(s.round)) { choice in Task { await model.send(.answer(choice), expectedRevision:s.revision) } }
                                } else {
                                    Text(card.pattern).font(.largeTitle).accessibilityAddTraits(.isHeader)
                                    Text(card.meaning).font(.title2)
                                    Text("意味と使い方を、自分で思い出せますか？").foregroundStyle(.secondary)
                                }
                            }
                        }
                        if model.busy { ProgressView() }
                        if let error = model.error { Text(error); Button("記録を読み直す") { Task { await model.open() } } }
                    }.frame(maxWidth:600, alignment:.leading).padding(24).frame(maxWidth:.infinity).id("top")
                }.onChange(of: model.session?.currentID) { _ in proxy.scrollTo("top", anchor: .top) }
                 .onChange(of: model.session?.page) { _ in proxy.scrollTo("top", anchor: .top) }
                 .onChange(of: model.session?.questionIndex) { _ in proxy.scrollTo("top", anchor: .top) }
            }
        }.background(Color(uiColor: .systemBackground))
            .safeAreaInset(edge:.bottom) { actions }
            .disabled(model.busy).interactiveDismissDisabled(model.busy)
            .sheet(item:$lookup) { reference in
                NavigationStack {
                    LookupDetailView(services:services,reference:reference)
                        .toolbar { ToolbarItem(placement:.cancellationAction) { Button("閉じる") { lookup = nil } } }
                }
            }
            .task { await model.open() }.onDisappear { audio.stop() }
            .onChange(of: model.session?.revision) { _ in audio.stop() }
            .onChange(of: phase) { if $0 != .active { audio.stop() } }
    }
    @ViewBuilder private func recallButtons(revision: Int) -> some View {
        Button("覚える") { Task { await model.send(.decide(false), expectedRevision:revision) } }.frame(minHeight:44)
        Button("覚えてる") { Task { await model.send(.decide(true), expectedRevision:revision) } }.frame(minHeight:44)
    }
    private var actions: some View {
        VStack {
            Divider()
            if model.error == nil, let s = model.session {
                if s.completed { Button("レッスン一覧へ") { dismiss() }.buttonStyle(.borderedProminent) }
                else if s.nextRound { Button("次の回読へ") { Task { await model.send(.nextRound, expectedRevision:s.revision) } }.buttonStyle(.borderedProminent) }
                else if s.page == 4 {
                    ViewThatFits(in:.horizontal) {
                        HStack { recallButtons(revision:s.revision) }
                        VStack(spacing:8) { recallButtons(revision:s.revision) }
                    }.buttonStyle(.bordered)
                } else {
                    Button(s.page == 2 ? "問題へ" : "次へ") { Task { await model.send(.next, expectedRevision:s.revision) } }
                        .buttonStyle(.borderedProminent).disabled(s.page == 3 && s.selected == nil)
                }
            }
        }.controlSize(.large).frame(maxWidth:.infinity, minHeight:60).padding(.bottom,12).background(Color(uiColor:.systemBackground))
    }
}

@MainActor
struct GrammarExplanationView: View {
    let card: GrammarCard
    let page: Int
    @ScaledMetric(relativeTo:.largeTitle) private var size: CGFloat = 42
    var body: some View {
        VStack(alignment:.leading, spacing:24) {
            Text(card.pattern).font(.system(size:size,weight:.medium)).fixedSize(horizontal:false,vertical:true).accessibilityAddTraits(.isHeader)
            if page == 0 {
                Text(card.meaning).font(.title2)
                Text(card.explanation)
                if !card.prerequisites.isEmpty {
                    DisclosureGroup("先に確認したい形") {
                        VStack(alignment:.leading,spacing:16) {
                            Text("必要な形だけ読み直せます。表示するだけでは学習完了になりません。")
                                .font(.footnote).foregroundStyle(.secondary)
                            ForEach(card.prerequisites) { item in
                                Text(item.pattern).font(.headline)
                                Text(item.meaning)
                                Text(item.form)
                                Text(item.explanation).foregroundStyle(.secondary)
                            }
                        }.padding(.top,12)
                    }
                }
            } else if page == 1 {
                Text("形と使い方").font(.headline)
                Text(card.form).font(.title3)
                if let constraints = card.constraints { Text(constraints).foregroundStyle(.secondary) }
                if let note = card.note { Text("ポイント").font(.headline); Text(note) }
            } else {
                ForEach(card.examples) { GrammarExampleView(example:$0) }
                if !card.comparisons.isEmpty {
                    DisclosureGroup("似た表現との違い") {
                        VStack(alignment:.leading,spacing:20) {
                            if let note = card.note { Text(note) }
                            ForEach(card.comparisons) { comparison in
                                Text(comparison.pattern).font(.title2)
                                Text(comparison.meaning)
                                Text(comparison.difference).foregroundStyle(.secondary)
                                if let example = comparison.example { GrammarExampleView(example:example) }
                            }
                        }.padding(.top,12)
                    }
                }
            }
        }
    }
}
@MainActor
struct GrammarExampleView: View {
    let example: Example
    @EnvironmentObject private var audio: KoreanAudioService
    private var request: LearningAudio { LearningAudio(source:.systemTTS,usage:.wordSentence,text:example.korean,asset:nil) }
    var body: some View {
        VStack(alignment:.leading,spacing:8) {
            Text(example.korean).font(.title3).fixedSize(horizontal:false,vertical:true)
            Text(example.japanese).foregroundStyle(.secondary)
            if let note = example.learningPoint { Text(note).font(.footnote).foregroundStyle(.secondary) }
            if audio.availability(for:request) == .available {
                ViewThatFits(in:.horizontal) {
                    HStack(spacing:20) { buttons }
                    VStack(alignment:.leading) { buttons }
                }
            } else if let message = audio.availability(for:request).message { Text(message).font(.footnote) }
            if let message = audio.message { Text(message).font(.footnote) }
        }
    }
    @ViewBuilder private var buttons: some View {
        Button { audio.play(request,speed:.normal) } label: { Label("聞く",systemImage:"speaker.wave.2").fixedSize(horizontal:false,vertical:true).frame(maxWidth:.infinity,minHeight:44) }.accessibilityLabel("例文を通常の速さで聞く")
        Button { audio.play(request,speed:.slow) } label: { Text("ゆっくり").fixedSize(horizontal:false,vertical:true).frame(maxWidth:.infinity,minHeight:44) }
        Button { audio.stop() } label: { Text("停止").frame(maxWidth:.infinity,minHeight:44) }.disabled(!audio.isPlaying)
    }
}
@MainActor
struct GrammarQuestionView: View {
    let question: GrammarQuestion
    let selected: String?
    let seed: UInt64
    let answer: (String) -> Void
    var body: some View {
        VStack(alignment:.leading,spacing:20) {
            Text(question.prompt).font(.title3)
            if let korean = question.korean { Text(korean).font(.largeTitle).fixedSize(horizontal:false,vertical:true) }
            ForEach(QuizOptions.ordered(question.choices,seed:seed,contentID:question.id)) { choice in
                Button { answer(choice.id) } label: {
                    HStack {
                        Text(choice.text).multilineTextAlignment(.leading)
                        Spacer()
                        if selected == choice.id { Image(systemName:"checkmark.circle").accessibilityLabel("選択した答え") }
                    }.frame(maxWidth:.infinity,minHeight:44)
                }.buttonStyle(.bordered).disabled(selected != nil)
            }
            if let selected = selected {
                Label(question.isCorrect(selected) ? "正解" : "もう一度確認しましょう",systemImage:question.isCorrect(selected) ? "checkmark" : "arrow.uturn.backward").font(.headline)
                if let correct = question.choices.first(where: { $0.id == question.correctID }) { Text("正しい答え：\(correct.text)") }
                Text(question.explanation).foregroundStyle(.secondary)
            }
        }
    }
}
