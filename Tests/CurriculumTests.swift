import XCTest
@testable import HangulStudy

final class CurriculumTests: XCTestCase {
    private func item(_ area: String) -> DiagnosticItem {
        DiagnosticItem(id:ContentID(rawValue:UUID().uuidString),area:area,prompt:"確認",korean:"가",choices:[QuizChoice(id:"a",text:"正答"),QuizChoice(id:"b",text:"別の答え")],correct:"a",accepted:[],audio:nil)
    }
    func testDiagnosticEarlyExitAndStaleTap() throws {
        var s = DiagnosticSession(id:UUID(),contentVersion:13,items:[item("hangul"),item("hangul"),item("vocabulary")])
        try s.answer("b",expectedRevision:0)
        XCTAssertThrowsError(try s.answer("a",expectedRevision:0))
        try s.answer("b",expectedRevision:1)
        XCTAssertTrue(s.ended); XCTAssertNil(s.current); XCTAssertEqual(s.recommendation,.hangul)
        XCTAssertThrowsError(try s.answer("a",expectedRevision:2))
    }
    func testDiagnosticCorrectBranchAndUnassessedAudio() throws {
        var s = DiagnosticSession(id:UUID(),contentVersion:13,items:[item("hangul"),item("hangul"),item("vocabulary"),item("vocabulary"),item("grammar"),item("grammar"),item("production"),item("listening")])
        for _ in 0..<7 { try s.answer("a",expectedRevision:s.revision) }
        try s.answer(nil,expectedRevision:s.revision)
        XCTAssertEqual(s.recommendation,.beginner); XCTAssertTrue(s.ended)
        let restored = try JSONDecoder().decode(DiagnosticSession.self,from:JSONEncoder().encode(s))
        try restored.validate(); XCTAssertEqual(restored.results.count,8); XCTAssertNil(restored.results[7])
    }
    func testEmptyDiagnosticIsRejected() {
        let s = DiagnosticSession(id:UUID(),contentVersion:13,items:[])
        XCTAssertThrowsError(try s.validate())
    }
    func testRealDiagnosticProfileColdResumeAndHistoryPreservation() async throws {
        let content = try SQLiteContentRepository(url:XCTUnwrap(Bundle.main.url(forResource:"content",withExtension:"sqlite")),allowFixture:false)
        let items = try await content.diagnosticItems()
        XCTAssertEqual(items.count,8)
        let production = try XCTUnwrap(items.first { $0.area == "production" })
        let introductory = try await content.curriculumProduction(level:.intro,after:"")
        let introductoryQuestions = try await content.productionQuestions(id:try XCTUnwrap(introductory.first).0)
        XCTAssertTrue(introductoryQuestions.contains { $0.id == production.id })
        XCTAssertEqual(Set(items.map(\.area)),Set(["hangul","vocabulary","grammar","production","listening"]))
        let folder = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try FileManager.default.createDirectory(at:folder,withIntermediateDirectories:true)
        defer { try? FileManager.default.removeItem(at:folder) }
        let schema = try String(contentsOf:XCTUnwrap(Bundle.main.url(forResource:"user-schema-v1",withExtension:"sql")),encoding:.utf8)
        let path = folder.appendingPathComponent("user.sqlite")
        let repo = try SQLiteProgressRepository(url:path,schema:schema,datasetID:"ko-ja-core")
        let initial = try await repo.curriculumProfile(); XCTAssertNil(initial)
        let word = try XCTUnwrap(items.first { $0.area == "vocabulary" })
        try await repo.setFavorite(word.id,enabled:true)
        let s = try await repo.beginDiagnostic(items:items,version:13,restart:false)
        let answered = try await repo.answerDiagnostic(id:s.id,revision:0,answer:s.items[0].correct)
        let cold = try SQLiteProgressRepository(url:path,schema:schema,datasetID:"ko-ja-core")
        let restored = try await cold.beginDiagnostic(items:Array(items.reversed()),version:14,restart:false)
        XCTAssertEqual(restored.id,s.id); XCTAssertEqual(restored.revision,answered.revision)
        XCTAssertEqual(restored.items.map(\.id),s.items.map(\.id))
        for level in [LearningLevel.intro,.intermediate,.maintenance] {
            try await cold.saveCurriculumProfile(CurriculumProfile(level:level,skippedHangul:true))
        }
        let profile = try await cold.curriculumProfile(); XCTAssertEqual(profile?.level,.maintenance)
        let favorites = try await cold.favoriteIDs(); XCTAssertTrue(favorites.contains(word.id))
        let state = try await cold.reviewState(for:word.id,skill:"vocabulary"); XCTAssertNil(state)
    }
    func testDATA08AuthoredCourseUnitsAndAllVocabularyLessons() async throws {
        let url = try XCTUnwrap(Bundle.main.url(forResource:"content",withExtension:"sqlite"))
        let content = try SQLiteContentRepository(url:url,allowFixture:false)
        let courses = try await content.courses()
        let course = try XCTUnwrap(courses.first { $0.title == "初中級・会話と現代生活" })
        XCTAssertEqual(course.lessons.count,47)
        var seen = Set<ContentID>()
        for lesson in course.lessons {
            let steps = try await content.lessonSteps(for:lesson.id)
            XCTAssertLessThanOrEqual(steps.count,20)
            for step in steps {
                XCTAssertEqual(step.kind,.explanation)
                XCTAssertEqual(step.skill,"vocabulary_preview")
                let card = try await content.vocabularyCard(id:step.id)
                XCTAssertEqual(step.symbol,card.headword)
                XCTAssertTrue(step.explanation.contains(try XCTUnwrap(card.meanings.first).text))
                XCTAssertTrue(seen.insert(step.id).inserted)
            }
        }
        XCTAssertEqual(seen.count,911)
    }

}
