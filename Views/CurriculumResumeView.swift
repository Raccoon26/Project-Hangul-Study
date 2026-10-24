import SwiftUI

@MainActor
struct CurriculumResumeView: View {
    let services: AppContainer
    let route: CurriculumRoute
    @Environment(\.dismiss) private var dismiss
    @State private var set: VocabularyStudySet?
    @State private var lesson: GrammarLesson?
    @State private var course: Course?
    @State private var index = 0
    @State private var error: String?
    var body: some View {
        NavigationStack {
            Group {
                switch route.kind {
                case "practice":
                    if let id = UUID(uuidString:route.target) { LookupPracticeResumeView(services:services,id:id) } else { Text("練習記録を確認できません") }
                case "vocabulary":
                    if let set = set { VocabularyStudySessionView(services:services,set:set) } else { waiting }
                case "grammar":
                    if let lesson = lesson { GrammarStudyView(services:services,lesson:lesson) } else { waiting }
                case "production": ProductionStudyView(services:services,id:ContentID(rawValue:route.target))
                case "listening":
                    let parts = route.target.split(separator:":").map(String.init)
                    ListeningStudyView(services:services,level:parts.count >= 2 ? LearningLevel(rawValue:parts[1]) : nil,batch:parts.count >= 3 ? (Int(parts[2]) ?? 0) : 0,resumeScope:route.target,lessonID:parts.count == 3 && parts[0] == "lesson" ? ContentID(rawValue:parts[2]) : nil)
                case "lesson":
                    if let course = course { LessonFlowView(services:services,course:course,start:index) } else { waiting }
                default:
                    if route.target == "grammar" { GrammarReviewView(services:services) }
                    else { ReviewSessionView(services:services) }
                }
            }
            // These sessions already provide an accessible close action in
            // their own header. A second navigation bar displaced the card.
            .toolbar(usesSessionHeader ? .hidden : .visible,for:.navigationBar)
            .toolbar {
                if !usesSessionHeader {
                    ToolbarItem(placement:.navigationBarLeading) { Button("閉じる") { dismiss() } }
                }
            }
        }.task { await load() }
    }
    private var usesSessionHeader: Bool {
        switch route.kind {
        case "vocabulary": return set != nil
        case "grammar": return lesson != nil
        case "lesson": return course != nil
        case "review": return true
        default: return false
        }
    }
    private var waiting: some View {
        VStack(spacing:20) {
            if let error = error { Text(error); Button("読み直す") { Task { await load() } } } else { ProgressView() }
        }.padding(24)
    }
    private func load() async {
        do {
            switch route.kind {
            case "vocabulary":
                guard let id = UUID(uuidString:route.target) else { throw GrammarError.invalidState }
                set = try await services.progress.curriculumVocabularySet(id:id)
            case "grammar":
                for level in LearningLevel.allCases {
                    var after = -1
                    while true {
                        let rows = try await services.content.grammarLessons(level:level,after:after,limit:30)
                        if let found = rows.first(where: { $0.id.rawValue == route.target }) { lesson = found; return }
                        guard rows.count == 30, let last = rows.last else { break }
                        after = last.order
                    }
                }
                throw GrammarError.changedContent
            case "lesson":
                let courses = try await services.content.courses()
                for c in courses {
                    if let i = c.lessons.firstIndex(where: { $0.id.rawValue == route.target }) { course = c; index = i; return }
                }
                throw GrammarError.changedContent
            default: break
            }
            error = nil
        } catch { self.error = LearningErrorMessage.message(for: error) }
    }
}
