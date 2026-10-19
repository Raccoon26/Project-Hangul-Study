import Foundation

/// Scans bounded pages only when allocating a new set. Never caches the vocabulary corpus.
struct VocabularySetCatalog: Sendable {
    let content: any ContentRepository
    let progress: any ProgressRepository
    func createNext(level: LearningLevel = .intro, size: Int = 20) async throws -> VocabularyStudySet {
        guard (1...25).contains(size) else { throw VocabularyStudyError.invalidState }
        var cursor: VocabularyCursor?
        var ids: [ContentID] = []
        while ids.count < size {
            try Task.checkCancellation()
            let page = try await content.vocabulary(matching: VocabularyQuery(level: level), after: cursor, limit: 100)
            if page.isEmpty { break }
            let assigned = try await progress.assignedVocabularyIDs(in: page.map(\.id))
            for word in page where !assigned.contains(word.id) {
                ids.append(word.id)
                if ids.count == size { break }
            }
            guard let last = page.last else { break }
            cursor = VocabularyCursor(sortKey: last.sortKey, id: last.id)
            if page.count < 100 { break }
        }
        guard !ids.isEmpty else { throw VocabularyStudyError.noNewWords }
        return try await progress.createVocabularySet(level: level, ids: ids)
    }
}
