import Foundation

/// Self-recall within one attempt, deliberately independent of SRS/acquisition status.
enum VocabularyPassEngine {
    static func start(setID: UUID, ids: [ContentID], contentVersion: Int, seed: UInt64,
                      now: Date = Date()) throws -> VocabularySession {
        let state = VocabularySession(id: UUID(), setID: setID, vocabularyIDs: ids,
            contentVersionAtStart: contentVersion, seed: seed, startedAt: now, updatedAt: now,
            order: ids, passID: UUID())
        try state.validate()
        return state
    }
    static func applying(_ action: VocabularyAction, to original: VocabularySession,
                         now: Date = Date()) throws -> VocabularySession {
        try original.validate()
        guard !original.completed else { throw VocabularyStudyError.invalidState }
        var state = original
        switch action {
        case .expose(let revision, let version):
            guard state.currentID != nil, revision > 0, version > 0 else { throw VocabularyStudyError.invalidState }
            if state.exposed { return state }
            state.exposed = true; state.totalExposures += 1
        case .reveal:
            guard state.currentID != nil, state.exposed else { throw VocabularyStudyError.invalidState }
            if state.revealed { return state }
            state.revealed = true
        case .decide(let decision):
            guard let id = state.currentID, state.revealed else { throw VocabularyStudyError.invalidState }
            if decision == .known { state.passed.append(id) } else { state.deferred.append(id) }
            state.position += 1; state.exposed = false; state.revealed = false
            if state.position == state.order.count && state.deferred.isEmpty { state.completedAt = now }
        case .nextRound:
            guard state.needsNextRound, !state.deferred.isEmpty else { throw VocabularyStudyError.invalidState }
            state.round += 1
            let order = RecallOrder.next(state.deferred, previous: state.order,
                seed: state.seed &+ UInt64(state.round), scope: ContentID(rawValue: state.setID.uuidString))
            state.order = order; state.position = 0; state.passed = []; state.deferred = []
            state.passID = UUID(); state.exposed = false; state.revealed = false
        }
        state.revision += 1; state.updatedAt = now
        try state.validate()
        return state
    }
}
