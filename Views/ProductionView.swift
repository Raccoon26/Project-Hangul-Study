import SwiftUI

@MainActor
struct ProductionCatalogView: View {
    let services: AppContainer
    var level: LearningLevel? = nil
    @State private var entries: [Entry] = []
    @State private var busy = false
    @State private var more = true
    @State private var error: String?
    private struct Entry: Identifiable { let id: ContentID; let title: String }
    var body: some View {
        List {
            Text("形を確認してから、自分で入力します。韓国語キーボードを追加してお使いください。").foregroundStyle(.secondary)
            NavigationLink("文法の意味・使い方を確認") { GrammarCatalogView(services:services,level:level ?? .intro) }
            ForEach(entries) { entry in
                NavigationLink(entry.title) { ProductionStudyView(services:services,id:entry.id) }
            }
            if more { Button("続きを表示") { Task { await load() } }.disabled(busy) }
            if entries.isEmpty && !busy && !more { Text("この段階の入力練習はまだ収録されていません。単語や文法から学習を続けられます。").foregroundStyle(.secondary) }
            if busy { ProgressView() }
            if let error = error { Text(error) }
        }.navigationTitle("活用・入力練習").task { if entries.isEmpty { await load() } }
    }
    private func load() async {
        guard !busy else { return }; busy = true; error = nil
        defer { busy = false }
        do {
            let rows: [(ContentID,String)]
            if let level = level { rows = try await services.content.curriculumProduction(level:level,after:entries.last?.id.rawValue ?? "") }
            else { rows = try await services.content.productionVocabulary(after:entries.last?.id.rawValue ?? "") }
            entries += rows.map { Entry(id:$0.0,title:$0.1) }; more = rows.count == 30
        } catch { self.error = LearningErrorMessage.message(for: error) }
    }
}
@MainActor
struct ProductionStudyView: View {
    let services: AppContainer
    let id: ContentID
    @EnvironmentObject private var audio: KoreanAudioService
    @Environment(\.scenePhase) private var scenePhase
    @FocusState private var focused: Bool
    @State private var session: ProductionSession?
    @State private var grammar: GrammarCard?
    @State private var grammarNotice: String?
    @State private var input = ""
    @State private var error: String?
    @State private var busy = false
    var body: some View {
        ScrollView {
            VStack(alignment:.leading,spacing:24) {
                if let s = session {
                    if s.completed {
                        Text("練習完了").font(.largeTitle)
                        Text("結果を保存しました。すぐの再入力だけで習得済みにはしません。単語の復習予定も確認できます。")
                        Button("もう一度") { Task { await open() } }.frame(minHeight:44)
                    } else if let q = s.current {
                        Text(s.retrying ? "間違えた問題を確認" : "\(s.position+1) / \(s.questions.count)").font(.caption)
                        if s.studying {
                            Text(q.lemma).font(.largeTitle)
                            Text(q.meaning).font(.title2)
                            Text("語幹：\(q.lemma.dropLast())-").font(.title2)
                            Text(q.form.title).font(.headline)
                            Text(q.generated).font(.largeTitle)
                            Text(q.explanation)
                            if let grammar = grammar {
                                DisclosureGroup("関連する文法："+grammar.pattern) {
                                    GrammarExplanationView(card:grammar,page:0)
                                    GrammarExplanationView(card:grammar,page:1)
                                }
                            }
                            sound(q.generated)
                        } else {
                            Text(q.prompt).font(.title3)
                            if let korean = q.korean { Text(korean).font(.title2) }
                            TextField("韓国語で入力",text:$input,axis:.vertical)
                                .textFieldStyle(.roundedBorder).font(.title2).focused($focused)
                                .autocorrectionDisabled().textInputAutocapitalization(.never)
                                .submitLabel(.done).onSubmit { submit() }.disabled(s.result != nil)
                                .accessibilityLabel("韓国語の答え")
                            if input.count > 500 { Text("500文字以内で入力してください。").font(.footnote) }
                            if let result = s.result {
                                Text(result == .correct ? "✓ 正解" : result == .spacing ? "内容は合っています。分かち書きを確認しましょう" : "もう一度確認しましょう").font(.headline)
                                Text(q.accepted.joined(separator:" ／ ")).font(.title2)
                                Text(q.explanation)
                                sound(q.accepted[0])
                            } else {
                                Text("学習した内容と問題の指示に合わせて入力してください。自由翻訳の自動採点ではありません。").font(.footnote).foregroundStyle(.secondary)
                            }
                        }
                    }
                }
                if let grammarNotice = grammarNotice { Text(grammarNotice).font(.footnote).foregroundStyle(.secondary) }
                if busy { ProgressView() }
                if let error = error { Text(error); Button("記録を読み直す") { Task { await open() } } }
            }.frame(maxWidth:600,alignment:.leading).padding(24).frame(maxWidth:.infinity)
        }.safeAreaInset(edge:.bottom) {
            if let s = session, s.current != nil, error == nil {
                Button(s.studying ? "入力してみる" : s.result != nil ? "次へ" : "答える") {
                    if s.studying || s.result != nil { Task { await change(nil,expectedRevision:s.revision) } }
                    else { submit() }
                }.frame(maxWidth:.infinity,minHeight:44).buttonStyle(.borderedProminent).controlSize(.large)
                    .padding().background(Color(uiColor:.systemBackground))
                    .disabled(busy || (!s.studying && s.result == nil && (ProductionAnswer.normalize(input).isEmpty || input.count > 500)))
            }
        }.controlSize(.large).navigationTitle("活用").navigationBarTitleDisplayMode(.inline).toolbar(.hidden,for:.tabBar)
            .scrollDismissesKeyboard(.interactively)
            .toolbar { ToolbarItemGroup(placement:.keyboard) { Spacer(); Button("閉じる") { focused = false } } }
            .disabled(busy).task { await open() }
            .task(id:session?.current?.grammarID) {
                grammar = nil; grammarNotice = nil
                if let id = session?.current?.grammarID {
                    do {
                        let loaded = try await services.content.grammarCard(id:id)
                        if session?.current?.grammarID == id { grammar = loaded }
                    }
                    catch is CancellationError { }
                    catch {
                        if session?.current?.grammarID == id { grammarNotice = "関連する文法の説明を読み込めませんでした。保存済みの問題は続けられます。" }
                    }
                }
            }.onDisappear { audio.stop() }
            .onChange(of:scenePhase) { phase in
                if phase != .active { audio.stop(); focused = false }
            }
    }
    @ViewBuilder private func sound(_ text: String) -> some View {
        let request = LearningAudio(source:.systemTTS,usage:.wordSentence,text:text,asset:nil)
        if audio.availability(for:request) == .available {
            HStack {
                Button { audio.play(request,speed:.normal) } label: { Label("聞く",systemImage:"speaker.wave.2").frame(minHeight:44) }
                Button("ゆっくり") { audio.play(request,speed:.slow) }.frame(minHeight:44)
                if audio.isPlaying { Button("停止") { audio.stop() }.frame(minHeight:44) }
            }.frame(minHeight:44)
        } else if let message = audio.availability(for:request).message { Text(message).font(.footnote) }
        if let message = audio.message { Text(message).font(.footnote) }
    }
    private func submit() {
        guard !busy, session?.result == nil else { return }
        focused = false
        let answer = input, revision = session?.revision
        Task { await change(answer, expectedRevision:revision) }
    }
    private func open() async {
        guard !busy else { return }; busy = true; error = nil
        defer { busy = false }
        do {
            if let saved = try await services.progress.activeProduction(scope:id) { session = saved }
            else {
                let questions = try await services.content.productionQuestions(id:id)
                session = try await services.progress.beginProduction(scope:id,questions:questions,version:services.metadata.contentVersion)
            }
            input = session?.answer ?? ""
        } catch { self.error = LearningErrorMessage.message(for: error) }
    }
    private func change(_ answer: String?, expectedRevision: Int?) async {
        guard !busy, error == nil, let s = session, s.revision == expectedRevision else { return }; busy = true
        defer { busy = false }
        do {
            session = try await services.progress.updateProduction(s,answer:answer)
            audio.stop(); input = session?.answer ?? ""; focused = false
        } catch { self.error = LearningErrorMessage.message(for: error) }
    }
}
