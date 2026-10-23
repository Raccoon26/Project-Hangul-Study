import SwiftUI

@MainActor
struct LearnView: View {
    @Environment(\.dynamicTypeSize) private var dynamicTypeSize
    @EnvironmentObject private var model: AppModel
    @EnvironmentObject private var preferences: LearningPreferencesStore
    @State private var shortReview = false
    @Environment(\.scenePhase) private var scenePhase
    @State private var profile: CurriculumProfile?
    @State private var resume: CurriculumRoute?
    @State private var launch: CurriculumRoute?
    @State private var error: String?
    @State private var loaded = false
    private var due: Int { model.reviews.due + model.grammarReviews.due + model.listeningDue }
    var body: some View {
        List {
            Section {
                Text("한국어").font(.largeTitle).accessibilityLabel("韓国語")
                Text("少しずつ、長く学ぶ").foregroundStyle(.primary).fixedSize(horizontal:false,vertical:true)
            }
            if let services = model.container {
                if loaded && profile == nil {
                    Section {
                        NavigationLink("学習の開始位置を選ぶ") { PlacementView(services:services) }
                        Text("初めての方も、学習経験のある方も。短い確認で始められます。既存の学習記録はそのまま残ります。").font(.subheadline).foregroundStyle(.primary).fixedSize(horizontal:false,vertical:true)
                    } header: { Text("はじめに").foregroundStyle(.primary).fixedSize(horizontal:false,vertical:true) }
                }
                Section {
                    if let resume = resume {
                        Button { launch = resume } label: {
                            Text(resume.title).font(.body).fixedSize(horizontal:false,vertical:true).frame(minHeight:44)
                        }
                    } else if due > 0 || model.reviews.hasActiveSession || model.grammarReviews.hasActiveSession || model.listeningReviewActive {
                        NavigationLink("今日の復習に進む") { CurriculumReviewView(services:services) }
                    } else {
                        NavigationLink("\((profile?.level ?? .hangul).japaneseName)を学ぶ") { CurriculumLevelView(services:services,level:profile?.level ?? .hangul) }
                    }
                } header: { Text("続きから").foregroundStyle(.primary).fixedSize(horizontal:false,vertical:true) }
                Section {
                    if model.reviews.due > 0 || model.reviews.hasActiveSession {
                        Button(model.reviews.hasActiveSession ? "短く復習 · 保存した続きから" : "短く復習 · \(preferences.value.amount.count)語") { shortReview = true }.frame(minHeight:44)
                    }
                    NavigationLink("\(due)項目 · 復習を確認") { CurriculumReviewView(services:services) }
                    Text("復習と新しい学習は、どちらからでも始められます。").font(.footnote).foregroundStyle(.primary).fixedSize(horizontal:false,vertical:true)
                } header: { Text("今日の復習").foregroundStyle(.primary).fixedSize(horizontal:false,vertical:true) }
                Section {
                    NavigationLink((profile?.level ?? .hangul).japaneseName) { CurriculumLevelView(services:services,level:profile?.level ?? .hangul) }
                    NavigationLink("維持学習") { MaintenanceView(services:services) }
                    NavigationLink("すべての学習段階") { CurriculumView(services:services) }
                    NavigationLink("開始位置・レベル診断") { PlacementView(services:services) }
                } header: { Text("現在のコース").foregroundStyle(.primary).fixedSize(horizontal:false,vertical:true) }
            }
            if let error = error { Text(error); Button("読み直す") { Task { await refresh() } } }
        }.listStyle(.insetGrouped).navigationTitle("学ぶ").navigationBarTitleDisplayMode(dynamicTypeSize.isAccessibilitySize ? .inline : .large)
            .task { await refresh() }
            .fullScreenCover(isPresented:$shortReview,onDismiss:{Task { await refresh() }}) {
                if let services = model.container { ReviewSessionView(services:services,sessionLimit:preferences.value.amount.count) }
            }
            .onChange(of:scenePhase) { if $0 == .active { Task { await refresh() } } }
            .onReceive(NotificationCenter.default.publisher(for:.NSCalendarDayChanged)) { _ in Task { await refresh() } }
            .onReceive(NotificationCenter.default.publisher(for:UIApplication.significantTimeChangeNotification)) { _ in Task { await refresh() } }
            .fullScreenCover(item:$launch,onDismiss:{Task { await refresh() }}) { route in
                if let services = model.container { CurriculumResumeView(services:services,route:route) }
            }
    }
    private func refresh() async {
        await model.refreshSummary()
        guard let services = model.container else { return }
        do {
            profile = try await services.progress.curriculumProfile()
            resume = try await services.progress.curriculumResume()
            loaded = true; error = nil
        } catch { self.error = LearningErrorMessage.message(for: error) }
    }
}
