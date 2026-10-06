import sys
import types

from startup_interviews_rag.infrastructure.metadata.ytdlp_metadata_source import YtDlpMetadataSource

INFO = {
    "id": "yOLw6ncCJwY",
    "title": "Alquiler de barcos",
    "upload_date": "20200107",
    "formats": ["dropped"],
}


class FakeYoutubeDL:
    opts: dict = {}

    def __init__(self, opts):
        FakeYoutubeDL.opts = opts

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def extract_info(self, url, download):
        assert download is False
        return INFO

    def sanitize_info(self, info):
        return info


def test_fetch_keeps_the_useful_fields_without_downloading(monkeypatch):
    monkeypatch.setitem(sys.modules, "yt_dlp", types.SimpleNamespace(YoutubeDL=FakeYoutubeDL))
    meta = YtDlpMetadataSource().fetch("https://www.youtube.com/watch?v=yOLw6ncCJwY")

    assert FakeYoutubeDL.opts["skip_download"] is True
    assert (meta.id, meta.title, meta.published) == (
        "yOLw6ncCJwY",
        "Alquiler de barcos",
        "2020-01-07",
    )
