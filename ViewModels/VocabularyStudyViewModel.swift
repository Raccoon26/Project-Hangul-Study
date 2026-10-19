import SwiftUI

@MainActor
final class VocabularyStudyViewModel: ObservableObject {
    @Published private(set) var set: VocabularyStudySet
    @Published private(set) var session: VocabularySession?
    @Published private(set) var card: VocabularyCard?
    @Published private(set) var busy = false
    @Published private(set) var errorMessage: String?
    @Published private(set) var hasNext = true
    let services: AppContainer
    init(services: AppContainer, set: VocabularyStudySet) { self.services = services; self.set = set }

    func open(restart: Bool = false) async {
        guard !busy else { return }
        busy = true; errorMessage = nil
        defer { busy = false }
        do {
            session = try await services.progress.beginVocabularySet(set.id, contentVersion: services.metadata.contentVersion, restart: restart)
            try await loadCard()
        } catch { errorMessage = LearningErrorMessage.message(for: error) }
    }
    func reload() async {
        guard !busy else { return }
        busy = true; errorMessage = nil
        defer { busy = false }
        do {
            if let current = session { session = try await services.progress.vocabularySession(current.id) }
            else { session = try await services.progress.beginVocabularySet(set.id, contentVersion: services.metadata.contentVersion, restart: false) }
            try await loadCard()
        } catch { errorMessage = LearningErrorMessage.message(for: error) }
    }
    func act(_ action: VocabularyAction, expectedRevision: Int) async {
        guard !busy, errorMessage == nil, let current = session, current.revision == expectedRevision else { return }
        busy = true
        defer { busy = false }
        do {
            session = try await services.progress.updateVocabularySession(current.id, expectedRevision: current.revision, action: action)
            try await loadCard()
        } catch { errorMessage = "保存を確認できませんでした。読み直してから続けてください。\n" + LearningErrorMessage.message(for: error) }
    }
    func nextSet() async {
        guard !busy, session?.completed == true else { return }
        busy = true; errorMessage = nil
        defer { busy = false }
        do {
            let existing = try await services.progress.vocabularySets(level: set.level, after: set.number, limit: 1)
            let next: VocabularyStudySet
            if let first = existing.first { next = first }
            else { next = try await VocabularySetCatalog(content: services.content, progress: services.progress).createNext(level: set.level) }
            set = next; card = nil; session = nil
            session = try await services.progress.beginVocabularySet(set.id, contentVersion: services.metadata.contentVersion, restart: false)
            try await loadCard()
        } catch VocabularyStudyError.noNewWords { hasNext = false }
        catch { errorMessage = LearningErrorMessage.message(for: error) }
    }
    private func loadCard() async throws {
        guard let current = session, let id = current.currentID else { card = nil; return }
        card = nil
        let loaded = try await services.content.vocabularyCard(id: id)
        if !current.exposed {
            session = try await services.progress.updateVocabularySession(current.id, expectedRevision: current.revision,
                action: .expose(revision: loaded.revision, contentVersion: services.metadata.contentVersion))
        }
        card = loaded
    }
}
