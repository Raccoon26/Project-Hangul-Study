import SwiftUI

@MainActor
struct LookupView: View {
    @EnvironmentObject private var app: AppModel
    @StateObject private var model = LookupViewModel()
    @FocusState private var searchFocused: Bool
    private var searchText: Binding<String> {
        Binding(get:{ model.term },set:{ value in
            // A multiline field wraps large text, but Return still submits the
            // search just as the former single-line search bar did.
            if value.rangeOfCharacter(from:.newlines) != nil {
                model.term = value.components(separatedBy:.newlines).joined(separator:" ")
                    .trimmingCharacters(in:.whitespacesAndNewlines)
                searchFocused = false
            } else { model.term = value }
        })
    }
    var body: some View {
        Group {
            if let services = app.container {
                results(services)
                    .scrollDismissesKeyboard(.interactively)
                    .task(id:model.term) { await model.search(services:services) }
            }
        }.navigationTitle("調べる").navigationBarTitleDisplayMode(.inline)
    }
    private func results(_ services: AppContainer) -> some View {
        List {
            Section {
                // A growing field keeps search readable at every text size.
                // Search and cancellation still use the shared query model.
                TextField("検索",text:searchText,prompt:Text("検索").foregroundColor(.primary),axis:.vertical)
                    .textFieldStyle(.roundedBorder).font(.body).focused($searchFocused)
                    .textInputAutocapitalization(.never).autocorrectionDisabled()
                    .submitLabel(.search).onSubmit { searchFocused = false }
                    .accessibilityIdentifier("dictionary-search")
                    .accessibilityLabel("韓国語・日本語で検索")
                if !model.term.isEmpty {
                    Button("検索語を消す") { model.term = "" }.tint(.primary)
                }
            }
            Section {
                NavigationLink { SavedContentView(services:services) } label: { Text("保存した項目・苦手な項目").fixedSize(horizontal:false,vertical:true) }
            }
            if model.term.trimmingCharacters(in:.whitespacesAndNewlines).isEmpty {
                Text("韓国語か日本語で、単語や文法を探せます。").foregroundStyle(Color.primary)
                NavigationLink("最近見た項目") { SavedContentView(services:services,initial:.recent) }
            } else {
                if model.busy { ProgressView("検索中") }
                if !model.busy && model.entries.isEmpty && model.error == nil { Text("見つかりませんでした。基本形や短い言葉でも検索できます。").foregroundStyle(Color.primary) }
                ForEach(model.entries) { entry in
                    NavigationLink { LookupDetailView(services:services,reference:entry.reference) } label: { LookupRow(entry:entry) }
                }
                if model.more { Button("さらに表示") { Task { await model.next(services:services) } }.tint(.primary).disabled(model.busy).frame(minHeight:44) }
            }
            if let error = model.error { Text(error); Button("もう一度検索") { Task { await model.search(services:services) } }.tint(.primary) }
        }
    }
}
@MainActor
struct LookupRow: View {
    let entry: LookupEntry
    var body: some View {
        VStack(alignment:.leading,spacing:8) {
            Text(entry.title).font(.title2)
            Text(entry.meaning).foregroundStyle(Color.primary)
            Text(entry.subtitle + " · " + entry.level.japaneseName).font(.caption).foregroundStyle(Color.primary)
        }.padding(.vertical,8)
    }
}
@MainActor
struct SavedContentView: View {
    let services: AppContainer
    @State private var list: SavedList
    @State private var kind = ""
    @State private var rows: [SavedRow] = []
    @State private var more = false
    @State private var offset = 0
    @State private var loading = false
    @State private var saving = false
    @State private var generation = UUID()
    @State private var error: String?
    @State private var practice: LookupPractice?
    private struct SavedRow: Identifiable {
        let ref: LookupReference; let entry: LookupEntry?
        var id: String { ref.id }
    }
    init(services: AppContainer, initial: SavedList = .favorites) { self.services = services; _list = State(initialValue:initial) }
    private var selection: String { list.rawValue + kind }
    var body: some View {
        List {
            Section {
                Picker("一覧",selection:$list) { ForEach(SavedList.allCases,id:\.self) { Text($0.title).tag($0) } }
                Picker("種類",selection:$kind) { Text("すべて").tag(""); ForEach(LookupKind.allCases,id:\.self) { Text($0.title).tag($0.rawValue) } }
            }.disabled(saving)
            if list == .difficult {
                Text("過去30日以内に繰り返し難しかった復習項目です。最近の結果と復習段階を使い、以前の間違いだけで固定しません。").font(.footnote).foregroundStyle(Color.primary)
            }
            if !rows.isEmpty {
                Section("選んで練習") {
                    ForEach(LookupKind.allCases,id:\.self) { type in
                        if rows.contains(where: { $0.entry?.reference.kind == type }) {
                            Button("この一覧の" + type.title + "を練習 · 最大20項目") { start(type) }.frame(minHeight:44).disabled(saving || loading)
                        }
                    }
                    Text("表示した項目から練習します。途中の自主練習があれば再開します。復習予定は変更しません。").font(.footnote).foregroundStyle(Color.primary)
                }
            }
            if loading { ProgressView() }
            if rows.isEmpty && !loading && error == nil { Text("まだ項目はありません").foregroundStyle(Color.primary) }
            ForEach(rows) { row in
                if let entry = row.entry {
                    NavigationLink { LookupDetailView(services:services,reference:row.ref) } label: { LookupRow(entry:entry) }
                } else {
                    VStack(alignment:.leading,spacing:8) {
                        Text("この教材は現在利用できません").foregroundStyle(Color.primary)
                        if list == .favorites { Button("保存から外す") { remove(row.ref) }.disabled(saving).frame(minHeight:44) }
                    }
                }
            }
            if more { Button("さらに表示") { Task { await load(reset:false) } }.disabled(loading || saving).frame(minHeight:44) }
            if let error = error { Text(error); Button("読み直す") { Task { await load(reset:true) } } }
        }.navigationTitle("学習管理")
            .task(id:selection) { await load(reset:true) }
            .fullScreenCover(item:$practice,onDismiss:{Task { await load(reset:true) }}) { p in
                if p.kind == .vocabulary { ReviewSessionView(services:services,practiceID:p.id) }
                else { GrammarReviewView(services:services,practiceID:p.id) }
            }
    }
    private func load(reset: Bool) async {
        if !reset && loading { return }
        let token = UUID(); generation = token; loading = true; error = nil
        let requested = selection, selectedList = list
        if reset { rows = []; offset = 0; more = false }
        let page = offset
        defer { if token == generation { loading = false } }
        do {
            let refs = try await services.progress.savedReferences(list:selectedList,kind:LookupKind(rawValue:kind),offset:page,now:Date())
            var values: [SavedRow] = []
            for ref in refs {
                try Task.checkCancellation()
                values.append(SavedRow(ref:ref,entry:try await services.content.lookupEntry(ref)))
            }
            try Task.checkCancellation()
            guard token == generation, selection == requested else { return }
            rows += values; offset = page + refs.count; more = refs.count == 30
        } catch is CancellationError {} catch { if token == generation { self.error = LearningErrorMessage.message(for: error) } }
    }
    private func remove(_ ref: LookupReference) {
        guard !saving else { return }; saving = true
        Task {
            defer { saving = false }
            do { try await services.progress.setFavorite(ref,enabled:false); await load(reset:true) }
            catch { self.error = LearningErrorMessage.message(for: error) }
        }
    }
    private func start(_ type: LookupKind) {
        guard !saving else { return }; saving = true
        let refs = Array(rows.compactMap(\.entry).filter { $0.reference.kind == type }.prefix(20)).map(\.reference)
        Task {
            defer { saving = false }
            do {
                for ref in refs {
                    if type == .vocabulary { _ = try await services.content.vocabularyCard(id:ref.contentID) }
                    else { _ = try await services.content.grammarCard(id:ref.contentID) }
                }
                let session = try await services.progress.beginLookupPractice(ids:refs.map(\.contentID),kind:type,now:Date())
                practice = LookupPractice(id:session.id,kind:type)
            } catch { self.error = LearningErrorMessage.message(for: error) }
        }
    }
}
@MainActor
struct LookupPracticeResumeView: View {
    let services: AppContainer
    let id: UUID
    @State private var session: ReviewSession?
    @State private var error: String?
    var body: some View {
        Group {
            if let session = session {
                if session.skill == "grammar" { GrammarReviewView(services:services,practiceID:id) }
                else { ReviewSessionView(services:services,practiceID:id) }
            } else if let error = error { Text(error).padding(24) }
            else { ProgressView() }
        }.task {
            do { let s = try await services.progress.reviewSession(id); guard s.isPractice else { throw ReviewError.invalidState }; session = s }
            catch { self.error = LearningErrorMessage.message(for: error) }
        }
    }
}
