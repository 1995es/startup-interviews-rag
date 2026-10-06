from startup_interviews_rag.application.ports.metadata import VideoMetadataSource
from startup_interviews_rag.domain.video import VideoMeta


class YtDlpMetadataSource(VideoMetadataSource):
    """Equivalent to `yt-dlp --dump-json`, keeping only the useful fields."""

    def fetch(self, url: str) -> VideoMeta:
        import yt_dlp

        opts = {"quiet": True, "no_warnings": True, "skip_download": True}
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.sanitize_info(ydl.extract_info(url, download=False))
        return VideoMeta.from_info(info)
