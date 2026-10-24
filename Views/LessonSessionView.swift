import SwiftUI

/// A full-screen flow keeps the app's tab bar outside the learning environment.
@MainActor
struct LessonFlowView: View {
    let services: AppContainer
    @State private var course: Course
    let nextCourse: Course?
    @State private var lessonIndex: Int
    init(services: AppContainer, course: Course, start: Int, nextCourse: Course? = nil) {
        self.services = services; _course = State(initialValue: course); self.nextCourse = nextCourse
        _lessonIndex = State(initialValue: start)
    }
    var body: some View {
        if course.lessons.indices.contains(lessonIndex) {
        LessonSessionView(services: services, lesson: course.lessons[lessonIndex],
            hasNext: lessonIndex + 1 < course.lessons.count || (nextCourse != nil && nextCourse?.id != course.id),
            nextTitle: lessonIndex + 1 < course.lessons.count ? "次のレッスンへ" : "次のコースへ",
            onNext: {
                if lessonIndex + 1 < course.lessons.count { lessonIndex += 1 }
                else if let next = nextCourse, !next.lessons.isEmpty { course = next; lessonIndex = 0 }
            })
            .id(course.lessons[lessonIndex].id)
        } else { Text("このコースには学習できるレッスンがありません。").padding(24) }
    }
}

