import SwiftUI

@MainActor
struct PlacementView: View {
    let services: AppContainer
    @State private var selected: LearningLevel = .hangul
    @State private var saved = false
    @State private var busy = false
    @State private var error: String?
    var body: some View {
        List {
            Section("どこから始めますか？") {
                Text("学習経験に合わせて選んでください。いつでも変更できます。診断は任意です。").foregroundStyle(.secondary)
                Button("韓国語は初めて") { selected = .hangul; saved = false }.frame(minHeight:44).disabled(busy)
                Button("ハングルは読める") { selected = .intro; saved = false }.frame(minHeight:44).disabled(busy)
                Button("簡単な韓国語が分かる") { selected = .beginner; saved = false }.frame(minHeight:44).disabled(busy)
                Picker("開始位置",selection:$selected) { ForEach(LearningLevel.allCases,id:\.rawValue) { Text($0.japaneseName).tag($0) } }.onChange(of:selected) { _ in saved = false }.disabled(busy)
                Text("上の段階は順次追加予定です。これはアプリ内の段階で、TOPIKなどの試験の級ではありません。").font(.footnote).foregroundStyle(.secondary)
                Button(saved ? "保存しました" : "この位置を保存") { Task { await save() } }.disabled(busy || saved).frame(minHeight:44)
                if saved { NavigationLink("ここから始める："+selected.japaneseName) { CurriculumLevelView(services:services,level:selected) } }
            }
            Section {
                NavigationLink("レベル診断 · 最大8問") { DiagnosticView(services:services) }
                Text("読み・単語・文法・活用・聞き取りの短い確認です。結果は開始位置の提案にだけ使います。既存の学習記録を消したり、習得済みにしたりしません。").font(.footnote).foregroundStyle(.secondary)
            }
            if let error = error { Text(error) }
        }.navigationTitle("開始位置")
            .task {
                do { let profile = try await services.progress.curriculumProfile(); if let p = profile { selected = p.level } }
                catch { self.error = LearningErrorMessage.message(for: error) }
            }
    }
    private func save() async {
        guard !busy else { return }; busy = true
        defer { busy = false }
        do { try await services.progress.saveCurriculumProfile(CurriculumProfile(level:selected,skippedHangul:selected != .hangul)); saved = true; error = nil }
        catch { self.error = LearningErrorMessage.message(for: error) }
    }
}
@MainActor
struct DiagnosticView: View {
    let services: AppContainer
    @EnvironmentObject private var audio: KoreanAudioService
    @Environment(\.scenePhase) private var phase
    @State private var session: DiagnosticSession?
    @State private var input = ""
    @State private var busy = false
    @State private var error: String?
    @State private var heard = false
    @State private var playbackRevision: Int?
    @State private var chosen: LearningLevel = .intro
    @State private var saved = false
    var body: some View {
        ScrollView {
            VStack(alignment:.leading,spacing:24) {
                if let s = session {
                    if s.current == nil {
                        Text("おすすめの開始位置").font(.headline)
                        Text(s.recommendation.japaneseName).font(.largeTitle)
                        Text(s.recommendation == .hangul ? "文字の読み方を、最初からゆっくり確認しましょう。" : s.recommendation == .intro ? "基本の単語と文法を確認しながら進めるのがおすすめです。" : "基本事項を確認できました。初級の日常表現に進んでみましょう。")
                        Text("短い確認のため、上級の力は測定していません。聞き取りを飛ばした場合は、その力を評価していません。").font(.footnote).foregroundStyle(.secondary)
                        Picker("開始位置を変更",selection:$chosen) { ForEach(LearningLevel.allCases,id:\.rawValue) { Text($0.japaneseName).tag($0) } }.onChange(of:chosen) { _ in saved = false }.disabled(busy)
                        Button(saved ? "保存しました" : "この位置を保存") { Task { await save() } }.disabled(busy || saved).frame(minHeight:44)
                        if saved { NavigationLink("ここから始める") { CurriculumLevelView(services:services,level:chosen) } }
                        Button("もう一度診断する") { Task { await open(restart:true) } }.disabled(busy).frame(minHeight:44)
                    } else if let q = s.current {
                        Text("\(s.results.count+1) / \(s.items.count)").font(.subheadline)
                        ProgressView(value:Double(s.results.count),total:Double(s.items.count)).accessibilityLabel("診断の進み具合")
                        if let sound = q.audio {
                            if audio.availability(for:sound) == .available {
                                Button { playbackRevision = s.revision; if !audio.play(sound,speed:.normal) { playbackRevision = nil } } label: { Label("聞く",systemImage:"speaker.wave.2") }.frame(minHeight:44)
                            } else { Text(audio.availability(for:sound).message ?? "音声を利用できません") }
                        }
                        Text(q.prompt).font(.title3)
                        if let text = q.korean { Text(text).font(.largeTitle) }
                        if q.choices.isEmpty {
                            TextField("韓国語で入力",text:$input).font(.title2).autocorrectionDisabled().textInputAutocapitalization(.never).accessibilityLabel("診断の回答")
                            Button("答える") { submit(input,revision:s.revision) }.buttonStyle(.borderedProminent).frame(minHeight:44).disabled(busy || input.trimmingCharacters(in:.whitespacesAndNewlines).isEmpty || input.count > 500)
                        } else {
                            ForEach(q.choices) { choice in
                                Button { submit(choice.id,revision:s.revision) } label: { Text(choice.text).frame(maxWidth:.infinity,alignment:.leading).frame(minHeight:44) }.buttonStyle(.bordered).disabled(busy || (q.audio != nil && !heard) || audio.isPlaying)
                            }
                        }
                        Button(q.audio == nil ? "分からない" : "聞き取りを今回は飛ばす") { submit(q.audio == nil ? "__unknown__" : nil,revision:s.revision) }.disabled(busy).frame(minHeight:44)
                    }
                } else if busy { ProgressView() }
                if let error = error { Text(error); Button("読み直す") { Task { await open(restart:false) } } }
            }.frame(maxWidth:600,alignment:.leading).padding(24).frame(maxWidth:.infinity)
        }.navigationTitle("レベル診断")
            .task { await open(restart:false) }
            .onDisappear { playbackRevision = nil; audio.stop() }
            .onChange(of:phase) { if $0 != .active { playbackRevision = nil; audio.stop() } }
            .onChange(of:audio.completedPlaybackCount) { _ in
                if playbackRevision == session?.revision && playbackRevision != nil { heard = true; playbackRevision = nil }
            }
    }
    private func open(restart: Bool) async {
        guard !busy else { return }; busy = true
        defer { busy = false }
        do {
            let old = try await services.progress.diagnosticSession()
            if !restart, let old = old { session = old }
            else { let items = try await services.content.diagnosticItems(); session = try await services.progress.beginDiagnostic(items:items,version:services.metadata.contentVersion,restart:restart) }
            chosen = session?.recommendation ?? .intro; error = nil; saved = false
            heard = false; input = ""; playbackRevision = nil; audio.stop()
        } catch { self.error = LearningErrorMessage.message(for: error) }
    }
    private func submit(_ value: String?,revision: Int) {
        guard !busy, let s = session, s.revision == revision else { return }
        busy = true; audio.stop(); playbackRevision = nil
        Task {
            defer { busy = false }
            do {
                session = try await services.progress.answerDiagnostic(id:s.id,revision:revision,answer:value)
                input = ""; heard = false; chosen = session?.recommendation ?? .intro; error = nil
            } catch { self.error = LearningErrorMessage.message(for: error) }
        }
    }
    private func save() async {
        guard !busy else { return }; busy = true
        defer { busy = false }
        do { try await services.progress.saveCurriculumProfile(CurriculumProfile(level:chosen,skippedHangul:chosen != .hangul)); saved = true }
        catch { self.error = LearningErrorMessage.message(for: error) }
    }
}
