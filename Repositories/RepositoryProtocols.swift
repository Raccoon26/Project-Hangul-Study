import Foundation

protocol ContentRepository: Sendable {
    func lookup(_ term: String, offset: Int) async throws -> [LookupEntry]
    func lookupEntry(_ reference: LookupReference) async throws -> LookupEntry?
    func vocabularyDetail(id: ContentID) async throws -> VocabularyDetail
    func relatedLookup(_ reference: LookupReference) async throws -> [LookupEntry]

    func curriculumIDs(level: LearningLevel, kind: String, after: String) async throws -> [ContentID]
    func curriculumProduction(level: LearningLevel, after: String) async throws -> [(ContentID,String)]
    func diagnosticItems() async throws -> [DiagnosticItem]

    func listeningBatches(level: LearningLevel, after: Int) async throws -> [(Int,Int)]
    func listeningBatchIDs(level: LearningLevel, batch: Int) async throws -> [ContentID]
    func listeningQuestions(level: LearningLevel?, ids: [ContentID]?) async throws -> [ListeningQuestion]
    func listeningCourses(level: LearningLevel) async throws -> [Course]
    func listeningLessonIDs(lesson: ContentID) async throws -> [ContentID]
    func listeningContext(source: ContentID) async throws -> ListeningContext
    func productionVocabulary(after: String) async throws -> [(ContentID,String)]
    func productionQuestions(id: ContentID) async throws -> [ProductionQuestion]
    func grammarLessons(level: LearningLevel, after: Int, limit: Int) async throws -> [GrammarLesson]
    func grammarIDs(lesson: ContentID) async throws -> [ContentID]
    func grammarCard(id: ContentID) async throws -> GrammarCard
    func grammarSearch(level: LearningLevel, prefix: String, after: String, limit: Int) async throws -> [ContentID]
    func vocabularyCount(level: LearningLevel) async throws -> Int
    func vocabularyCard(id: ContentID) async throws -> VocabularyCard

    func metadata() async throws -> ContentMetadata
    func vocabulary(after cursor: VocabularyCursor?, limit: Int) async throws -> [Vocabulary]
    func vocabulary(matching query: VocabularyQuery, after cursor: VocabularyCursor?, limit: Int) async throws -> [Vocabulary]
    func examples(for id: ContentID) async throws -> [Example]
    func pronunciationRule(for id: ContentID) async throws -> PronunciationContent?
    func lessonSteps(for lessonID: ContentID) async throws -> [LessonStep]
    func courses() async throws -> [Course]
}
protocol ProgressRepository: Sendable {
    func statistics(now: Date, timeZone: TimeZone) async throws -> LearningStatistics
    func unseenVocabulary(in ids: [ContentID]) async throws -> Int
    func maintenanceWords(now: Date, limit: Int) async throws -> [ContentID]

    func savedReferences(list: SavedList, kind: LookupKind?, offset: Int, now: Date) async throws -> [LookupReference]
    func isFavorite(_ reference: LookupReference) async throws -> Bool
    func setFavorite(_ reference: LookupReference, enabled: Bool) async throws
    func rememberLookup(_ reference: LookupReference, now: Date) async throws
    func beginLookupPractice(ids: [ContentID], kind: LookupKind, now: Date) async throws -> ReviewSession

    func curriculumProfile() async throws -> CurriculumProfile?
    func saveCurriculumProfile(_ value: CurriculumProfile) async throws
    func curriculumResume() async throws -> CurriculumRoute?
    func curriculumCounts(ids: [ContentID], kind: String) async throws -> (Int,Int)
    func diagnosticSession() async throws -> DiagnosticSession?
    func beginDiagnostic(items: [DiagnosticItem], version: Int, restart: Bool) async throws -> DiagnosticSession
    func answerDiagnostic(id: UUID, revision: Int, answer: String?) async throws -> DiagnosticSession
    func curriculumVocabularySet(id: UUID) async throws -> VocabularyStudySet

