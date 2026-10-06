"""The Colab notebook is how people without a GPU try the project, and it
embeds the package and the dependency versions: these tests keep it in step
with the repository."""

import base64
import importlib.util
import io
import re
import tarfile
import tomllib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("build_nb", ROOT / "notebooks/build_h1_notebook.py")
build_nb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(build_nb)


@pytest.fixture(scope="module")
def notebook() -> dict:
    return build_nb.build()


def sources(notebook: dict, cell_type: str = "code") -> list[str]:
    return ["".join(c["source"]) for c in notebook["cells"] if c["cell_type"] == cell_type]


def test_committed_notebook_is_up_to_date(notebook):
    committed = build_nb.NOTEBOOK.read_text(encoding="utf-8")
    assert committed == build_nb.render(notebook), (
        "notebooks/h1_diarization_check.ipynb is stale: "
        "run `poetry run python notebooks/build_h1_notebook.py`"
    )


def test_embedded_package_is_the_repository_package(notebook):
    cell = next(s for s in sources(notebook) if "PACKAGE = (" in s)
    b64 = "".join(re.findall(r'^\s*"([A-Za-z0-9+/=]+)"\s*$', cell, re.M))
    with tarfile.open(fileobj=io.BytesIO(base64.b64decode(b64)), mode="r:gz") as tar:
        embedded = {m.name: tar.extractfile(m).read() for m in tar.getmembers()}

    expected = {
        p.relative_to(ROOT).as_posix(): p.read_bytes()
        for p in (ROOT / "startup_interviews_rag").rglob("*.py")
        if "__pycache__" not in p.parts
    }
    assert embedded == expected


def test_h1_script_is_embedded_verbatim(notebook):
    cell = next(s for s in sources(notebook) if s.startswith("%%writefile h1_check.py"))
    script = (ROOT / "notebooks/h1_check.py").read_text(encoding="utf-8")
    # Notebook cells drop the trailing newline
    assert cell == "%%writefile h1_check.py\n" + script.rstrip("\n")


def test_installs_into_colab_python_with_whisperx_from_the_lock(notebook):
    # Colab's own Python, like any WhisperX demo: a separate venv inherits the
    # kernel's environment (MPLBACKEND...) without its packages and breaks.
    code = "\n".join(sources(notebook))
    assert ".venv" not in code and "uv " not in code

    lock = tomllib.loads((ROOT / "poetry.lock").read_text(encoding="utf-8"))
    whisperx = next(p["version"] for p in lock["package"] if p["name"] == "whisperx")
    install = next(line for line in code.splitlines() if "pip install" in line)
    assert f"whisperx=={whisperx}" in install
    # An old yt-dlp is what breaks YouTube downloads: always the latest.
    assert re.search(r"\byt-dlp(\s|$)", install)


def test_nltk_punkt_tab_is_provisioned_before_running(notebook):
    # whisperx fetches punkt_tab at alignment time, and nltk refuses fetches
    # through a proxy (Colab has one): the notebook must ship it beforehand.
    code = "\n".join(sources(notebook))
    assert "punkt_tab.zip" in code
    assert 'os.environ["NLTK_DATA"]' in code
