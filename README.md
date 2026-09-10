# Video → Texto con WhisperX (local)

Versión local, en un solo script, del notebook de Colab `Demo_WhisperX.ipynb`.

```
entrada (URL de YouTube | vídeo/audio local)
   → audio wav 16 kHz mono (yt-dlp / ffmpeg)
   → transcripción (Whisper large-v2 vía faster-whisper)
   → alineación de timestamps por palabra
   → [diarización opcional: quién habla]
   → salidas .txt / .json / .srt (+ .speakers.txt)
```

## Atajo: URL → JSON en un solo comando

`youtube_to_json.py` hace el pipeline entero (descarga, transcripción,
alineación, diarización y agrupación por turnos) y escribe directamente el JSON
plano, sin pasar por `.txt`/`.srt` ni por los scripts de conversión:

```bash
.venv\Scripts\python.exe youtube_to_json.py "https://www.youtube.com/watch?v=2vv4hHAvqnE" --language es --min-speakers 2
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

Es la versión mínima del pipeline: sin opciones de más y sin tokens en el
código. La diarización se activa sola si hay `HF_TOKEN` en el entorno; si falta,
avisa y sigue sin separar hablantes. GPU/CPU se detectan solos. Opciones:
`--model`, `--language`, `--min-speakers` / `--max-speakers`, `--min-words` y
`-o`. El audio intermedio va a `audio/` y el JSON a `output/<id>.json`.

```bash
set HF_TOKEN=hf_xxx          # Windows (cmd);  PowerShell: $env:HF_TOKEN="hf_xxx"
```

Los scripts originales (`video_to_text.py`, `json_to_script.py`,
`json_to_simple.py`) siguen ahí para cuando quieras las salidas intermedias
(`.srt`, guion Markdown) o reprocesar un `.json` ya generado sin volver a
transcribir.

## Corpus de ejemplo: 10 vídeos de Itnig

`guiones/` contiene el resultado de pasar el pipeline entero por diez vídeos del
canal [Itnig](https://www.youtube.com/@itnig) elegidos al azar: el guion en
Markdown con marcas de tiempo e interlocutor, y el mismo contenido en JSON plano
`[{text, speaker, start, end}]`. El índice, el criterio del sorteo y los avisos
sobre la calidad de la transcripción están en
[`guiones/README.md`](guiones/README.md).

Los `.wav` (`audio/`) y el JSON completo de WhisperX (`output/`, ~5 MB por
vídeo) no se versionan: se regeneran con `video_to_text.py`.

## Qué cambió respecto al notebook de Colab

| Colab | Local |
|---|---|
| `from google.colab import files` + `files.download(...)` | los ficheros se escriben en `output/` |
| `from google.colab import userdata` para el `HF_TOKEN` | variable de entorno `HF_TOKEN` o `--hf-token` |
| `device = "cuda"`, `compute_type = "float16"` fijos | autodetección de GPU/CPU y *fallback* a CPU/int8 |
| solo URL de YouTube | URL **o** fichero local (`.mp4`, `.mkv`, `.mp3`, `.wav`…) |
| celdas sueltas | un único script con CLI (`video_to_text.py`) |
| — | carga de DLLs de cuDNN/cuBLAS en Windows para CTranslate2 |
| — | salidas extra: `.srt` y transcripción por turnos de hablante |

## Instalación

Requisitos: Python 3.9–3.12 y `ffmpeg` en el PATH (`winget install Gyan.FFmpeg`).

```bash
python -m venv .venv
.venv\Scripts\python.exe -m pip install torch==2.8.0+cu126 torchaudio==2.8.0+cu126 torchvision==0.23.0+cu126 --index-url https://download.pytorch.org/whl/cu126
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Sin GPU NVIDIA, instala `torch` normal (`pip install torch torchaudio`) y usa `--device cpu`.

### Versiones fijadas y por qué (comprobado en este equipo, Win 11 + RTX 4070)

