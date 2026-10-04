# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Qué es esto

Pipeline local de **vídeo → texto** con WhisperX, más la ingesta con LLM para
un RAG (`docs/ingesta-llm.md`). Es un paquete, `video_rag/`, con
**arquitectura hexagonal (puertos y adaptadores)**. Más adelante tendrá una
capa de API sobre el RAG.

```
video_rag/
├── domain/          lógica pura: sin E/S ni dependencias de terceros
├── application/
│   ├── ports/       clases abstractas que necesitan los casos de uso
│   └── use_cases/   TranscribeVideo, RenderScript, PrepareLLMInput, SegmentEpisode
├── infrastructure/  adaptadores de salida: WhisperX, yt-dlp, Anthropic, OpenRouter, JSON
├── interfaces/
│   └── cli/         adaptadores de entrada (más adelante, api/)
├── config.py        Settings: entorno + .env
└── container.py     composition root: el único sitio que elige adaptadores
```

Regla de dependencias: `interfaces` → `application` → `domain`, e
`infrastructure` implementa los puertos de `application`. Ni `domain` ni
`application` importan `infrastructure`, `interfaces`, `config` ni SDKs de
terceros. Las interfaces piden el caso de uso a `container` y nunca importan
`infrastructure` por su cuenta. La inyección es por constructor, a mano y sin
framework.

Los cuatro scripts de `video_rag/interfaces/cli/`. No hay comandos instalados
(`[project.scripts]`): se lanzan por ruta, `poetry run python
video_rag/interfaces/cli/<script>.py`. Los imports `video_rag.*` resuelven
porque `poetry install` instala el propio paquete en el venv en modo editable.

- `transcribe.py`: URL o fichero local → wav 16 kHz
  mono → transcripción → alineación por palabra → diarización → JSON
  `[{text, speaker, start, end}]` agrupado por turnos. La diarización se
  activa sola si hay `HF_TOKEN` (entorno o `.env`) y GPU/CPU se autodetectan.
- `script.py`: ese JSON plano → guion Markdown tipo
  entrevista, una fila por intervención. **Solo maqueta**: no toca los turnos.
- `prepare.py`: paso 1 de `docs/ingesta-llm.md`.
  URL → metadatos (`meta/<id>.json`) + transcripción → `llm_input/<id>.txt`
  con turnos numerados (`t020`, y `t020.s1`… en los de más de 150 palabras) y
  `llm_input/<id>.json` con el texto original de cada ID. La transcripción va
  en un **proceso hijo** (`SubprocessTranscriber`); si ya existen
  `meta/<id>.json` y `output/<id>.json`, los reutiliza sin red ni WhisperX.
- `segment.py`: paso 2. `llm_input/<id>.txt` → una
  llamada al LLM con salida con esquema JSON → `segments/<id>.json` (speakers,
  units, glossary, episode_summary). La caché va por `model` +
  `PROMPT_VERSION` (`domain/segmentation.py`). Las `raw_tags` son libres, sin
  taxonomía cerrada (ver el paso 9 del doc).

### LLM: puerto `LLMProvider`

`application/ports/llm.py` define `LLMProvider.generate_structured(StructuredRequest)
-> StructuredResponse`. Ningún caso de uso conoce el SDK: los adaptadores
traducen sus excepciones a `LLMError`. Hay dos implementaciones en
`infrastructure/llm/`:

- `AnthropicProvider` (por defecto, `claude-opus-5-5`): pensamiento
  adaptativo, `effort` y `fallbacks: "default"`; el modelo que respondió de
  verdad se guarda en `served_by`. Opus 5.5 rechaza `temperature`, por eso no
  se fija a 0 como dice el doc. Su `effort` por defecto es `medium`, por eso
  siempre se envía.
- `OpenRouterProvider` (`anthropic/claude-opus-5-5`): SDK `openai` contra
  `https://openrouter.ai/api/v1`, con `response_format` json_schema y
  `reasoning.effort`. El uso de tokens se normaliza a la semántica de
  Anthropic: `input_tokens` no incluye los de caché.

