from video_rag.infrastructure.audio import ytdlp_audio_source
from video_rag.infrastructure.audio.ytdlp_audio_source import YtDlpAudioSource

URL = "https://www.youtube.com/watch?v=yOLw6ncCJwY"


def test_existing_wav_is_reused_without_downloading(tmp_path, monkeypatch):
    monkeypatch.setattr(ytdlp_audio_source, "require_ffmpeg", lambda: None)
    wav = tmp_path / "yOLw6ncCJwY.wav"
    wav.write_bytes(b"RIFF")
    source = YtDlpAudioSource(tmp_path)
    monkeypatch.setattr(source, "_download", lambda url: (_ for _ in ()).throw(AssertionError))

    assert source.fetch(URL) == wav


def test_missing_wav_is_downloaded(tmp_path, monkeypatch):
    monkeypatch.setattr(ytdlp_audio_source, "require_ffmpeg", lambda: None)
    source = YtDlpAudioSource(tmp_path)
    monkeypatch.setattr(source, "_download", lambda url: tmp_path / "downloaded.wav")

    assert source.fetch(URL) == tmp_path / "downloaded.wav"