- **`torch 2.8.0+cu126`**: `torch 2.13+cu126` falla al importar
  (`WinError 1114` cargando `c10.dll`), tanto en un venv limpio como en la
  instalación de Anaconda. 2.7.1 y 2.8.0 funcionan; whisperx 3.8.6 pide 2.8.0.
- El sufijo **`+cu126`** es imprescindible: con `torch==2.8.0` a secas pip
  considera satisfecha la rueda `2.8.0+cpu` y te quedas sin GPU.
- **`ctranslate2 4.5.0`**: la 4.8.1 que instala `faster-whisper` provoca un
  *segfault* (exit 139) al cargar cualquier modelo, incluso en CPU.
- **`nvidia-cublas-cu12` / `nvidia-cudnn-cu12`**: CTranslate2 necesita
  cuDNN 9 y cuBLAS 12 en el PATH; el script registra esas carpetas
  automáticamente al arrancar (`_register_cuda_dlls`).

## Uso

```bash
.venv\Scripts\python.exe video_to_text.py "https://www.youtube.com/watch?v=2vv4hHAvqnE" --language es
```

```bash
.venv\Scripts\python.exe video_to_text.py "C:/ruta/mi_video.mp4" --model large-v2 --language es
```

Opciones principales:

- `--model` `tiny|base|small|medium|large-v2|large-v3` (por defecto `large-v2`)
- `--language es` (si se omite, Whisper detecta el idioma)
- `--device auto|cuda|cpu`, `--compute-type float16|int8|float32`, `--batch-size 16`
- `--no-align` para saltar la alineación por palabra
- `--diarize --min-speakers 2 [--max-speakers N]` → necesita `HF_TOKEN` y haber
  aceptado las condiciones de `pyannote/speaker-diarization-3.1` en Hugging Face

Salidas en `output/`: `<id>.txt`, `<id>.json` (timestamps por palabra),
`<id>.srt` y, con diarización, `<id>.speakers.txt`.

## Del JSON al guion en Markdown

`json_to_script.py` convierte el `.json` en un guion tipo entrevista de
periódico, una fila por intervención:

```bash
.venv\Scripts\python.exe json_to_script.py output/2vv4hHAvqnE.json --timestamps
```

```markdown
`00:01:11` **SPEAKER_02** — Más 140 de coeficiente intelectual. ¿Quién tiene más 140?

`00:01:18` **SPEAKER_01** — Y solo pueden usarlas estas personas, ¿no?
```

- Corta los turnos **por palabra**, no por segmento: un segmento de Whisper
  suele contener pregunta y respuesta, así que cortar por segmento se come el
  diálogo (643 → 547 intervenciones bien separadas en el vídeo de ejemplo).
- `--min-words 4`: la diarización salta de hablante en palabras sueltas; las
  rachas más cortas se absorben en el turno vecino.
- Los cortes se ajustan al final de frase más cercano (±3 palabras) para no
  partir oraciones a la mitad.
- `--names SPEAKER_00=Jordi,SPEAKER_01=Bernat` para poner nombres reales.
- `--table` para una tabla Markdown, `--by-segment` para el corte antiguo,
  `-o fichero.md` para elegir la salida (por defecto `<id>.guion.md`).

## JSON simplificado

`json_to_simple.py` reduce el JSON de WhisperX (4,8 MB, con `words`, `score`,
`avg_logprob`…) a una lista plana con solo lo necesario:

```bash
.venv\Scripts\python.exe json_to_simple.py output/2vv4hHAvqnE.json
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

Agrupa por turno de hablante con la misma lógica que `json_to_script.py`
(547 filas en el vídeo de ejemplo). Con `--by-segment` da una fila por segmento
de Whisper (643) y con `--by-word` una por palabra (14 067). Acepta también
`--names`, `--min-words`, `--round N` (decimales de los tiempos, `-1` para
dejarlos como están), `--indent` y `-o`.
