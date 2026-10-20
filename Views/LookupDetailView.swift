import SwiftUI

@MainActor
struct LookupDetailView: View {
    let services: AppContainer
    let reference: LookupReference
    @EnvironmentObject private var audio: KoreanAudioService
    @Environment(\.scenePhase) private var phase
    @State private var entry: LookupEntry?
    @State private var word: VocabularyDetail?
    @State private var grammar: GrammarCard?
    @State private var related: [LookupEntry] = []
    @State private var favorite = false
    @State private var inReview = false
    @State private var loading = true
    @State private var saving = false
    @State private var error: String?
    @State private var practice: LookupPractice?
    @State private var generation = UUID()
    var body: some View {
        ScrollView {
            VStack(alignment:.leading,spacing:24) {
                if loading { ProgressView() }
                if let word = word {
                    VocabularyCardContentView(card:word.card,revealed:true)
                    if let reading = word.pronunciation { Text("発音の目安：[\(reading)]").font(.subheadline).foregroundStyle(.secondary) }
                    if !extraExamples(word).isEmpty {
                        DisclosureGroup("ほかの例文") { VStack(alignment:.leading,spacing:20) { ForEach(extraExamples(word)) { GrammarExampleView(example:$0) } }.padding(.top,12) }
                    }
                    if word.card.notes.count > 1 {
                        DisclosureGroup("ほかのポイント") { ForEach(Array(word.card.notes.dropFirst())) { note in VStack(alignment:.leading) { Text(note.title).font(.headline); Text(note.text) }.padding(.vertical,8) } }
                    }
                    if !word.conjugations.isEmpty {
                        DisclosureGroup("主な活用") {
                            VStack(alignment:.leading,spacing:16) {
                                if word.irregular { Text("不規則な形を含みます").font(.footnote).foregroundStyle(.secondary) }
                                ForEach(word.conjugations) { form in VStack(alignment:.leading,spacing:6) { Text(form.form.title).font(.subheadline); Text(form.result.form).font(.title2) } }
                            }.padding(.top,12)
                        }
                    }
                }
                if let grammar = grammar {
                    GrammarExplanationView(card:grammar,page:0)
                    Text("形と使い方").font(.headline)
                    Text(grammar.form).font(.title3)
                    if let text = grammar.constraints { Text(text).foregroundStyle(.secondary) }
                    ForEach(grammar.examples) { GrammarExampleView(example:$0) }
                    if let note = grammar.note { Text("ポイント").font(.headline); Text(note).foregroundStyle(.secondary) }
                    if !grammar.comparisons.isEmpty {
                        DisclosureGroup("似た表現との違い") {
                            VStack(alignment:.leading,spacing:20) {
                                ForEach(grammar.comparisons) { item in
                                    NavigationLink { LookupDetailView(services:services,reference:LookupReference(contentID:item.id,kind:.grammar)) } label: { Text(item.pattern).font(.title2) }
                                    Text(item.difference).foregroundStyle(.secondary)
                                }
                            }.padding(.top,12)
                        }
                    }
                }
                if entry != nil {
                    Text(inReview ? "復習中 · 予定は学習画面で確認できます" : "調べただけでは学習完了になりません").font(.footnote).foregroundStyle(.secondary)
                    Button { toggle() } label: { Label(favorite ? "保存を解除" : "保存する",systemImage:favorite ? "bookmark.fill" : "bookmark").frame(minHeight:44) }.disabled(saving)
                    if word != nil || grammar != nil {
                        Button("もう一度学ぶ") { start() }.buttonStyle(.borderedProminent).controlSize(.large).disabled(saving)
                        Text("意味や問題を確認する自主練習です。途中の練習は再開し、既存の復習予定は変更しません。").font(.footnote).foregroundStyle(.secondary)
                    }
                    if word?.hasProductionPractice == true {
                        NavigationLink("活用・入力を練習") { ProductionStudyView(services:services,id:reference.contentID) }
                    }
                    if let entry = entry { NavigationLink("コースで順番に学ぶ") { CurriculumLevelView(services:services,level:entry.level) } }
                    if !related.isEmpty {
                        DisclosureGroup("関連する単語・文法") {
                            ForEach(related) { item in
                                NavigationLink { LookupDetailView(services:services,reference:item.reference) } label: { LookupRow(entry:item) }
                            }
                        }
                    }
                }
                if let error = error { Text(error); Button("読み直す") { Task { await load() } }.disabled(loading || saving) }
            }.frame(maxWidth:600,alignment:.leading).padding(24).frame(maxWidth:.infinity)
        }.navigationTitle(reference.kind.title).navigationBarTitleDisplayMode(.inline)
            .task(id:reference) { await load() }
            .onDisappear { audio.stop() }
            .onChange(of:phase) { if $0 != .active { audio.stop() } }
            .fullScreenCover(item:$practice,onDismiss:{Task { await load() }}) { p in
                if p.kind == .vocabulary { ReviewSessionView(services:services,practiceID:p.id) }
                else { GrammarReviewView(services:services,practiceID:p.id) }
            }
    }
    private func extraExamples(_ word: VocabularyDetail) -> [Example] {
        let shown = Set(word.card.meanings.compactMap { $0.example?.id })
        return word.examples.filter { !shown.contains($0.id) }
    }
    private func load() async {
        let token = UUID(); generation = token
        loading = true; error = nil; word = nil; grammar = nil; entry = nil; related = []
        favorite = false; inReview = false
        defer { if generation == token { loading = false } }
        do {
            guard let found = try await services.content.lookupEntry(reference) else { throw VocabularyStudyError.missingContent }
            let saved = try await services.progress.isFavorite(reference)
            let loadedWord: VocabularyDetail?
            let loadedGrammar: GrammarCard?
            if reference.kind == .vocabulary { loadedWord = try await services.content.vocabularyDetail(id:reference.contentID); loadedGrammar = nil }
            else { loadedWord = nil; loadedGrammar = try await services.content.grammarCard(id:reference.contentID) }
            let links = try await services.content.relatedLookup(reference)
            let reviewed = try await services.progress.reviewState(for:reference.contentID,skill:reference.kind.rawValue) != nil
            try Task.checkCancellation()
            guard generation == token else { return }
            try await services.progress.rememberLookup(reference,now:Date())
            try Task.checkCancellation()
            guard generation == token else { return }
            entry = found; word = loadedWord; grammar = loadedGrammar; related = links; favorite = saved; inReview = reviewed
        } catch is CancellationError {} catch { if generation == token { self.error = LearningErrorMessage.message(for: error) } }
    }
    private func toggle() {
        guard !saving else { return }; saving = true
        let enabled = !favorite
        Task {
            defer { saving = false }
            do { try await services.progress.setFavorite(reference,enabled:enabled); favorite = enabled }
            catch { self.error = LearningErrorMessage.message(for: error) }
        }
    }
    private func start() {
        guard !saving else { return }; saving = true; audio.stop()
        Task {
            defer { saving = false }
            do {
                let session = try await services.progress.beginLookupPractice(ids:[reference.contentID],kind:reference.kind,now:Date())
                practice = LookupPractice(id:session.id,kind:reference.kind)
            } catch { self.error = LearningErrorMessage.message(for: error) }
        }
    }
}
