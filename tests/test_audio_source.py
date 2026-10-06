import sys
from types import SimpleNamespace

import pytest

from startup_interviews_rag.application.ports.audio import AudioError
from startup_interviews_rag.infrastructure.audio import ytdlp_audio_source
from startup_interviews_rag.infrastructure.audio.ytdlp_audio_source import YtDlpAudioSource

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


def test_failed_download_reports_the_last_error(tmp_path, monkeypatch):
    class FailingYoutubeDL:
        def __init__(self, opts):
            self.fmt = opts["format"]

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def extract_info(self, url, download):
            raise RuntimeError(f"HTTP Error 403 with {self.fmt}")

    monkeypatch.setitem(sys.modules, "yt_dlp", SimpleNamespace(YoutubeDL=FailingYoutubeDL))

    with pytest.raises(AudioError, match="Last error: HTTP Error 403 with 18/best"):
        YtDlpAudioSource(tmp_path)._download(URL)