El proveedor se elige con `LLM_PROVIDER` en `.env` (`anthropic` |
`openrouter`) o con `--provider`. El modelo, con `LLM_MODEL` o `--model`. Las
claves se leen de `ANTHROPIC_API_KEY` y `OPENROUTER_API_KEY`. Como los ids de
modelo difieren entre proveedores, cambiar de proveedor vuelve a segmentar.
Para añadir un proveedor: un adaptador en `infrastructure/llm/`, una rama en
`container.build_llm()` y su nombre en `LLM_PROVIDERS`.

`guiones/` es la única carpeta de salida que **sí** se versiona: los diez
guiones de vídeos de Itnig (`.md` anotado + `.json` plano) más su índice. Se
regenera con el pipeline normal; `audio/`, `output/`, `meta/`, `llm_input/` y
`segments/` siguen ignorados.

Las dependencias se gestionan con **Poetry** (`pyproject.toml` +
`poetry.lock`; no hay `requirements.txt`). `poetry.toml` fija el venv dentro
del proyecto, en `.venv/`. Todo se ejecuta con `poetry run`. Un script
nuevo es un módulo en `interfaces/cli/` con su `main()` y su
`if __name__ == "__main__"`. Para añadir una
dependencia, `poetry add <paquete>`, nunca `pip install`. Python 3.11–3.12:
`ctranslate2 4.5.0` no tiene ruedas para 3.13.

## Comandos

```bash
# URL -> output/<id>.json con {text, speaker, start, end}
poetry run python video_rag/interfaces/cli/transcribe.py "https://www.youtube.com/watch?v=..." --language es --min-speakers 2

# Iteracion rapida sobre cambios de codigo: modelo pequeno + audio corto
poetry run python video_rag/interfaces/cli/transcribe.py "audio/foo.wav" --model tiny --language es -o output_test/foo.json

# JSON -> guion Markdown
poetry run python video_rag/interfaces/cli/script.py output/<id>.json --timestamps

# Ingesta con LLM (pasos 1 y 2)
poetry run python video_rag/interfaces/cli/prepare.py "https://www.youtube.com/watch?v=..." --language es --min-speakers 2
poetry run python video_rag/interfaces/cli/segment.py <id> [--provider openrouter] [--model ...] [--force]

# Tests (dominio, casos de uso con fakes, adaptadores LLM con clientes stub)
poetry run pytest

# Formato y lint (config en [tool.ruff] de pyproject.toml)
poetry run ruff format .
poetry run ruff check . --fix
```

Reejecutar sobre un `.wav` ya descargado en `audio/` ahorra la descarga; el
adaptador detecta que la entrada ya es wav y no vuelve a pasar por ffmpeg.

Los tests no tocan red ni modelos: `tests/fakes.py` tiene adaptadores en
memoria de los puertos, y los adaptadores LLM se prueban con clientes stub
inyectados por el constructor.

## Restricciones del entorno (comprobadas, no cambiar a la ligera)

Estas versiones están fijadas en `pyproject.toml` porque las alternativas
**rompen en este equipo** (Win 11, RTX 4070). Antes de "actualizar
dependencias", verificar con una carga de modelo real:

- `torch 2.8.0+cu126`. La 2.13 falla al importar (`WinError 1114` cargando
  `c10.dll`), también en la instalación de Anaconda del sistema.
- El sufijo `+cu126` es obligatorio en el pin: con `torch==2.8.0` pip da por
  buena la rueda `+cpu` y `torch.cuda.is_available()` pasa a `False`. En
  `pyproject.toml` va como restricción múltiple: `+cu126` desde la fuente
  `pytorch-cu126` en Windows, y la `2.8.0` de PyPI en el resto.
- Los *markers* usan `platform_system == 'Windows'`, no `sys_platform ==
  'win32'`: torch declara sus `nvidia-*` con `platform_system == "Linux"` y
  Poetry no sabe que `sys_platform` y `platform_system` se excluyen, así que
  con `sys_platform` el lock falla por un conflicto de versiones de cuDNN.
- `ctranslate2 4.5.0`. La 4.8.1 (la que arrastra `faster-whisper`) provoca
  *segfault* (exit 139) al cargar cualquier modelo, incluso en CPU.
