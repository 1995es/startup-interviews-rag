# Vídeo → texto con WhisperX (local)

Transcribe un vídeo de YouTube (o un fichero local) en tu máquina, con
timestamps por palabra y separación de interlocutores, y escupe un JSON plano
listo para procesar:

```
entrada (URL de YouTube | vídeo/audio local)
   → audio wav 16 kHz mono           (yt-dlp / ffmpeg)
   → transcripción                   (Whisper large-v2 vía faster-whisper)
   → alineación de timestamps        (por palabra)
   → diarización opcional            (pyannote: quién habla y cuándo)
   → turnos                          (corte por palabra, no por segmento)
   → output/<id>.json                [{text, speaker, start, end}]
```

Encima de eso va la ingesta con LLM para un RAG
([`docs/ingesta-llm.md`](docs/ingesta-llm.md)). Hay cuatro scripts, en
[`video_rag/interfaces/cli/`](video_rag/interfaces/cli/):

| Script | Qué hace |
|---|---|
| `transcribe.py` | el pipeline de transcripción: URL o fichero → `output/<id>.json` |
| `script.py` | ese JSON → guion en Markdown, una fila por intervención |
| `prepare.py` | paso 1 de la ingesta: metadatos + transcripción → `llm_input/<id>.txt` numerado |
| `segment.py` | paso 2: una llamada al LLM por episodio → `segments/<id>.json` |

## Arquitectura

El código es un paquete, [`video_rag/`](video_rag/), con arquitectura
hexagonal (puertos y adaptadores):

```
domain/          lógica pura (turnos, numeración, guion, prompt de segmentación)
application/     casos de uso + puertos (clases abstractas) que necesitan
infrastructure/  adaptadores: WhisperX, yt-dlp, Anthropic, OpenRouter, ficheros JSON
interfaces/cli/  los cuatro scripts (más adelante, interfaces/api/)
container.py     composition root: elige los adaptadores e inyecta dependencias
```

El LLM está detrás del puerto `LLMProvider`, con dos implementaciones:
`AnthropicProvider` (por defecto) y `OpenRouterProvider`. Para cambiar de
proveedor no se toca código, basta con el `.env`:

```bash
LLM_PROVIDER=openrouter          # anthropic (por defecto) | openrouter
LLM_MODEL=anthropic/claude-opus-5-5   # opcional; por defecto, el del proveedor
ANTHROPIC_API_KEY=sk-ant-...
OPENROUTER_API_KEY=sk-or-...
```

o con `poetry run python video_rag/interfaces/cli/segment.py <id> --provider openrouter --model ...`.

## Instalación

