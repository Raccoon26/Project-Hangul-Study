import SwiftUI

@MainActor
struct CurriculumView: View {
    let services: AppContainer
    var body: some View {
        List {
            Text("このアプリの学習段階です。試験の級とは異なります。どの段階からでも始められます。").font(.subheadline).foregroundStyle(.primary).fixedSize(horizontal:false,vertical:true)
            ForEach(LearningLevel.allCases,id:\.rawValue) { level in
                NavigationLink(level.japaneseName) { CurriculumLevelView(services:services,level:level) }
            }
            NavigationLink("開始位置・レベル診断") { PlacementView(services:services) }
        }.navigationTitle("学習コース")
    }
}
@MainActor
struct CurriculumLevelView: View {
    let services: AppContainer
    let level: LearningLevel
    @State private var counts: [CurriculumCount] = []
    @State private var courses: [Course] = []
    @State private var doneLessons: Set<ContentID> = []
    @State private var launch: LessonLaunch?
    @State private var error: String?
    @State private var loading = true
    @State private var saved = false
    @State private var saving = false
    private struct LessonLaunch: Identifiable { let course: Course; let index: Int; var id: String { course.lessons[index].id.rawValue } }
    private func count(_ kind: String) -> Int { counts.first { $0.kind == kind }?.total ?? 0 }
    var body: some View {
        List {
            Section {
                Button(saved ? "開始位置に設定しました" : "ここから始める") { Task { await select() } }.frame(minHeight:44).disabled(saved || saving)
                Text("開始位置を変えても、学習記録と復習予定は残ります。").font(.footnote).foregroundStyle(.primary).fixedSize(horizontal:false,vertical:true)
            }
            if level == .maintenance {
                Section {
                    Text("終わりを決めず、これまでの内容を復習します。未学習のコースにも戻れます。")
                    NavigationLink("維持学習を始める") { MaintenanceView(services:services) }
                    NavigationLink("活用・入力を練習") { ProductionCatalogView(services:services) }
                    NavigationLink("聞いて確認") { ListeningCatalogView(services:services) }
                }
            } else {
                if loading { ProgressView("進み具合を確認中") }
                if let next = nextLesson {
                    Section {
                        Button(next.course.lessons[next.index].title) { launch = next }.frame(minHeight:44)
                    } header: { Text("次のレッスン").foregroundStyle(.primary).fixedSize(horizontal:false,vertical:true) }
                }
                Section {
                    if count("vocabulary") > 0 { NavigationLink("単語 · 小さなセットで回読") { VocabularyStudySetsView(services:services,level:level) } }
                    if count("grammar") > 0 { NavigationLink("文法 · 意味と使い方") { GrammarCatalogView(services:services,level:level) } }
                    if count("vocabulary") > 0 { NavigationLink("活用・入力練習") { ProductionCatalogView(services:services,level:level) } }
                    if count("listening") > 0 { NavigationLink("リスニング・書き取り") { ListeningBatchView(services:services,level:level) } }
                    NavigationLink("今日の復習 · 全段階") { CurriculumReviewView(services:services) }
                } header: { Text("学ぶ").foregroundStyle(.primary).fixedSize(horizontal:false,vertical:true) }
                ForEach(courses) { course in
                    Section {
                        Text(course.description).font(.subheadline).foregroundStyle(.primary).fixedSize(horizontal:false,vertical:true)
                        ForEach(Array(course.lessons.enumerated()),id:\.element.id) { index,lesson in
                            Button { launch = LessonLaunch(course:course,index:index) } label: {
                                HStack { Text(lesson.title); Spacer(); if doneLessons.contains(lesson.id) { Text("完了").font(.caption) } }.frame(minHeight:44)
                            }
                        }
                    } header: { Text(course.title).foregroundStyle(.primary).fixedSize(horizontal:false,vertical:true) }
                }
                if !loading && counts.allSatisfy({ $0.total == 0 }) {
                    Text("この段階の教材はまだ収録されていません。開始位置は保存でき、収録済みのコースと復習をいつでも利用できます。").foregroundStyle(.primary).fixedSize(horizontal:false,vertical:true)
                    NavigationLink("収録済みの初級コース") { CurriculumLevelView(services:services,level:.beginner) }
                }
                Section {
                    ForEach(counts.filter { $0.total > 0 }) { value in
                        VStack(alignment:.leading,spacing:8) {
                            Text("\(value.title) · \(value.completed) / \(value.total) 確認済み")
                            if value.kind != "lesson" { Text("長期復習が進んだ項目：\(value.stable)").font(.caption).foregroundStyle(.primary).fixedSize(horizontal:false,vertical:true) }
                        }.padding(.vertical,4)
                    }
                    Text("確認済みと長期記憶は別の記録です。教材が増えると総数は増えますが、確認済みの記録は消えません。長期復習は30日以上の段階を目安に表示します。").font(.footnote).foregroundStyle(.primary).fixedSize(horizontal:false,vertical:true).accessibilityIdentifier("curriculum-progress-note")
                } header: { Text("学習の記録").foregroundStyle(.primary).fixedSize(horizontal:false,vertical:true) }
                if !counts.isEmpty && counts.contains(where: { $0.total > 0 }) && counts.allSatisfy({ $0.completed == $0.total }), let next = nextLevel {
                    Section {
                        Text("収録されている内容を一通り確認しました。復習を続けながら次の段階も見てみましょう。")
                        NavigationLink("次の段階："+next.japaneseName) { CurriculumLevelView(services:services,level:next) }
                    }
                }
            }
            if let error = error { Text(error); Button("読み直す") { Task { await load() } } }
        }.navigationTitle(level.japaneseName)
            .task { await load() }
            .fullScreenCover(item:$launch,onDismiss:{ Task { await load() } }) { item in
                LessonFlowView(services:services,course:item.course,start:item.index)
            }
    }
    private var nextLesson: LessonLaunch? {
        for course in courses {
            if let index = course.lessons.firstIndex(where: { !doneLessons.contains($0.id) }) { return LessonLaunch(course:course,index:index) }
        }
        return nil
    }
    private var nextLevel: LearningLevel? {
        guard let i = LearningLevel.allCases.firstIndex(of:level), i+1 < LearningLevel.allCases.count else { return nil }
        return LearningLevel.allCases[i+1]
    }
    private func select() async {
        guard !saving else { return }; saving = true
        defer { saving = false }
        do { try await services.progress.saveCurriculumProfile(CurriculumProfile(level:level,skippedHangul:level != .hangul)); saved = true }
        catch { self.error = LearningErrorMessage.message(for: error) }
    }
    private func load() async {
        loading = true; error = nil
        defer { loading = false }
        do {
            var values: [CurriculumCount] = []; var lessonIDs = Set<ContentID>()
            for kind in ["lesson","vocabulary","grammar","listening"] {
                var count = CurriculumCount(kind:kind); var after = ""
                while true {
                    try Task.checkCancellation()
                    let ids = try await services.content.curriculumIDs(level:level,kind:kind,after:after)
                    if ids.isEmpty { break }
                    let progress = try await services.progress.curriculumCounts(ids:ids,kind:kind)
                    count.total += ids.count; count.completed += progress.0; count.stable += progress.1
                    if kind == "lesson" { lessonIDs.formUnion(ids) }
                    after = ids.last?.rawValue ?? after
                    if ids.count < 200 { break }
                }
                values.append(count)
            }
            counts = values
            courses = try await services.content.courses().compactMap { c in
                let lessons = c.lessons.filter { lessonIDs.contains($0.id) }
                return lessons.isEmpty ? nil : Course(id:c.id,title:c.title,description:c.description,lessons:lessons)
            }
            doneLessons = Set(try await services.progress.lessonProgress().filter { $0.completedCount > 0 }.map(\.lessonID))
        } catch is CancellationError {} catch { self.error = LearningErrorMessage.message(for: error) }
    }
}

