import SwiftUI

@MainActor
struct MaintenanceView: View {
    let services: AppContainer
    @State private var candidates: [ContentID] = []
    @State private var practice: LookupPractice?
    @State private var busy = false
    @State private var message: String?
    var body: some View {
        List {
            Section {
                Text("これまで学んだことを、無理なく使い続けましょう。途中で閉じても、回答した分は残ります。")
                NavigationLink("予定された復習をする") { CurriculumReviewView(services:services) }
            }
            Section("使い方を確かめる") {
                NavigationLink("苦手な単語・文法") { SavedContentView(services:services,initial:.difficult) }
                NavigationLink("活用・文を入力する") { ProductionCatalogView(services:services) }
                NavigationLink("聞いて理解する・書き取る") { ListeningCatalogView(services:services) }
            }
            Section("久しぶりの単語") {
                if candidates.isEmpty { Text("今は追加の練習候補がありません。予定された復習から続けられます。").foregroundStyle(.secondary) }
                else { Button("\(candidates.count)語を短く確認") { Task { await start() } }.frame(minHeight:44).disabled(busy) }
                Text("30日以上確認しておらず、復習予定も進行中の回読もない単語が対象です。練習によって既存の復習予定を前倒ししません。").font(.footnote).foregroundStyle(.secondary)
            }
            if let message = message { Text(message); Button("読み直す") { Task { await load() } }.disabled(busy) }
        }.navigationTitle("維持学習").task { await load() }
            .fullScreenCover(item:$practice,onDismiss:{ Task { await load() } }) { p in ReviewSessionView(services:services,practiceID:p.id) }
    }
    private func load() async {
        guard !busy else { return }; busy = true; defer { busy = false }
        do {
            let ids = try await services.progress.maintenanceWords(now:Date(),limit:10)
            var active: [ContentID] = []
            for id in ids {
                if try await services.content.lookupEntry(LookupReference(contentID:id,kind:.vocabulary)) != nil { active.append(id) }
            }
            candidates = active; message = nil
        } catch { message = "練習候補を読み込めませんでした。記録は変更していません。" }
    }
    private func start() async {
        guard !busy, !candidates.isEmpty else { return }; busy = true; defer { busy = false }
        do {
            let session = try await services.progress.beginLookupPractice(ids:candidates,kind:.vocabulary,now:Date())
            practice = LookupPractice(id:session.id,kind:.vocabulary); message = nil
        } catch { message = "練習を開始できませんでした。もう一度お試しください。" }
    }
}