    func activeListening(scope: String) async throws -> ListeningSession?
    func listeningDue(now: Date) async throws -> (Int, [ContentID])
    func deferUnavailableListening(ids: [ContentID], contentVersion: Int) async throws
    func beginListening(scope: String, questions: [ListeningQuestion], version: Int, review: Bool) async throws -> ListeningSession
    func updateListening(_ expected: ListeningSession, action: ListeningAction, now: Date) async throws -> ListeningSession
    func saveListeningDraft(_ expected: ListeningSession, text: String, sequence: Int) async throws
    func activeProduction(scope: ContentID) async throws -> ProductionSession?
    func beginProduction(scope: ContentID, questions: [ProductionQuestion], version: Int) async throws -> ProductionSession
    func updateProduction(_ expected: ProductionSession, answer: String?) async throws -> ProductionSession
    func saveProductionDraft(_ expected: ProductionSession, text: String, sequence: Int) async throws
    func grammarStatuses(ids: [ContentID]) async throws -> [GrammarLessonStatus]
    func beginGrammar(lesson: ContentID, ids: [ContentID], contentVersion: Int, restart: Bool) async throws -> GrammarSession
    func grammarSession(id: UUID) async throws -> GrammarSession
    func updateGrammar(id: UUID, revision: Int, action: GrammarAction, contentRevision: Int, contentVersion: Int) async throws -> GrammarSession
    func grammarReviewSummary(now: Date) async throws -> ReviewSummary
    func beginGrammarReview(now: Date) async throws -> ReviewSession
    func prepareGrammarReview(sessionID: UUID, contentID: ContentID, question: GrammarQuestion) async throws -> GrammarReviewQuestion
    func answerGrammarReview(sessionID: UUID, contentID: ContentID, choice: String, contentRevision: Int, contentVersion: Int) async throws -> GrammarReviewQuestion
    func backfillVocabularyReviews(timeZoneID: String) async throws
    func reviewSummary(now: Date, timeZoneID: String) async throws -> ReviewSummary
    func reviewState(for id: ContentID, skill: String) async throws -> SRSState?
    func beginReview(now: Date, limit: Int) async throws -> ReviewSession
    func configureReviewContentVersion(_ version: Int) async throws
    func deferUnavailableReview(sessionID: UUID, contentID: ContentID, contentVersion: Int, now: Date) async throws -> ReviewSession
    func reviewSession(_ id: UUID) async throws -> ReviewSession
    func exposeReview(sessionID: UUID, contentID: ContentID, contentRevision: Int, contentVersion: Int, now: Date, timeZoneID: String) async throws -> ReviewSession
    func revealReview(sessionID: UUID, contentID: ContentID, now: Date) async throws -> ReviewSession
    func submitReview(sessionID: UUID, contentID: ContentID, rating: ReviewRating, now: Date, timeZoneID: String) async throws -> ReviewSession

    func resumableVocabularySet(level: LearningLevel) async throws -> VocabularyStudySet?
    func vocabularySets(level: LearningLevel, after number: Int, limit: Int) async throws -> [VocabularyStudySet]
    func assignedVocabularyIDs(in ids: [ContentID]) async throws -> Set<ContentID>
    func createVocabularySet(level: LearningLevel, ids: [ContentID]) async throws -> VocabularyStudySet
    func beginVocabularySet(_ setID: UUID, contentVersion: Int, restart: Bool) async throws -> VocabularySession
    func vocabularySession(_ id: UUID) async throws -> VocabularySession
    func updateVocabularySession(_ id: UUID, expectedRevision: Int, action: VocabularyAction) async throws -> VocabularySession

    func beginLesson(_ lessonID: ContentID, steps: [ContentID], contentVersion: Int, restart: Bool) async throws -> LessonSession
    func lessonResults(sessionID: UUID) async throws -> [LessonStepResult]
    func submitStep(sessionID: UUID, event: StudyEvent, selectedChoiceID: String?) async throws
    func advanceLesson(sessionID: UUID) async throws -> LessonSession
    func lessonProgress() async throws -> [LessonProgress]
    func favoriteIDs() async throws -> Set<ContentID>
    func setFavorite(_ id: ContentID, enabled: Bool) async throws
    func record(_ event: StudyEvent) async throws
    func summary(now: Date) async throws -> LearningSummary
}
