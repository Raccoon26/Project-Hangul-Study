import SwiftUI

@MainActor
final class AppModel: ObservableObject {
    @Published private(set) var container: AppContainer?
    @Published private(set) var introVocabularyCount = 0
    @Published private(set) var beginnerVocabularyCount = 0
    @Published private(set) var beginnerResumeSet: VocabularyStudySet?
    @Published private(set) var listeningDue = 0
    @Published private(set) var listeningReviewActive = false
    @Published private(set) var grammarReviews: ReviewSummary = .empty
    @Published private(set) var reviews: ReviewSummary = .empty
    @Published private(set) var introResumeSet: VocabularyStudySet?
    @Published private(set) var words: [Vocabulary] = []
    @Published private(set) var courses: [Course] = []
    @Published private(set) var favorites: Set<ContentID> = []
    @Published private(set) var summary: LearningSummary = .empty
    @Published private(set) var lessonProgress: [ContentID: LessonProgress] = [:]
    @Published private(set) var loading = false
    @Published private(set) var hasMore = false
    @Published var errorMessage: String?
    private let pageSize = 50

    func open() async {
        guard container == nil, !loading else { return }
        loading = true
        errorMessage = nil
        defer { loading = false }
        do {
            let services = try await AppContainer.open()
            container = services
        } catch { errorMessage = "データを読み込めませんでした。もう一度お試しください。\n\(LearningErrorMessage.message(for: error))" }
    }
    func loadLegacyWords() async {
        guard let container = container, words.isEmpty, !loading else { return }
        loading = true; defer { loading = false }
        do {
            words = try await container.content.vocabulary(after:nil,limit:pageSize)
            favorites = try await container.progress.favoriteIDs()
            hasMore = words.count == pageSize
        } catch { errorMessage = "単語を読み込めませんでした" }
    }
    func loadMore() async {
        guard let container = container, let last = words.last, hasMore, !loading else { return }
        loading = true
        defer { loading = false }
        do {
            let page = try await container.content.vocabulary(after: VocabularyCursor(sortKey: last.sortKey, id: last.id), limit: pageSize)
            words.append(contentsOf: page)
            hasMore = page.count == pageSize
        } catch { errorMessage = "単語を読み込めませんでした" }
    }
    func toggleFavorite(_ id: ContentID) async {
        guard let container = container else { return }
        do {
            try await container.progress.setFavorite(id, enabled: !favorites.contains(id))
            favorites = try await container.progress.favoriteIDs()
            summary = try await container.progress.summary(now: Date())
        } catch { errorMessage = "保存できませんでした。もう一度お試しください" }
    }
    func refreshSummary() async {
        guard let container = container else { return }
        do {
            introVocabularyCount = try await container.content.vocabularyCount(level: .intro)
            beginnerVocabularyCount = try await container.content.vocabularyCount(level: .beginner)
            listeningDue = try await container.progress.listeningDue(now: Date()).0
            listeningReviewActive = try await container.progress.activeListening(scope: "review") != nil
            grammarReviews = try await container.progress.grammarReviewSummary(now: Date())
            reviews = try await container.progress.reviewSummary(now: Date(), timeZoneID: TimeZone.current.identifier)
            introResumeSet = try await container.progress.resumableVocabularySet(level: .intro)
            beginnerResumeSet = try await container.progress.resumableVocabularySet(level: .beginner)
            lessonProgress = Dictionary(uniqueKeysWithValues: try await container.progress.lessonProgress().map { ($0.lessonID, $0) })
        }
        catch { errorMessage = "学習記録を読み込めませんでした" }
    }
}
