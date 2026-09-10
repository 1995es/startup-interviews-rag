# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Qué es esto

Pipeline local de **vídeo → texto** con WhisperX. Sin framework, sin paquete y
sin tests: dos scripts sueltos en la raíz.

- `youtube_to_json.py` — **el pipeline entero, autocontenido**: URL (o fichero
  local) → wav 16 kHz mono → transcripción → alineación por palabra →
  diarización → JSON `[{text, speaker, start, end}]` agrupado por turnos. Está
  íntegramente **en inglés** (es el fichero pensado para leerse desde GitHub).
  Versión deliberadamente mínima: sin flags de dispositivo ni de granularidad,
  la diarización se activa sola si hay `HF_TOKEN` en el entorno (no hay
  `--hf-token`) y GPU/CPU se autodetectan.
- `json_to_script.py` — ese JSON plano → guion Markdown tipo entrevista, una
  fila por intervención. **Solo maqueta**: no toca los turnos, que ya vienen
  cortados del pipeline. En castellano, como el resto de la documentación.

`guiones/` es la única carpeta de salida que **sí** se versiona: los diez
guiones de vídeos de Itnig (`.md` anotado + `.json` plano) más su índice. Se
regenera con el pipeline normal; `audio/` y `output/` siguen ignorados.

Todo se ejecuta con el intérprete del venv del proyecto,
`.venv\Scripts\python.exe` (Windows, Python 3.12 de Anaconda). No hay entorno
"de sistema".

## Comandos

```bash
# URL -> output/<id>.json con {text, speaker, start, end}
.venv\Scripts\python.exe youtube_to_json.py "https://www.youtube.com/watch?v=..." --language es --min-speakers 2

# Iteracion rapida sobre cambios de codigo: modelo pequeno + audio corto
.venv\Scripts\python.exe youtube_to_json.py "audio/foo.wav" --model tiny --language es -o output_test/foo.json

# JSON -> guion Markdown
.venv\Scripts\python.exe json_to_script.py output/<id>.json --timestamps
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

**`_register_cuda_dlls()` se ejecuta al importar `youtube_to_json.py`, antes que
whisperx.** Registra `torch/lib` y `site-packages/nvidia/*/bin` como
directorios de DLL. Sin eso CTranslate2 no encuentra cuDNN/cuBLAS en Windows.
No mover esa llamada por debajo de los imports de whisperx (que por eso mismo
son locales, dentro de `main()`).

**Los turnos de hablante se cortan por palabra, no por segmento.** Un segmento
de Whisper dura ~20 s y suele contener pregunta y respuesta, así que agrupar
por `segment["speaker"]` destruye el diálogo (643 turnos falsos vs. 547 reales
en el vídeo de ejemplo). `build_turns()` reconstruye los turnos desde
`segments[].words[].speaker` y aplica dos correcciones encadenadas:
`smooth_runs()` absorbe las rachas de menos de `--min-words` palabras (la
diarización salta de hablante en palabras sueltas) y `snap_to_sentences()`
desplaza el corte al final de frase más cercano (±3 palabras) para no partir
oraciones. Si el JSON no trae timings por palabra, cae a una fila por segmento.

**La descarga de YouTube reintenta con varias cadenas de formato**
(`bestaudio/best` → `251/140/bestaudio` → `18/best`). El `bestaudio/best` del
notebook original daba 403 en YouTube; no simplificar ese bucle. Ese bucle
**no** salva un yt-dlp desfasado: con 2026.7.4 YouTube devolvia 403 en
cualquier descarga completa, con las tres cadenas y con todos los
`player_client` (`tv_embedded`, `android`, `ios`…). Sintoma caracteristico:
`--list-formats` funciona y hasta un `--test` de 10 kB pasa, pero la descarga
entera muere con 403. Se arregla actualizando yt-dlp, no tocando el codigo.

**Degradación en cascada**: si falla la carga del modelo en GPU se reintenta en
CPU/int8; si no hay `HF_TOKEN` se avisa y se continúa sin diarizar. El script
no debería abortar por falta de diarización.

## Convenciones

- `youtube_to_json.py` está íntegramente en inglés. En el resto (mensajes,
  comentarios, docstrings de `json_to_script.py`) se escribe en castellano
  **sin acentos en el código** — los `print`/`log` van sin tildes a propósito,
  por la consola de Windows con cp1252. El Markdown generado sí lleva tildes.
- Los ficheros generados (`audio/`, `output/`) no son fuente: se pueden
  regenerar y no hay que editarlos a mano.