Requisitos: Python 3.11–3.12, [Poetry](https://python-poetry.org/) 2.x y
`ffmpeg` en el PATH (`winget install Gyan.FFmpeg` / `brew install ffmpeg` /
`apt install ffmpeg`).

```bash
poetry install
cp .env.template .env   # y rellenar las claves que hagan falta
```

Crea el venv en `.venv/` e instala las dependencias fijadas en `poetry.lock`.
En Windows, `torch`/`torchaudio`/`torchvision` salen del índice CUDA 12.6 de
PyTorch (`+cu126`); en macOS y Linux, de PyPI. Sin GPU NVIDIA el pipeline detecta
que no hay CUDA y tira de CPU/int8 (bastante más lento).

Cada script se lanza por su ruta, con `poetry run python
video_rag/interfaces/cli/<script>.py`. Los tests, con
`poetry run pytest`: no usan red ni modelos.

## Uso

```bash
poetry run python video_rag/interfaces/cli/transcribe.py "https://www.youtube.com/watch?v=2vv4hHAvqnE" --language es --min-speakers 2
```

```json
[
  {
    "text": "para ver si me abren.",
    "speaker": "SPEAKER_02",
    "start": 3.284,
    "end": 4.045
  }
]
```

Acepta también rutas locales (`.mp4`, `.mkv`, `.mp3`, `.wav`…). El wav
intermedio se guarda en `audio/` y el JSON en `output/<id>.json`; volver a
lanzarlo sobre el `.wav` ya descargado ahorra la descarga y la conversión.

Opciones: `--model` (`tiny`…`large-v3`, por defecto `large-v2`), `--language`,
`--min-speakers` / `--max-speakers`, `--min-words` y `-o`. El dispositivo se
autodetecta (CUDA si la hay, y si el modelo no carga en GPU se reintenta en
CPU/int8).

### Diarización: quién habla

Se activa sola si hay un `HF_TOKEN` en el entorno o en `.env`; si no lo hay, avisa y sigue
adelante con un solo hablante. Hace falta además aceptar las condiciones de
[`pyannote/speaker-diarization-3.1`](https://huggingface.co/pyannote/speaker-diarization-3.1)
en Hugging Face con esa misma cuenta.

```bash
set HF_TOKEN=hf_xxx           # Windows (cmd)
$env:HF_TOKEN="hf_xxx"        # Windows (PowerShell)
export HF_TOKEN=hf_xxx        # macOS / Linux
```

`SPEAKER_00`, `SPEAKER_01`… son etiquetas automáticas: la diarización agrupa
voces por parecido acústico, no sabe quién es quién.

## Del JSON al guion en Markdown

```bash
poetry run python video_rag/interfaces/cli/script.py output/2vv4hHAvqnE.json --timestamps
```

```markdown
`00:01:11` **SPEAKER_02** — Más 140 de coeficiente intelectual. ¿Quién tiene más 140?

`00:01:18` **SPEAKER_01** — Y solo pueden usarlas estas personas, ¿no?
```

Con `--names SPEAKER_00=Jordi,SPEAKER_01=Bernat` se ponen nombres reales,
`--table` saca una tabla Markdown, `--title` cambia el encabezado y `-o` elige
la salida (por defecto `<id>.guion.md`).

## Por qué los turnos se cortan por palabra

Un segmento de Whisper dura ~20 s y suele contener la pregunta *y* la
respuesta, así que agrupar por el hablante del segmento se come el diálogo (643
turnos falsos frente a 547 reales en el vídeo de ejemplo). El pipeline
reconstruye los turnos desde el speaker de cada palabra y aplica dos
correcciones (en [`domain/turns.py`](video_rag/domain/turns.py)):

- **`smooth_runs`** — la diarización salta de hablante en palabras sueltas; las
  rachas de menos de `--min-words` (4 por defecto) se absorben en el turno
  vecino más largo.
- **`snap_to_sentences`** — el corte entre hablantes cae a menudo a mitad de
  frase; si hay un final de frase a ±3 palabras, el límite se mueve ahí.

## Corpus de ejemplo: 10 vídeos de Itnig

[`guiones/`](guiones/) contiene el resultado de pasar el pipeline por diez
vídeos del canal [Itnig](https://www.youtube.com/@itnig) elegidos al azar
(10,2 h de audio, 104.233 palabras): el guion en Markdown con marca de tiempo e
interlocutor y el mismo contenido en JSON plano. El índice, el criterio del
sorteo y los avisos sobre la calidad de la transcripción están en
[`guiones/README.md`](guiones/README.md).

Es la única carpeta de salida versionada: `audio/` y `output/` se regeneran.

## Versiones fijadas y por qué

Comprobado en este equipo (Windows 11, RTX 4070). Antes de "actualizar
dependencias", verificar con una carga de modelo real:

- **`torch 2.8.0+cu126`**: la 2.13 falla al importar (`WinError 1114` cargando
  `c10.dll`), también en la instalación de Anaconda del sistema.
- El sufijo **`+cu126`** es imprescindible: con `torch==2.8.0` a secas pip da
  por buena la rueda `+cpu` y `torch.cuda.is_available()` pasa a `False`.
- **`ctranslate2 4.5.0`**: la 4.8.1 que arrastra `faster-whisper` provoca un
  *segfault* (exit 139) al cargar cualquier modelo, incluso en CPU.
- **`nvidia-cublas-cu12` / `nvidia-cudnn-cu12`**: CTranslate2 necesita esas DLL
  en Windows; `_register_cuda_dlls()` las registra al arrancar, antes de
  importar whisperx.
- **`yt-dlp`** hay que mantenerlo al día: con la 2026.7.4 YouTube devolvía 403
  en cualquier descarga completa (todos los `player_client`, todas las cadenas
  de formato). Síntoma característico: `--list-formats` funciona y hasta un
  `--test` de 10 kB pasa, pero la descarga entera muere con 403.

## Licencia y contenido

El código es de este repositorio; las transcripciones de `guiones/` provienen de
vídeos de Itnig y están ahí con fines de análisis y búsqueda.