@MainActor
struct CurriculumReviewView: View {
    let services: AppContainer
    @EnvironmentObject private var app: AppModel
    @Environment(\.scenePhase) private var phase
    @State private var showWords = false
    @State private var showGrammar = false
    var body: some View {
        List {
            Text("開始位置に関係なく、これまでの復習を続けます。1回最大20項目。残りは次の回に取り組めます。").foregroundStyle(.primary).fixedSize(horizontal:false,vertical:true)
            Button("単語 \(app.reviews.due)語" + (app.reviews.hasActiveSession ? " · 続きから" : "")) { showWords = true }.frame(minHeight:44).disabled(app.reviews.due == 0 && !app.reviews.hasActiveSession)
            Button("文法 \(app.grammarReviews.due)項目" + (app.grammarReviews.hasActiveSession ? " · 続きから" : "")) { showGrammar = true }.frame(minHeight:44).disabled(app.grammarReviews.due == 0 && !app.grammarReviews.hasActiveSession)
            NavigationLink("リスニング \(app.listeningDue)項目" + (app.listeningReviewActive ? " · 続きから" : "")) { ListeningStudyView(services:services,level:nil) }.disabled(app.listeningDue == 0 && !app.listeningReviewActive)
            Text("復習を待つ間も、新しい内容を学べます。").font(.footnote)
        }.navigationTitle("今日の復習").task { await app.refreshSummary() }
            .onChange(of:phase) { if $0 == .active { Task { await app.refreshSummary() } } }
            .onReceive(NotificationCenter.default.publisher(for:.NSCalendarDayChanged)) { _ in Task { await app.refreshSummary() } }
            .fullScreenCover(isPresented:$showWords,onDismiss:{Task { await app.refreshSummary() }}) { ReviewSessionView(services:services) }
            .fullScreenCover(isPresented:$showGrammar,onDismiss:{Task { await app.refreshSummary() }}) { GrammarReviewView(services:services) }
    }
}