@MainActor
struct LessonSessionView: View {
    @Environment(\.dismiss) private var dismiss
    @Environment(\.scenePhase) private var scenePhase
    @EnvironmentObject private var audio: KoreanAudioService
    @StateObject private var model: LessonViewModel
    private enum Focus: Hashable { case prompt, feedback }
    @AccessibilityFocusState private var focus: Focus?
    @ScaledMetric(relativeTo: .largeTitle) private var glyphSize: CGFloat = 88
    let hasNext: Bool
    let nextTitle: String
    let onNext: () -> Void
    init(services: AppContainer, lesson: Lesson, hasNext: Bool, nextTitle: String = "次のレッスンへ", onNext: @escaping () -> Void) {
        _model = StateObject(wrappedValue: LessonViewModel(services: services, lesson: lesson))
        self.hasNext = hasNext; self.nextTitle = nextTitle; self.onNext = onNext
    }
    var body: some View {
        VStack(spacing: 0) {
            header
            if !model.steps.isEmpty && !model.completed {
                ProgressView(value: Double(model.index), total: Double(model.steps.count))
                    .padding(.horizontal, 24).accessibilityLabel("レッスンの進み具合")
                    .accessibilityValue("\(model.index + 1) / \(model.steps.count)")
            }
            ScrollViewReader { proxy in
              ScrollView {
                VStack(alignment: .leading, spacing: 24) {
                    if model.completed { completion }
                    else if let step = model.step { lessonContent(step) }
                    else if model.busy { ProgressView("読み込み中") }
                    if let error = model.errorMessage {
                        Text(error).foregroundStyle(.secondary).accessibilityLabel("お知らせ。\(error)")
                        if model.session == nil {
                            Button(model.needsRestart ? "最初から始める" : "もう一度試す") {
                                Task { await model.open(restart: model.needsRestart) }
                            }.buttonStyle(.bordered).disabled(model.busy)
                        }
                    }
                }.frame(maxWidth: 600, alignment: .leading).padding(24)
                    .frame(maxWidth: .infinity).id("lesson-top")
              }
              .onChange(of: model.session?.currentID) { _ in
                  proxy.scrollTo("lesson-top", anchor: .top)
                  focus = .prompt
              }
              .onChange(of: model.currentResult?.contentID) { resultID in
                  if resultID != nil && model.step?.kind == .quiz {
                      proxy.scrollTo("feedback", anchor: .bottom)
                      focus = .feedback
                  }
              }
              .onChange(of: model.completed) { _ in proxy.scrollTo("lesson-top", anchor: .top) }
            }
        }
        .background(Color(uiColor: .systemBackground))
        .safeAreaInset(edge: .bottom, spacing: 0) { bottomAction }
        .interactiveDismissDisabled(model.busy)
        .task { await model.open() }
        .onDisappear { audio.stop() }
        .onChange(of: scenePhase) { phase in if phase != .active { audio.stop() } }
        .onChange(of: model.session?.currentID) { _ in audio.stop() }
        .onChange(of: audio.completedPlaybackCount) { _ in model.markAudioHeard() }
    }
    private var header: some View {
        HStack(alignment: .center, spacing: 12) {
            Button { audio.stop(); dismiss() } label: {
                Image(systemName: "xmark").frame(width: 44, height: 44).contentShape(Rectangle())
            }.accessibilityLabel("レッスンを閉じる。記録は保存されています").disabled(model.busy)
            Text(model.lesson.title).font(.subheadline.weight(.medium)).fixedSize(horizontal: false, vertical: true)
            Spacer(minLength: 0)
            if !model.steps.isEmpty && !model.completed {
                Text("\(model.index + 1) / \(model.steps.count)").font(.caption).monospacedDigit()
                    .foregroundStyle(.secondary).fixedSize()
            }
        }.padding(.horizontal, 12).padding(.vertical, 8)
    }
    @ViewBuilder private func lessonContent(_ step: LessonStep) -> some View {
        if !step.category.isEmpty { Text(step.category).font(.subheadline).foregroundStyle(.secondary) }
        if !step.symbol.isEmpty {
            Text(step.symbol).font(.system(size: step.symbol.count > 5 ? glyphSize * 0.65 : glyphSize, weight: .medium))
                .multilineTextAlignment(.center).frame(maxWidth: .infinity)
                .fixedSize(horizontal: false, vertical: true)
                .accessibilityLabel(step.kind == .character ? "\(step.symbol)、\(step.title)" : step.symbol)
        }
        if let pronunciation = step.pronunciation, step.audio?.usage != .comparison {
            Text(pronunciation.readings.map { "[" + $0 + "]" }.joined(separator: " / "))
                .font(.title2).foregroundStyle(.secondary).frame(maxWidth: .infinity)
                .multilineTextAlignment(.center).accessibilityLabel("学習用発音表記。" + pronunciation.readings.joined(separator: "、または、"))
        }
        if let request = step.audio { audioControls(request, listening: step.requiresListening) }
        Text(step.title).font(step.kind == .character ? .title2 : .title3).fontWeight(.medium)
            .accessibilityAddTraits(.isHeader).accessibilityFocused($focus, equals: .prompt)
        if step.kind == .quiz {
            VStack(spacing: 12) {
                ForEach(model.options) { choice in
                    Button { model.selectedChoiceID = choice.id } label: {
                        HStack(spacing: 16) {
                            Text(choice.text).multilineTextAlignment(.leading).frame(maxWidth: .infinity, alignment: .leading)
                            if model.selectedChoiceID == choice.id { Image(systemName: "checkmark.circle.fill") }
                            else { Image(systemName: "circle").foregroundStyle(.secondary) }
                        }.padding(.horizontal, 16).padding(.vertical, 14).frame(minHeight: 52)
                            .background(model.selectedChoiceID == choice.id ? Color.accentColor.opacity(0.10) : Color(uiColor: .secondarySystemBackground), in: RoundedRectangle(cornerRadius: 12))
                    }.buttonStyle(.plain).disabled(model.currentResult != nil || model.busy)
                        .accessibilityAddTraits(model.selectedChoiceID == choice.id ? [.isSelected] : [])
                }
            }
            if let result = model.currentResult {
                VStack(alignment: .leading, spacing: 12) {
                    Label(result.outcome == .correct ? "正解" : "もう一度確認しましょう",
                          systemImage: result.outcome == .correct ? "checkmark" : "arrow.turn.up.left")
                        .font(.headline).accessibilityAddTraits(.isHeader)
                    if result.outcome != .correct, let correct = step.choices.first(where: { $0.id == step.correctChoiceID }) {
                        Text("正解：\(correct.text)")
                    }
                    Text(step.explanation).foregroundStyle(.secondary)
                }.accessibilityElement(children: .combine).id("feedback")
                    .accessibilityFocused($focus, equals: .feedback)
            }
        } else {
            if step.kind == .character || step.pronunciation?.showComposition == true {
                let formulas = HangulComposition.formulas(for: step.symbol)
                ForEach(formulas.indices, id: \.self) { index in
                    Text(formulas[index]).font(.title2).frame(maxWidth: .infinity)
                        .multilineTextAlignment(.center).fixedSize(horizontal: false, vertical: true)
                }
            }
            Text(step.explanation).font(.body).lineSpacing(5).fixedSize(horizontal: false, vertical: true)
            if let pronunciation = step.pronunciation {
                Text(pronunciation.context).font(.footnote).foregroundStyle(.secondary)
                if !pronunciation.examples.isEmpty {
                    Text("ほかの例").font(.headline)
                    ForEach(pronunciation.examples) { example in
                        VStack(alignment: .leading, spacing: 6) {
                            Text(example.spelling).font(.title2)
                            Text("[\(example.reading)] · \(example.meaning)").foregroundStyle(.secondary)
                        }
                    }
                }
            }
        }
    }
    @ViewBuilder private func audioControls(_ request: LearningAudio, listening: Bool) -> some View {
        let availability = audio.availability(for: request)
        VStack(alignment: .leading, spacing: 8) {
            if availability == .available {
                LearningAudioControlRow { audioButtons(request) }
                Text(request.source == .systemTTS ? "システム音声" : "確認用の録音音声")
                    .font(.caption).foregroundStyle(.secondary)
                if listening && model.currentResult == nil && model.heardStepID != model.step?.id {
                    Text("音声を最後まで聞いてから答えましょう。")
                        .font(.subheadline).foregroundStyle(.secondary)
                }
            } else if let message = availability.message {
                Text(message).font(.subheadline).foregroundStyle(.secondary)
                if listening { Text("記録は保存されています。この問題は音声を利用できるときに再開してください。").font(.footnote).foregroundStyle(.secondary) }
            }
            if let message = audio.message { Text(message).font(.subheadline).foregroundStyle(.secondary) }
        }
    }
    @ViewBuilder private func audioButtons(_ request: LearningAudio) -> some View {
        Button { audio.play(request, speed: .normal) } label: {
            Label("聞く", systemImage: "speaker.wave.2").fixedSize(horizontal:false,vertical:true).frame(maxWidth:.infinity,minHeight:44)
        }.accessibilityLabel("通常の速さで聞く")
        Button { audio.play(request,speed:.slow) } label: { Text("ゆっくり").fixedSize(horizontal:false,vertical:true).frame(maxWidth:.infinity,minHeight:44) }
            .accessibilityLabel("少しゆっくり聞く")
        Button { audio.stop() } label: { Text("停止").frame(maxWidth:.infinity,minHeight:44) }.disabled(!audio.isPlaying)
    }
    private var completion: some View {
        VStack(alignment: .leading, spacing: 24) {
            Text("完了").font(.largeTitle.weight(.semibold)).accessibilityAddTraits(.isHeader)
            Text(model.lesson.title).font(.title2)
            Text("\(model.correctCount) / \(model.quizCount) 正解").font(.title3).monospacedDigit()
            Text("学習記録を保存しました。いつでも読み返せます。").foregroundStyle(.secondary)
            Button("もう一度") { audio.stop(); Task { await model.open(restart: true) } }
                .buttonStyle(.bordered).controlSize(.large).disabled(model.busy)
        }
    }
    private var bottomAction: some View {
        VStack(spacing: 0) {
            Divider()
            if model.completed {
                Button {
                    audio.stop()
                    if hasNext { onNext() } else { dismiss() }
                } label: {
                    Text(hasNext ? nextTitle : "学習一覧へ").frame(maxWidth: .infinity, minHeight: 28)
                }.buttonStyle(.borderedProminent).controlSize(.large)
                    .frame(maxWidth: 600).padding(16).disabled(model.busy)
            } else if let step = model.step {
                let answered = model.currentResult != nil
                Button { audio.stop(); Task { await model.act(expectedID:step.id, expectedAnswered:answered) } } label: {
                    Text(model.actionTitle).frame(maxWidth: .infinity, minHeight: 28)
                }.buttonStyle(.borderedProminent).controlSize(.large)
                    .frame(maxWidth: 600).padding(16).disabled(!model.canAct)
            }
        }.frame(maxWidth: .infinity).background(Color(uiColor: .systemBackground))
    }
}
