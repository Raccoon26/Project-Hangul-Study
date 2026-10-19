import SwiftUI

@MainActor
final class ReviewViewModel: ObservableObject {
    let services: AppContainer
    @Published private(set) var session: ReviewSession?
    @Published private(set) var card: VocabularyCard?
    @Published private(set) var busy = false
    @Published private(set) var errorMessage: String?
    @Published private(set) var remainingDue = 0
    @Published private(set) var nothingDue = false
    let practiceID: UUID?
    let sessionLimit: Int
    init(services: AppContainer, practiceID: UUID? = nil, sessionLimit: Int = 20) { self.services = services; self.practiceID = practiceID; self.sessionLimit = min(20,max(1,sessionLimit)) }
    func open() async {
        guard !busy else { return }
        busy = true; errorMessage = nil
        defer { busy = false }
        do {
            if let id = practiceID { session = try await services.progress.reviewSession(id) }
            else { session = try await services.progress.beginReview(now: Date(), limit: sessionLimit) }
            nothingDue = false
            try await loadCard()
        } catch ReviewError.nothingDue { nothingDue = true; card = nil }
        catch { errorMessage = "復習を読み込めませんでした。記録を保ったまま、もう一度お試しください。" }
    }
    func reload() async {
        guard !busy else { return }
        guard let current = session else { await open(); return }
        busy = true; errorMessage = nil
        defer { busy = false }
        do { session = try await services.progress.reviewSession(current.id); try await loadCard() }
        catch { errorMessage = "復習記録を読み込めませんでした。教材と記録は削除されていません。" }
    }
    func reveal(expectedID: ContentID?) async {
        guard !busy, errorMessage == nil, let current = session, let id = current.currentID, id == expectedID else { return }
        busy = true
        defer { busy = false }
        do { session = try await services.progress.revealReview(sessionID: current.id, contentID: id, now: Date()) }
        catch { errorMessage = "保存を確認できませんでした。記録を読み直してください。" }
    }
    func rate(_ rating: ReviewRating, expectedID: ContentID?) async {
        guard !busy, errorMessage == nil, let current = session, current.revealed, let id = current.currentID, id == expectedID else { return }
        busy = true
        defer { busy = false }
        do {
            session = try await services.progress.submitReview(sessionID: current.id, contentID: id, rating: rating,
                now: Date(), timeZoneID: TimeZone.current.identifier)
            try await loadCard()
        } catch { errorMessage = "保存を確認できませんでした。記録を読み直してください。" }
    }
    private func loadCard() async throws {
        card = nil
        guard let current = session, let id = current.currentID else {
            if practiceID == nil { remainingDue = try await services.progress.reviewSummary(now:Date(),timeZoneID:TimeZone.current.identifier).due }
            else { remainingDue = 0 }
            return
        }
        let loaded = try await services.content.vocabularyCard(id: id)
        if !current.exposed {
            session = try await services.progress.exposeReview(sessionID: current.id, contentID: id,
                contentRevision: loaded.revision, contentVersion: services.metadata.contentVersion,
                now: Date(), timeZoneID: TimeZone.current.identifier)
        }
        card = loaded
    }
}
