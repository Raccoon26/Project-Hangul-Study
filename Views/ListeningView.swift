import SwiftUI

@MainActor
struct ListeningCatalogView: View {
    let services: AppContainer
    @Environment(\.scenePhase) private var scenePhase
    @State private var due = 0
    @State private var activeReview = false
    @State private var error: String?
    var body: some View {
        List {
            Section("今日の復習") {
                NavigationLink("\(due)項目 · \(activeReview ? "続きから" : "復習する")") {
                    ListeningStudyView(services:services,level:nil)
                }.disabled(due == 0 && !activeReview)
            }
            Section("音声を聞いて練習") {
                ForEach([LearningLevel.intro,.beginner,.lowerIntermediate],id:\.rawValue) { level in
                    NavigationLink(level.japaneseName) { ListeningBatchView(services:services,level:level) }
                }
                Text("再生ボタンを押すと音声が流れます。1回最大20問。途中で閉じても続きから再開できます。")
                    .font(.footnote).foregroundStyle(.secondary)
            }
            if let error = error { Text(error) }
        }.navigationTitle("リスニング").task { await refresh() }
            .onChange(of:scenePhase) { if $0 == .active { Task { await refresh() } } }
            .onReceive(NotificationCenter.default.publisher(for:.NSCalendarDayChanged)) { _ in Task { await refresh() } }
    }
    private func refresh() async {
        do {
            due = try await services.progress.listeningDue(now:Date()).0
            activeReview = try await services.progress.activeListening(scope:"review") != nil
            error = nil
        } catch {
            self.error = LearningErrorMessage.message(for: error)
        }
    }
}
@MainActor
struct ListeningBatchView: View {
    let services: AppContainer
    let level: LearningLevel
    @State private var batches: [Batch] = []
    @State private var courses: [Course] = []
    @State private var busy = false
    @State private var more = true
    @State private var error: String?
    private struct Batch: Identifiable { let id: Int; let count: Int }
    var body: some View {
        List {
            if !courses.isEmpty {
                Section("短いレッスン") {
                    ForEach(courses) { course in
                        NavigationLink(course.title) { ListeningCourseView(services:services,course:course,level:level) }
                    }
                }
            }
            ForEach(batches) { batch in
                NavigationLink("練習 \(batch.id+1) · \(batch.count)問") {
                    ListeningStudyView(services:services,level:level,batch:batch.id)
                }
            }
            if more { Button("続きを表示") { Task { await load() } }.disabled(busy) }
            if let error = error { Text(error) }
        }.navigationTitle(level.japaneseName + "リスニング")
            .task { if batches.isEmpty { await load() } }
    }
    private func load() async {
        guard !busy else { return }; busy = true; error = nil
        defer { busy = false }
        do {
            if batches.isEmpty { courses = try await services.content.listeningCourses(level:level) }
            let rows = try await services.content.listeningBatches(level:level,after:batches.last?.id ?? -1)
            batches += rows.map { Batch(id:$0.0,count:$0.1) }; more = rows.count == 30
        } catch { self.error = LearningErrorMessage.message(for: error) }
    }
}
@MainActor
struct ListeningCourseView: View {
    let services: AppContainer
    let course: Course
    let level: LearningLevel
    @State private var completed: Set<ContentID> = []
    @State private var error: String?
    var body: some View {
        List {
            Text(course.description)
            Text("まず内容理解、別の機会に書き取り等へ。1回5問でも途中で止められます。文法・単語の説明は解答後に確認できます。3〜10分を目安に、無理なく区切ってください。")
                .font(.footnote).foregroundStyle(.secondary)
            NavigationLink("先に文法を復習する") { GrammarCatalogView(services:services,level:level) }
            ForEach(course.lessons) { lesson in
                NavigationLink {
                    ListeningStudyView(services:services,level:level,lessonID:lesson.id)
                } label: {
                    HStack {
                        Text(lesson.title + " · \(lesson.itemCount)問")
                        Spacer()
                        if completed.contains(lesson.id) { Text("確認済み").font(.caption) }
                    }.frame(minHeight:44)
                }
            }
            if let error = error { Text(error) }
        }.navigationTitle(course.title).task {
            do {
                var done: Set<ContentID> = []
                for lesson in course.lessons {
                    let ids = try await services.content.listeningLessonIDs(lesson:lesson.id)
                    let counts = try await services.progress.curriculumCounts(ids:ids,kind:"listening")
                    if counts.0 == ids.count { done.insert(lesson.id) }
                }
                completed = done; error = nil
            } catch { self.error = LearningErrorMessage.message(for:error) }
        }
    }
}
@MainActor
private struct ListeningFeedbackContextView: View {
    let services: AppContainer
    let source: ContentID
    @State private var context: ListeningContext?
    @State private var error: String?
    var body: some View {
        VStack(alignment:.leading,spacing:16) {
            if let context = context {
                if let point = context.learningPoint { Text(point).foregroundStyle(.secondary) }
                ForEach(context.references) { entry in
                    NavigationLink(entry.title + " · " + entry.meaning) { LookupDetailView(services:services,reference:entry.reference) }
                }
            }
            if let error = error { Text(error) }
        }.task {
            do { context = try await services.content.listeningContext(source:source); error = nil }
            catch { self.error = LearningErrorMessage.message(for:error) }
        }
    }
}
@MainActor
struct ListeningStudyView: View {
    let services: AppContainer
    let level: LearningLevel?
    var batch = 0
    var resumeScope: String? = nil
    var lessonID: ContentID? = nil
    @EnvironmentObject private var audio: KoreanAudioService
    @Environment(\.scenePhase) private var scenePhase
    @FocusState private var focused: Bool
    @State private var session: ListeningSession?
    @State private var input = ""
    @State private var draftSequence = 0
    @State private var busy = false
    @State private var error: String?
    @State private var empty = false
    @State private var playback: Playback?
    private struct Playback { let question: ContentID; let speed: AudioSpeed; let revision: Int }
    private var scope: String { resumeScope ?? (lessonID.map { "lesson:"+(level?.rawValue ?? LearningLevel.lowerIntermediate.rawValue)+":"+$0.rawValue } ?? (level.map { "practice:"+$0.rawValue+":\(batch)" } ?? "review")) }
    var body: some View {
        ScrollView {
            VStack(alignment:.leading,spacing:24) {
                if let s = session {
                    if s.completed {
                        Text("練習完了").font(.largeTitle)
                        Text("\(s.correct) / \(s.questions.count) 正解").font(.title2)
                        if s.wrong > 0 { Text("\(s.wrong)問を再確認しました。再確認での正解：\(s.retrySuccess)問") }
                        Text("結果と復習予定を保存しました。短い間隔での再確認は、長期記憶とは分けて記録します。")
                            .foregroundStyle(.secondary)
                        Button(level == nil ? "残りの復習を確認" : "もう一度練習") { Task { await open() } }.frame(minHeight:44)
                    } else if let q = s.current {
                        Text(s.retrying ? "間違えた問題をもう一度" : "\(s.position+1) / \(s.questions.count)").font(.subheadline)
                        ProgressView(value:Double(s.position),total:Double(s.questions.count)).accessibilityLabel("問題の進み具合")
                        Text(q.prompt).font(.title3).fixedSize(horizontal:false,vertical:true)
                        audioControls(q,s:s)
                        if s.result == nil {
                            if q.task == .dictation {
                                TextField("韓国語で入力",text:$input,axis:.vertical)
                                    .textFieldStyle(.roundedBorder).font(.title2).focused($focused)
                                    .autocorrectionDisabled().textInputAutocapitalization(.never)
                                    .submitLabel(.done).onSubmit { submit(input) }
                                    .accessibilityLabel("聞こえた韓国語を入力")
                                    .disabled(busy)
                                Text("文中の句読点は入力してください。文末の「.」「!」「?」は省略できます。単語の間の空白も確認してください。")
                                    .font(.footnote).foregroundStyle(.secondary)
                                if input.count > 500 { Text("500文字以内で入力してください。") }
                            } else if s.revealsChoices {
                                ForEach(q.choices) { choice in
                                    Button { submit(choice.id) } label: {
                                        Text(choice.text).frame(maxWidth:.infinity,alignment:.leading).frame(minHeight:44)
                                    }.buttonStyle(.bordered).disabled(!s.heard || audio.isPlaying || busy || error != nil)
                                }
                            }
                            if !s.heard { Text("まず音声を最後まで聞いてください。").font(.footnote).foregroundStyle(.secondary) }
                        } else if let result = s.result {
                            Text(result == .correct ? "✓ 正解" : result == .spacing ? "ほぼ正解です。分かち書きを確認しましょう" : "もう一度確認しましょう").font(.headline)
                            // Transcript is conditionally created, never hidden with opacity/accessibility alone.
                            Text(q.transcript).font(.largeTitle).accessibilityLabel("韓国語の原文："+q.transcript)
                            Text(q.translation).font(.title3)
                            if q.task == .dictation { Text("入力した答え："+(s.answer ?? "")) }
                            else if let correct = q.choices.first(where: { $0.id == q.correctID }) { Text("正解："+correct.text) }
                            Text(q.explanation).foregroundStyle(.secondary)
                            ListeningFeedbackContextView(services:services,source:q.sourceID).id(q.id)
                        }
                    }
                } else if empty {
                    Text("今のところ、出題できる項目はありません。記録はそのまま保存されています。")
                    if level == nil { Text("利用できない教材は保留し、復習予定を残しています。教材更新後に再確認します。").font(.footnote) }
                }
                if busy { ProgressView() }
                if let error = error { Text(error); Button("記録を読み直す") { Task { await open() } }.frame(minHeight:44) }
            }.frame(maxWidth:600,alignment:.leading).padding(24).frame(maxWidth:.infinity)
        }.safeAreaInset(edge:.bottom) {
            if let s = session, let q = s.current {
                if s.result != nil {
                    Button("次へ") { Task { await change(.next, expectedRevision:s.revision) } }
                        .buttonStyle(.borderedProminent).controlSize(.large).frame(maxWidth:.infinity)
                        .padding().background(.regularMaterial).disabled(busy || error != nil)
                } else if q.task == .dictation {
                    Button("答える") { submit(input) }
                        .buttonStyle(.borderedProminent).controlSize(.large).frame(maxWidth:.infinity)
                        .padding().background(.regularMaterial)
                        .disabled(!s.heard || busy || audio.isPlaying || error != nil || ProductionAnswer.normalize(input).isEmpty || input.count > 500)
                }
            }
        }.navigationTitle(level?.japaneseName ?? "今日の復習").navigationBarTitleDisplayMode(.inline)
            .toolbar(.hidden,for:.tabBar).scrollDismissesKeyboard(.interactively)
            .toolbar { ToolbarItemGroup(placement:.keyboard) { Spacer(); Button("閉じる") { focused = false } } }
            .task { if session == nil { await open() } }
            .onChange(of:input) { saveDraft($0) }
            .onDisappear { saveDraft(input); playback = nil; audio.stop() }
            .onChange(of:scenePhase) { if $0 != .active { playback = nil; audio.stop() } }
            .onChange(of:audio.completedPlaybackCount) { _ in
                guard let play = playback, let s = session, s.current?.id == play.question, s.revision == play.revision else { return }
                playback = nil
                Task { await change(.played(play.speed), expectedRevision:play.revision) }
            }
    }
    @ViewBuilder private func audioControls(_ q: ListeningQuestion,s: ListeningSession) -> some View {
        if audio.availability(for:q.audio) == .available {
            VStack(spacing:12) {
                Button { play(q,s:s,speed:.normal) } label: {
                    Label(s.heard ? "もう一度" : "聞く",systemImage:"speaker.wave.2.fill")
                        .font(.headline).fixedSize(horizontal:false,vertical:true).frame(maxWidth:.infinity,minHeight:60)
                }.buttonStyle(.borderedProminent).disabled(busy)
                LearningAudioControlRow {
                    Button { play(q,s:s,speed:.slow) } label: { Text("ゆっくり").fixedSize(horizontal:false,vertical:true).frame(maxWidth:.infinity,minHeight:44) }.disabled(busy)
                    Button { playback = nil; audio.stop() } label: { Text("停止").frame(maxWidth:.infinity,minHeight:44) }.disabled(!audio.isPlaying)
                }
                Text(q.audio.source == .systemTTS ? "システム音声" : "確認用の録音音声").font(.caption).foregroundStyle(.secondary)
            }.frame(maxWidth:600)
        } else if let message = audio.availability(for:q.audio).message {
            Text(message)
            Text("音声が使える状態になってから再開してください。途中の記録は保存されています。").font(.footnote)
        }
        if let message = audio.message { Text(message).font(.footnote) }
    }
    private func play(_ q: ListeningQuestion,s: ListeningSession,speed: AudioSpeed) {
        guard !busy else { return }
        focused = false
        playback = Playback(question:q.id,speed:speed,revision:s.revision)
        if !audio.play(q.audio,speed:speed) { playback = nil }
    }
    private func submit(_ answer: String) {
        guard !busy, !audio.isPlaying, error == nil, session?.heard == true, session?.result == nil,
              !ProductionAnswer.normalize(answer).isEmpty, answer.count <= 500 else { return }
        let revision = session?.revision
        focused = false; Task { await change(.submit(answer), expectedRevision:revision) }
    }
    private func open() async {
        guard !busy else { return }; busy = true; error = nil; empty = false
        defer { busy = false }
        do {
            try await services.progress.configureReviewContentVersion(services.metadata.contentVersion)
            let saved = try await services.progress.activeListening(scope:scope)
            if let saved = saved { session = saved } else {
                var questions: [ListeningQuestion] = []
                if let lessonID = lessonID {
                    let ids = try await services.content.listeningLessonIDs(lesson:lessonID)
                    let rows = try await services.content.listeningQuestions(level:level,ids:ids)
                    let byID = Dictionary(uniqueKeysWithValues:rows.map { ($0.itemID,$0) })
                    guard ids.count == rows.count else { throw GrammarError.changedContent }
                    questions = try ids.map { id in
                        guard let question = byID[id] else { throw GrammarError.changedContent }
                        return question
                    }
                } else if let level = level {
                    let ids = try await services.content.listeningBatchIDs(level:level,batch:batch)
                    questions = try await services.content.listeningQuestions(level:level,ids:ids)
                } else {
                    // Content and progress are separate DBs. Resolve bounded due pages
                    // before snapshot creation; retired IDs must not starve later items.
                    while true {
                        try Task.checkCancellation()
                        let ids = try await services.progress.listeningDue(now:Date()).1
                        if ids.isEmpty { break }
                        questions = try await services.content.listeningQuestions(level:nil,ids:ids)
                        let available = Set(questions.map(\.itemID))
                        let missing = ids.filter { !available.contains($0) }
                        if !missing.isEmpty {
                            try await services.progress.deferUnavailableListening(ids:missing,contentVersion:services.metadata.contentVersion)
                        }
                        if !questions.isEmpty || missing.isEmpty { break }
                        await Task.yield()
                    }
                }
                if questions.isEmpty { session = nil; empty = true; return }
                session = try await services.progress.beginListening(scope:scope,questions:questions,version:services.metadata.contentVersion,review:level == nil)
            }
            draftSequence = max(draftSequence,session?.draftSequence ?? 0)
            input = session?.answer ?? session?.draft ?? ""
        } catch { self.error = LearningErrorMessage.message(for: error) }
    }
    private func saveDraft(_ value: String) {
        guard let s = session, s.current?.task == .dictation, s.result == nil, value.count <= 500 else { return }
        draftSequence += 1
        let sequence = draftSequence
        Task {
            do { try await services.progress.saveListeningDraft(s,text:value,sequence:sequence) }
            catch { self.error = LearningErrorMessage.message(for:error) }
        }
    }
    private func change(_ action: ListeningAction, expectedRevision: Int? = nil) async {
        guard !busy, error == nil, let s = session,
              expectedRevision == nil || expectedRevision == s.revision else { return }
        busy = true
        defer { busy = false }
        do {
            session = try await services.progress.updateListening(s,action:action,now:Date())
            if case .next = action { playback = nil; audio.stop(); input = ""; focused = false }
        } catch { self.error = LearningErrorMessage.message(for: error) }
    }
}
