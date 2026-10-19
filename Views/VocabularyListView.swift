import SwiftUI

@MainActor
struct VocabularyListView: View {
    @EnvironmentObject private var model: AppModel
    var body: some View {
        List {
            if model.container?.metadata.isFixture == true { Section { FixtureNotice() } }
            if model.words.isEmpty { Text("単語はまだ収録されていません") }
            ForEach(model.words) { word in
                NavigationLink {
                    VocabularyDetailView(word: word)
                } label: {
                    HStack(alignment: .firstTextBaseline) {
                        VStack(alignment: .leading, spacing: 8) {
                            Text(word.headword).font(.title2)
                            Text(word.meaning).font(.body).foregroundStyle(.secondary)
                        }
                        Spacer(minLength: 12)
                        if model.favorites.contains(word.id) {
                            Image(systemName: "bookmark.fill").foregroundStyle(.tint).accessibilityLabel("保存済み")
                        }
                    }.padding(.vertical, 8)
                }
            }
            if model.hasMore {
                Button("さらに表示") { Task { await model.loadMore() } }
                    .disabled(model.loading).frame(minHeight: 44)
            }
        }.navigationTitle("単語").task { await model.loadLegacyWords() }
    }
}

@MainActor
struct VocabularyDetailView: View {
    let word: Vocabulary
    @EnvironmentObject private var model: AppModel
    var body: some View {
        if let services = model.container {
            LookupDetailView(services:services,reference:LookupReference(contentID:word.id,kind:.vocabulary))
        }
    }
}
