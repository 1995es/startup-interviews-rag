# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Qué es esto

Pipeline local de **vídeo → texto** con WhisperX, portado desde el notebook de
Google Colab `Demo_WhisperX.ipynb` (que se conserva sin tocar como referencia
del original). Sin framework ni tests:

- `youtube_to_json.py` — **el camino corto y el recomendado**: URL (o fichero)
  → JSON `[{text, speaker, start, end}]` en una sola invocación. Es la fusión
  de los tres scripts de abajo, autocontenido (no importa de ellos). Versión
  mínima y **en inglés** (es el fichero pensado para publicar en GitHub): sin
  flags de dispositivo ni de granularidad, la diarización se activa sola si hay
  `HF_TOKEN` en el entorno (no hay `--hf-token`), y GPU/CPU se autodetectan sin
  fallback a CPU.
- `video_to_text.py` — URL o fichero local → wav 16 kHz mono → transcripción →
  alineación por palabra → diarización opcional → `.txt` / `.json` / `.srt`
  (+ `.speakers.txt`).
- `json_to_script.py` — el `.json` anterior → guion Markdown tipo entrevista,
  una fila por intervención.
- `json_to_simple.py` — el mismo `.json` → lista plana de
  `{text, speaker, start, end}`. **Importa la lógica de turnos de
  `json_to_script.py`** (`build_turns_by_word`, `smooth_runs`, …); si cambias
  cómo se agrupan los hablantes, cambia los dos a la vez — y también la copia
  que vive dentro de `youtube_to_json.py` (son **tres** sitios).

`guiones/` es la unica carpeta de salida que **si** se versiona: los diez
guiones de videos de Itnig (`.md` anotado + `.json` plano) mas su indice. Se
regenera con el pipeline normal; `audio/` y `output/` siguen ignorados.

No hay entorno "de sistema": todo se ejecuta con el intérprete del venv del
proyecto, `.venv\Scripts\python.exe` (Windows, Python 3.12 de Anaconda).

## Comandos

```bash
# Todo de una vez: URL -> output/<id>.json con {text, speaker, start, end}
.venv\Scripts\python.exe youtube_to_json.py "https://www.youtube.com/watch?v=..." --language es --min-speakers 2

# Transcribir (el modelo por defecto es large-v2)
.venv\Scripts\python.exe video_to_text.py "https://www.youtube.com/watch?v=..." --language es

# Con diarización (necesita HF_TOKEN en el entorno, nunca en el código)
.venv\Scripts\python.exe video_to_text.py "audio/foo.wav" --language es --diarize --min-speakers 2

# Iteración rápida sobre cambios de código: modelo pequeño + audio corto
.venv\Scripts\python.exe video_to_text.py "audio/foo.wav" --model tiny --language es --outdir output_test

# JSON → guion Markdown
.venv\Scripts\python.exe json_to_script.py output/<id>.json --timestamps

# JSON → JSON plano {text, speaker, start, end}
.venv\Scripts\python.exe json_to_simple.py output/<id>.json
```

Reejecutar sobre un `.wav` ya descargado en `audio/` ahorra la descarga; el
script detecta que la entrada ya es wav y no vuelve a pasar por ffmpeg.

## Restricciones del entorno (comprobadas, no cambiar a la ligera)

Estas versiones están fijadas en `requirements.txt` porque las alternativas
**rompen en este equipo** (Win 11, RTX 4070). Antes de "actualizar
dependencias", verificar con una carga de modelo real:

- `torch 2.8.0+cu126`. La 2.13 falla al importar (`WinError 1114` cargando
  `c10.dll`), también en la instalación de Anaconda del sistema.
- El sufijo `+cu126` es obligatorio en el pin: con `torch==2.8.0` pip da por
  buena la rueda `+cpu` y `torch.cuda.is_available()` pasa a `False`.
- `ctranslate2 4.5.0`. La 4.8.1 (la que arrastra `faster-whisper`) provoca
  *segfault* (exit 139) al cargar cualquier modelo, incluso en CPU.
- `nvidia-cublas-cu12` / `nvidia-cudnn-cu12` están instalados porque
  CTranslate2 necesita esas DLL en Windows.

Al depurar caídas: un pipe (`| tail`) se traga el código de salida y la salida
bufferizada de un proceso que muere de golpe. Usar `PYTHONUNBUFFERED=1` y
`${PIPESTATUS[0]}` — así se vio que el "exit 0" silencioso era en realidad un
segfault de CTranslate2.

## Detalles de diseño que no se ven en una lectura rápida

**`_register_cuda_dlls()` se ejecuta al importar `video_to_text.py`, antes que
whisperx.** Registra `torch/lib` y `site-packages/nvidia/*/bin` como
directorios de DLL. Sin eso CTranslate2 no encuentra cuDNN/cuBLAS en Windows.
No mover esa llamada por debajo de los imports de whisperx.

**Los turnos de hablante se cortan por palabra, no por segmento.** Un segmento
de Whisper dura ~20 s y suele contener pregunta y respuesta, así que agrupar
por `segment["speaker"]` destruye el diálogo (643 turnos falsos vs. 547 reales
en el vídeo de ejemplo). `json_to_script.py` reconstruye los turnos desde
`segments[].words[].speaker` y aplica dos correcciones encadenadas:
`smooth_runs()` absorbe las rachas de menos de `--min-words` palabras (la
diarización salta de hablante en palabras sueltas) y `snap_to_sentences()`
desplaza el corte al final de frase más cercano (±3 palabras) para no partir
oraciones. `build_turns_by_segment()` es el camino de reserva cuando el JSON no
trae speakers por palabra.

**`video_to_text.py` genera su `.speakers.txt` agrupando por segmento**, o sea
con la lógica peor. Es una inconsistencia conocida: el fichero bueno es el
`.guion.md` de `json_to_script.py`.

**La descarga de YouTube reintenta con varias cadenas de formato**
(`bestaudio/best` → `251/140/bestaudio` → `18/best`). El `bestaudio/best` del
notebook original daba 403 en YouTube; no simplificar ese bucle. Ese bucle **no** salva un
yt-dlp desfasado: con 2026.7.4 YouTube devolvia 403 en cualquier descarga
completa, con las tres cadenas y con todos los `player_client` (`tv_embedded`,
`android`, `ios`…). Sintoma caracteristico: `--list-formats` funciona y hasta
un `--test` de 10 kB pasa, pero la descarga entera muere con 403. Se arregla
actualizando yt-dlp, no tocando el codigo.

**Degradación en cascada**: si falla la carga en GPU se reintenta en CPU/int8;
si se pide `--diarize` sin `HF_TOKEN` se avisa y se continúa sin diarizar. El
script no debería abortar por falta de diarización.

## Convenciones

- Los mensajes de usuario, los comentarios y los docstrings están en castellano
  **sin acentos en el código** (los `print`/`log` van sin tildes a propósito,
  por la consola de Windows con cp1252); el Markdown generado sí lleva tildes.
  Excepción: `youtube_to_json.py` está íntegramente en inglés.
- Los ficheros generados (`audio/`, `output/`) no son fuente: se pueden
  regenerar y no hay que editarlos a mano.
