import SwiftUI

@MainActor
final class GrammarViewModel: ObservableObject {
    let services: AppContainer
    let lesson: GrammarLesson
    @Published private(set) var session: GrammarSession?
    @Published private(set) var card: GrammarCard?
    @Published private(set) var busy = false
    @Published private(set) var error: String?
    init(services: AppContainer, lesson: GrammarLesson) { self.services = services; self.lesson = lesson }
    func open(restart: Bool = false) async {
        guard !busy else { return }; busy = true; error = nil
        defer { busy = false }
        do {
            let ids = try await services.content.grammarIDs(lesson: lesson.id)
            session = try await services.progress.beginGrammar(lesson: lesson.id, ids: ids, contentVersion: services.metadata.contentVersion, restart: restart)
            card = nil; try await load()
        } catch { self.error = LearningErrorMessage.message(for: error) }
    }
    func send(_ action: GrammarAction, expectedRevision: Int) async {
        guard !busy, error == nil, let current = session, current.revision == expectedRevision else { return }
        busy = true; defer { busy = false }
        do {
            session = try await services.progress.updateGrammar(id: current.id, revision: current.revision, action: action,
                contentRevision: card?.revision ?? 1, contentVersion: services.metadata.contentVersion)
            try await load()
        } catch { self.error = LearningErrorMessage.message(for: error) }
    }
    private func load() async throws {
        guard let current = session, let id = current.currentID else { card = nil; return }
        if card?.id != id { card = try await services.content.grammarCard(id: id) }
        guard let loaded = card else { throw GrammarError.changedContent }
        if !current.exposed {
            session = try await services.progress.updateGrammar(id: current.id, revision: current.revision, action: .expose(loaded.questions),
                contentRevision: loaded.revision, contentVersion: services.metadata.contentVersion)
        }
    }
}

@MainActor
final class GrammarReviewViewModel: ObservableObject {
    let services: AppContainer
    @Published private(set) var session: ReviewSession?
    @Published private(set) var card: GrammarCard?
    @Published private(set) var question: GrammarReviewQuestion?
    @Published private(set) var busy = false
    @Published private(set) var error: String?
    @Published private(set) var empty = false
    @Published private(set) var due = 0
    let practiceID: UUID?
    init(services: AppContainer, practiceID: UUID? = nil) { self.services = services; self.practiceID = practiceID }
    func open() async {
        guard !busy else { return }; busy = true; error = nil
        defer { busy = false }
        do {
            if let id = practiceID { session = try await services.progress.reviewSession(id) }
            else { session = try await services.progress.beginGrammarReview(now: Date()) }; empty = false
            try await load()
        } catch ReviewError.nothingDue { empty = true; due = 0; session = nil; card = nil; question = nil }
        catch { self.error = LearningErrorMessage.message(for: error) }
    }
    private func load() async throws {
        card = nil; question = nil
        guard let current = session, let id = current.currentID else {
            if practiceID == nil { due = try await services.progress.grammarReviewSummary(now:Date()).due }
            else { due = 0 }; return
        }
        let loaded = try await services.content.grammarCard(id: id)
        let state = try await services.progress.reviewState(for: id, skill: "grammar")
        let index = (state?.reviewCount ?? 0) % loaded.questions.count
        question = try await services.progress.prepareGrammarReview(sessionID: current.id, contentID: id, question: loaded.questions[index])
        if !current.exposed {
            session = try await services.progress.exposeReview(sessionID: current.id, contentID: id, contentRevision: loaded.revision,
                contentVersion: services.metadata.contentVersion, now: Date(), timeZoneID: TimeZone.current.identifier)
        }
        card = loaded
    }
    func answer(_ choice: String, expectedQuestionID: ContentID) async {
        guard !busy, error == nil, let current = session, let id = current.currentID, question?.question.id == expectedQuestionID else { return }
        busy = true; defer { busy = false }
        do {
            question = try await services.progress.answerGrammarReview(sessionID: current.id, contentID: id, choice: choice, contentRevision: card?.revision ?? 1, contentVersion: services.metadata.contentVersion)
            session = try await services.progress.reviewSession(current.id)
        } catch { self.error = LearningErrorMessage.message(for: error) }
    }
    func rate(_ rating: ReviewRating, expectedQuestionID: ContentID) async {
        guard !busy, error == nil, let current = session, let id = current.currentID, question?.selected != nil, question?.question.id == expectedQuestionID else { return }
        busy = true; defer { busy = false }
        do {
            session = try await services.progress.submitReview(sessionID: current.id, contentID: id, rating: rating, now: Date(), timeZoneID: TimeZone.current.identifier)
            try await load()
        } catch { self.error = LearningErrorMessage.message(for: error) }
    }
}
