import AVFoundation
import Combine
import CryptoKit
import Foundation

@MainActor
protocol LearningAudioPlaying: AnyObject {
    func availability(for audio: LearningAudio) -> AudioAvailability
    func play(_ audio: LearningAudio, speed: AudioSpeed) -> Bool
    func stop()
}
@MainActor
protocol AudioPlaybackBackend: AnyObject {
    var hasKoreanVoice: Bool { get }
    func speak(_ text: String, rate: Float, finished: @escaping @MainActor (Bool) -> Void) throws -> Bool
    func playFile(_ url: URL, rate: Float, finished: @escaping @MainActor (Bool) -> Void) throws -> Bool
    func stop()
}
protocol RecordingResolving {
    func url(for asset: RecordingAsset) -> URL?
}
struct BundleRecordingResolver: RecordingResolving {
    let root: URL
    init(bundle: Bundle = .main) { root = bundle.bundleURL }
    init(root: URL) { self.root = root }
    func url(for asset: RecordingAsset) -> URL? {
        let path = asset.relativePath
        guard path.hasPrefix("Audio/"), !path.contains(".."), !path.contains("\\"),
              !path.hasPrefix("/"), asset.sha256.count == 64 else { return nil }
        let url = root.appendingPathComponent(path).resolvingSymlinksInPath()
        let base = root.resolvingSymlinksInPath().path + "/"
        guard url.path.hasPrefix(base), ["m4a", "wav", "mp3", "caf"].contains(url.pathExtension.lowercased()),
              let size = try? url.resourceValues(forKeys: [.fileSizeKey]).fileSize, size <= 10_000_000,
              let bytes = try? Data(contentsOf: url) else { return nil }
        let hash = SHA256.hash(data: bytes).map { String(format: "%02x", $0) }.joined()
        return hash == asset.sha256.lowercased() ? url : nil
    }
}

@MainActor
final class KoreanAudioService: ObservableObject, LearningAudioPlaying {
    @Published private(set) var completedPlaybackCount = 0
    @Published private(set) var isPlaying = false
    @Published private(set) var speed: AudioSpeed = .normal
    @Published private(set) var message: String?
    private let backend: any AudioPlaybackBackend
    private let recordings: any RecordingResolving
    private var generation = UUID()
    init(backend: any AudioPlaybackBackend, recordings: any RecordingResolving) {
        self.backend = backend; self.recordings = recordings
    }
    convenience init() { self.init(backend: SystemAudioBackend(), recordings: BundleRecordingResolver()) }
    func availability(for audio: LearningAudio) -> AudioAvailability {
        if audio.source == .verifiedRecording {
            guard let asset = audio.asset, recordings.url(for: asset) != nil else { return .recordingMissing }
            return .available
        }
        guard AudioPolicy.permitsTTS(audio) else { return .disallowed }
        return backend.hasKoreanVoice ? .available : .koreanVoiceMissing
    }
    @discardableResult func play(_ audio: LearningAudio, speed: AudioSpeed) -> Bool {
        stop()
        let availability = availability(for: audio)
        guard availability == .available else { message = availability.message; return false }
        let request = generation
        self.speed = speed; message = nil; isPlaying = true
        let finished: @MainActor (Bool) -> Void = { [weak self] success in
            guard let self = self, self.generation == request else { return }
            self.isPlaying = false
            if success { self.completedPlaybackCount += 1 }
            if !success { self.message = "音声を再生できませんでした。もう一度お試しください。" }
        }
        do {
            let started: Bool
            switch audio.source {
            case .systemTTS:
                guard let text = audio.text else { isPlaying = false; return false }
                started = try backend.speak(text, rate: AudioPolicy.speechRate(speed), finished: finished)
            case .verifiedRecording:
                guard let asset = audio.asset, let url = recordings.url(for: asset) else { isPlaying = false; message = AudioAvailability.recordingMissing.message; return false }
                started = try backend.playFile(url, rate: AudioPolicy.recordingRate(speed), finished: finished)
            }
            if !started { finished(false) }
            return started
        } catch { finished(false); return false }
    }
    func stop() {
        generation = UUID(); backend.stop(); isPlaying = false; message = nil
    }
}

