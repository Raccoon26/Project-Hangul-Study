import SwiftUI

@MainActor
final class LookupViewModel: ObservableObject {
    @Published var term = ""
    @Published private(set) var entries: [LookupEntry] = []
    @Published private(set) var busy = false
    @Published private(set) var more = false
    @Published private(set) var error: String?
    private var generation = UUID()
    private var loadedTerm = ""
    private var offset = 0
    func search(services: AppContainer) async {
        let token = UUID(); generation = token
        let requested = term
        entries = []; offset = 0; more = false; error = nil; busy = true
        defer { if generation == token { busy = false } }
        do {
            try await Task.sleep(nanoseconds:300_000_000)
            try Task.checkCancellation()
            let rows = try await services.content.lookup(requested,offset:0)
            try Task.checkCancellation()
            guard generation == token, term == requested else { return }
            entries = rows; loadedTerm = requested; offset = rows.count; more = rows.count == 30
        } catch is CancellationError {} catch { if generation == token { self.error = LearningErrorMessage.message(for: error) } }
    }
    func next(services: AppContainer) async {
        guard !busy, more, term == loadedTerm else { return }
        busy = true; let token = generation
        defer { if token == generation { busy = false } }
        do {
            let rows = try await services.content.lookup(loadedTerm,offset:offset)
            guard generation == token, term == loadedTerm else { return }
            entries += rows; offset += rows.count; more = rows.count == 30; error = nil
        } catch { if token == generation { self.error = LearningErrorMessage.message(for: error) } }
    }
}
