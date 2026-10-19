import Foundation

struct AppContainer: Sendable {
    let content: any ContentRepository
    let progress: any ProgressRepository
    let metadata: ContentMetadata

    static func open(bundle: Bundle = .main) async throws -> AppContainer {
        #if DEBUG
        let resource = "content"
        let allowFixture = false
        let progressName = "user-production-development.sqlite"
        #else
        let resource = "content"
        let allowFixture = false
        let progressName = "user.sqlite"
        #endif
        guard let contentURL = bundle.url(forResource: resource, withExtension: "sqlite"),
              let schemaURL = bundle.url(forResource: "user-schema-v1", withExtension: "sql") else {
            throw DatabaseError.invalidData("Missing bundled database resources")
        }
        let content = try SQLiteContentRepository(url: contentURL, allowFixture: allowFixture)
        let metadata = try await content.metadata()
        let base = try FileManager.default.url(for: .applicationSupportDirectory, in: .userDomainMask, appropriateFor: nil, create: true)
        let directory = base.appendingPathComponent("HangulStudy", isDirectory: true)
        try FileManager.default.createDirectory(at: directory, withIntermediateDirectories: true,
                                                attributes: [.protectionKey: FileProtectionType.completeUntilFirstUserAuthentication])
        let progress = try SQLiteProgressRepository(url: directory.appendingPathComponent(progressName),
                                                    schema: String(contentsOf: schemaURL, encoding: .utf8), datasetID: metadata.datasetID)
        try await progress.configureReviewContentVersion(metadata.contentVersion)
        try await progress.backfillVocabularyReviews(timeZoneID: TimeZone.current.identifier)
        return AppContainer(content: content, progress: progress, metadata: metadata)
    }
}
