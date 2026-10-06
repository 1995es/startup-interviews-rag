import logging
import shutil
from pathlib import Path

from video_rag.application.ports.audio import AudioError, AudioSource
from video_rag.domain.video import video_id

log = logging.getLogger(__name__)

# YouTube answers 403 on some format strings depending on the client, so a
# few of them are tried before giving up. The original notebook's
# `bestaudio/best` alone gave 403: do not simplify this list. It does not
# save an outdated yt-dlp, though: that is fixed by upgrading yt-dlp.
FORMATS = ("bestaudio/best", "251/140/bestaudio", "18/best")


def require_ffmpeg() -> None:
    """yt-dlp and whisperx.load_audio both shell out to the ffmpeg CLI."""
    if shutil.which("ffmpeg") is None:
        raise AudioError(
            "'ffmpeg' is not on the PATH.\n"
            "  winget install Gyan.FFmpeg   (Windows)\n"
            "  brew install ffmpeg          (macOS)\n"
            "  sudo apt install ffmpeg      (Linux)"
        )


class YtDlpAudioSource(AudioSource):
    """Downloads the audio with yt-dlp as a 16 kHz mono wav named
    `<audio_dir>/<id>.wav`. If that file already exists it is reused without
    touching the network."""

    def __init__(self, audio_dir: Path) -> None:
        self._audio_dir = audio_dir

    def fetch(self, url: str) -> Path:
        require_ffmpeg()
        vid = video_id(url)
        cached = self._audio_dir / f"{vid}.wav" if vid else None
        if cached is not None and cached.exists():
            log.info(f"Reusing audio {cached}")
            return cached
        return self._download(url)

    def _download(self, url: str) -> Path:
        import yt_dlp

        self._audio_dir.mkdir(parents=True, exist_ok=True)
        opts = {
            "outtmpl": str(self._audio_dir / "%(id)s.%(ext)s"),
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "wav"}],
            "postprocessor_args": ["-ar", "16000", "-ac", "1"],
            "quiet": True,
            "no_warnings": True,
            "noprogress": True,
        }
        for fmt in FORMATS:
            try:
                with yt_dlp.YoutubeDL({**opts, "format": fmt}) as ydl:
                    info = ydl.extract_info(url, download=True)
                path = self._audio_dir / f"{info['id']}.wav"
                if path.exists():
                    return path
            except Exception as exc:
                log.info(f"format='{fmt}' failed ({exc}). Retrying ...")
        raise AudioError("could not download the audio.")