@MainActor
final class SystemAudioBackend: NSObject, AudioPlaybackBackend, AVSpeechSynthesizerDelegate, AVAudioPlayerDelegate {
    private let synthesizer = AVSpeechSynthesizer()
    private var player: AVAudioPlayer?
    private var activeSpeech: ObjectIdentifier?
    private var activePlayer: ObjectIdentifier?
    private var finished: (@MainActor (Bool) -> Void)?
    private var observers: [NSObjectProtocol] = []
    private var sessionActive = false
    var hasKoreanVoice: Bool { koreanVoice != nil }
    private var koreanVoice: AVSpeechSynthesisVoice? {
        guard let voice = AVSpeechSynthesisVoice(language: "ko-KR"), voice.language.hasPrefix("ko") else { return nil }
        return voice
    }
    override init() {
        super.init(); synthesizer.delegate = self
        observers.append(NotificationCenter.default.addObserver(forName: AVAudioSession.interruptionNotification, object: nil, queue: .main) { [weak self] notice in
            guard let value = notice.userInfo?[AVAudioSessionInterruptionTypeKey] as? UInt,
                  value == AVAudioSession.InterruptionType.began.rawValue else { return }
            Task { @MainActor [weak self] in self?.interrupted() }
        })
        observers.append(NotificationCenter.default.addObserver(forName: AVAudioSession.routeChangeNotification, object: nil, queue: .main) { [weak self] notice in
            guard let value = notice.userInfo?[AVAudioSessionRouteChangeReasonKey] as? UInt,
                  value == AVAudioSession.RouteChangeReason.oldDeviceUnavailable.rawValue else { return }
            Task { @MainActor [weak self] in self?.interrupted() }
        })
    }
    deinit { for observer in observers { NotificationCenter.default.removeObserver(observer) } }
    private func activate() throws {
        let session = AVAudioSession.sharedInstance()
        try session.setCategory(.playback, mode: .spokenAudio, options: [.duckOthers])
        try session.setActive(true); sessionActive = true
    }
    private func deactivate() {
        if sessionActive { try? AVAudioSession.sharedInstance().setActive(false, options: .notifyOthersOnDeactivation) }
        sessionActive = false
    }
    func speak(_ text: String, rate: Float, finished: @escaping @MainActor (Bool) -> Void) throws -> Bool {
        guard let voice = koreanVoice else { return false }
        try activate()
        let utterance = AVSpeechUtterance(string: text)
        utterance.voice = voice; utterance.rate = min(max(rate, AVSpeechUtteranceMinimumSpeechRate), AVSpeechUtteranceMaximumSpeechRate)
        self.finished = finished; activeSpeech = ObjectIdentifier(utterance)
        synthesizer.speak(utterance)
        return true
    }
    func playFile(_ url: URL, rate: Float, finished: @escaping @MainActor (Bool) -> Void) throws -> Bool {
        let audio = try AVAudioPlayer(contentsOf: url)
        audio.enableRate = true; audio.rate = rate; audio.delegate = self
        try activate()
        player = audio; activePlayer = ObjectIdentifier(audio); self.finished = finished
        if !audio.play() { stop(); return false }
        return true
    }
    func stop() {
        activeSpeech = nil; activePlayer = nil; finished = nil
        synthesizer.stopSpeaking(at: .immediate); player?.stop(); player = nil; deactivate()
    }
    private func interrupted() {
        let callback = finished
        stop(); callback?(false)
    }
    private func complete(speech: ObjectIdentifier? = nil, audio: ObjectIdentifier? = nil, success: Bool) {
        guard (speech != nil && speech == activeSpeech) || (audio != nil && audio == activePlayer) else { return }
        let callback = finished
        activeSpeech = nil; activePlayer = nil; finished = nil; player = nil; deactivate(); callback?(success)
    }
    nonisolated func speechSynthesizer(_ synthesizer: AVSpeechSynthesizer, didFinish utterance: AVSpeechUtterance) {
        let id = ObjectIdentifier(utterance)
        Task { @MainActor [weak self] in self?.complete(speech: id, success: true) }
    }
    nonisolated func speechSynthesizer(_ synthesizer: AVSpeechSynthesizer, didCancel utterance: AVSpeechUtterance) {
        let id = ObjectIdentifier(utterance)
        Task { @MainActor [weak self] in self?.complete(speech: id, success: false) }
    }
    nonisolated func audioPlayerDidFinishPlaying(_ player: AVAudioPlayer, successfully flag: Bool) {
        let id = ObjectIdentifier(player)
        Task { @MainActor [weak self] in self?.complete(audio: id, success: flag) }
    }
    nonisolated func audioPlayerDecodeErrorDidOccur(_ player: AVAudioPlayer, error: Error?) {
        let id = ObjectIdentifier(player)
        Task { @MainActor [weak self] in self?.complete(audio: id, success: false) }
    }
}