- `nvidia-cublas-cu12` / `nvidia-cudnn-cu12` están instalados porque
  CTranslate2 necesita esas DLL en Windows.

Al depurar caídas: un pipe (`| tail`) se traga el código de salida y la salida
bufferizada de un proceso que muere de golpe. Usar `PYTHONUNBUFFERED=1` y
`${PIPESTATUS[0]}` — así se vio que el "exit 0" silencioso era en realidad un
segfault de CTranslate2.

## Detalles de diseño que no se ven en una lectura rápida

**`_register_cuda_dlls()` se ejecuta al importar
`infrastructure/transcription/whisperx_recognizer.py`, antes que whisperx.**
Registra `torch/lib` y `site-packages/nvidia/*/bin` como directorios de DLL.
Sin eso CTranslate2 no encuentra cuDNN/cuBLAS en Windows. No mover esa llamada
por debajo de los imports de whisperx, que por eso mismo son locales, dentro
de `recognize()`. Por la misma razón, `container.py` importa los adaptadores
pesados (WhisperX, los SDK de LLM) dentro de cada factoría y no arriba del
módulo.

**Los turnos de hablante se cortan por palabra, no por segmento.** Un segmento
de Whisper dura ~20 s y suele contener pregunta y respuesta, así que agrupar
por el hablante del segmento destruye el diálogo (643 turnos falsos vs. 547
reales en el vídeo de ejemplo). `build_turns()` (`domain/turns.py`)
reconstruye los turnos desde el hablante de cada palabra y aplica dos
correcciones encadenadas: `smooth_runs()` absorbe las rachas de menos de `--min-words` palabras (la
diarización salta de hablante en palabras sueltas) y `snap_to_sentences()`
desplaza el corte al final de frase más cercano (±3 palabras) para no partir
oraciones. Si el JSON no trae timings por palabra, cae a una fila por segmento.

**La descarga de YouTube reintenta con varias cadenas de formato**
(`bestaudio/best` → `251/140/bestaudio` → `18/best`, en
`infrastructure/audio/ytdlp_audio_source.py`). El `bestaudio/best` del
notebook original daba 403 en YouTube; no simplificar ese bucle. Ese bucle
**no** salva un yt-dlp desfasado: con 2026.7.4 YouTube devolvia 403 en
cualquier descarga completa, con las tres cadenas y con todos los
`player_client` (`tv_embedded`, `android`, `ios`…). Sintoma caracteristico:
`--list-formats` funciona y hasta un `--test` de 10 kB pasa, pero la descarga
entera muere con 403. Se arregla actualizando yt-dlp, no tocando el codigo.

**Degradación en cascada**: si falla la carga del modelo en GPU se reintenta en
CPU/int8; si no hay `HF_TOKEN` se avisa y se continúa sin diarizar. El
pipeline no debería abortar por falta de diarización.

## Convenciones

- **Todo el código se escribe en inglés. Nunca generar código en español**:
  identificadores, comentarios, docstrings, mensajes de `print`/`log`,
  textos de `--help`, errores y literales fijos que escribe el script (p. ej.
  las etiquetas de una cabecera). Vale para ficheros nuevos y para cualquier
  línea que se añada o modifique en los existentes.
- El español queda para la documentación (`CLAUDE.md`, `docs/`, README) y para
  los datos: el contenido transcrito, los valores de datos del prompt de
  segmentación (`UNIT_TYPES`, `ROLES`) y el Markdown de `guiones/`. Las
  etiquetas fijas que añade `script.py` ("turns", "speakers", "Time"…)
  están en inglés; los `.md` ya versionados de `guiones/` conservan las
  antiguas en castellano hasta que se regeneren.
- Los `print`/`log` van sin caracteres no ASCII, por la consola de Windows con
  cp1252.
- El código pasa `ruff format` y `ruff check` (líneas de 100 columnas; reglas
  E, W, F, I, B, UP, SIM). Ejecutarlos antes de dar un cambio por terminado.
- Los ficheros generados (`audio/`, `output/`) no son fuente: se pueden
  regenerar y no hay que editarlos a mano.
