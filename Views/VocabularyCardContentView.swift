import SwiftUI

/// Shared production vocabulary presentation for passes and spaced review.
@MainActor
struct VocabularyCardContentView: View {
    let card: VocabularyCard
    let revealed: Bool
    @EnvironmentObject private var audio: KoreanAudioService
    @ScaledMetric(relativeTo: .largeTitle) private var wordSize: CGFloat = 60
    @AccessibilityFocusState private var wordFocused: Bool
    var body: some View {
        VStack(alignment: .leading, spacing: 24) {
            VStack(spacing: 12) {
                Text(card.headword).font(.system(size: wordSize, weight: .medium))
                    .multilineTextAlignment(.center).fixedSize(horizontal: false, vertical: true)
                    .accessibilityFocused($wordFocused).accessibilityAddTraits(.isHeader)
                Text(card.partOfSpeech).font(.subheadline).foregroundStyle(.secondary)
                audioControls(card.audio, label: "単語を聞く")
            }.frame(maxWidth: .infinity).padding(.vertical, 20)
            if revealed {
                if let first = card.meanings.first { meaning(first) }
                if card.meanings.count > 1 {
                    DisclosureGroup("ほかの意味") {
                        VStack(alignment: .leading, spacing: 20) {
                            ForEach(Array(card.meanings.dropFirst())) { meaning($0) }
                        }.padding(.top, 12)
                    }
                }
                if let note = card.notes.first {
                    VStack(alignment: .leading, spacing: 8) {
                        Text("ポイント").font(.subheadline.weight(.semibold))
                        Text(note.text).font(.subheadline).foregroundStyle(.secondary)
                    }
                }
            } else {
                Text("意味を思い出してから、確認しましょう。")
                    .foregroundStyle(.secondary).frame(maxWidth: .infinity).multilineTextAlignment(.center)
            }
        }.onAppear { wordFocused = true }
    }
    @ViewBuilder private func meaning(_ meaning: VocabularyMeaning) -> some View {
        Text(meaning.text).font(.title2.weight(.medium))
        if let usage = meaning.usage { Text(usage).font(.subheadline).foregroundStyle(.secondary) }
        if let nuance = meaning.nuance { Text(nuance).font(.subheadline).foregroundStyle(.secondary) }
        if let example = meaning.example {
            VStack(alignment: .leading, spacing: 8) {
                Text(example.korean).font(.title3).fixedSize(horizontal: false, vertical: true)
                Text(example.japanese).foregroundStyle(.secondary)
                if let request = meaning.exampleAudio { audioControls(request, label: "例文を聞く") }
            }
        }
    }
    @ViewBuilder private func audioControls(_ request: LearningAudio, label: String) -> some View {
        if audio.availability(for: request) == .available {
            LearningAudioControlRow { audioButtons(request, label:label) }
            Text(request.source == .systemTTS ? "システム音声" : "確認用の録音音声").font(.caption).foregroundStyle(.secondary)
        } else if let message = audio.availability(for: request).message {
            Text(message).font(.footnote).foregroundStyle(.secondary)
        }
        if let message = audio.message { Text(message).font(.footnote).foregroundStyle(.secondary) }
    }
    @ViewBuilder private func audioButtons(_ request: LearningAudio, label: String) -> some View {
        Button { audio.play(request, speed: .normal) } label: {
            Label(label, systemImage: "speaker.wave.2").fixedSize(horizontal:false,vertical:true).frame(maxWidth:.infinity,minHeight:44)
        }.accessibilityLabel(label + "。通常の速さ")
        Button { audio.play(request,speed:.slow) } label: { Text("ゆっくり").fixedSize(horizontal:false,vertical:true).frame(maxWidth:.infinity,minHeight:44) }
            .accessibilityLabel(label + "。ゆっくり")
        Button { audio.stop() } label: { Text("停止").frame(maxWidth:.infinity,minHeight:44) }.disabled(!audio.isPlaying)
    }
}
