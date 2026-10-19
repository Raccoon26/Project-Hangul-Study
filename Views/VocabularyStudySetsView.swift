import SwiftUI

@MainActor
struct VocabularyStudySetsView: View {
    let services: AppContainer
    var level: LearningLevel = .intro
    @EnvironmentObject private var app: AppModel
    @State private var sets: [VocabularyStudySet] = []
    @State private var total = 0
    @State private var resumeSet: VocabularyStudySet?
    @State private var hasMore = false
    @State private var busy = false
    @State private var errorMessage: String?
    @State private var selection: VocabularyStudySet?
    var body: some View {
        List {
            Section {
                Text("\(total)語").font(.title2).monospacedDigit()
                Text("1セット約20語。意味を思い出してから確認し、覚えたい単語だけを次の周で繰り返します。")
                    .foregroundStyle(.secondary)
                Text("一度通過しても、いつでも学び直せます。").font(.footnote).foregroundStyle(.secondary)
            }
            if let resume = resumeSet {
                Section {
                    Button { selection = resume } label: {
                        Label("続きから · \(resume.title)", systemImage: "arrow.right.circle")
                            .frame(minHeight: 44)
                    }.disabled(busy)
                }
            }
            Section("学習セット") {
                ForEach(sets) { set in
                    Button { selection = set } label: {
                        HStack(spacing: 16) {
                            VStack(alignment: .leading, spacing: 6) {
                                Text(set.title).foregroundStyle(.primary)
                                Text("\(set.vocabularyIDs.count)語 · " + (set.hasActiveSession ? "続きから" : set.completedCount > 0 ? "完了・もう一度見る" : "始める"))
                                    .font(.subheadline).foregroundStyle(.secondary)
                            }
                            Spacer()
                            Image(systemName: set.completedCount > 0 ? "checkmark" : "chevron.right").accessibilityHidden(true)
                        }.padding(.vertical, 8).frame(minHeight: 44)
                    }.disabled(busy)
                }
                if hasMore {
                    Button("以前のセットをさらに表示") { Task { await load(more: true) } }.frame(minHeight: 44).disabled(busy)
                }
                Button { Task { await create() } } label: {
                    Label("新しいセットを始める", systemImage: "plus").frame(minHeight: 44)
                }.disabled(busy || total == 0)
            }
            if busy { ProgressView("読み込み中") }
            if let error = errorMessage {
                Section { Text(error).foregroundStyle(.secondary)
                    Button("読み直す") { Task { await load() } }.disabled(busy)
                }
            }
        }.navigationTitle(level.japaneseName + "単語")
            .task { await load() }
            .fullScreenCover(item: $selection, onDismiss: {
                Task { await load(); await app.refreshSummary() }
            }) { set in VocabularyStudySessionView(services: services, set: set) }
    }
    private func load(more: Bool = false) async {
        guard !busy else { return }
        busy = true; errorMessage = nil
        defer { busy = false }
        do {
            total = try await services.content.vocabularyCount(level: level)
            resumeSet = try await services.progress.resumableVocabularySet(level: level)
            let page = try await services.progress.vocabularySets(level: level, after: more ? sets.last?.number ?? 0 : 0, limit: 50)
            if more { sets.append(contentsOf: page) } else { sets = page }
            hasMore = page.count == 50
        } catch { errorMessage = LearningErrorMessage.message(for: error) }
    }
    private func create() async {
        guard !busy else { return }
        busy = true; errorMessage = nil
        defer { busy = false }
        do { selection = try await VocabularySetCatalog(content: services.content, progress: services.progress).createNext(level: level) }
        catch { errorMessage = LearningErrorMessage.message(for: error) }
    }
}
