# Guiones — 10 vídeos de Itnig

Transcripción completa de 10 vídeos del canal [Itnig](https://www.youtube.com/@itnig) elegidos al azar (10,2 h de audio · 104.233 palabras), generada con el pipeline de
este repositorio:

```bash
.venv\Scripts\python.exe video_to_text.py "<url>" --language es --diarize --min-speakers 2
.venv\Scripts\python.exe json_to_script.py output/<id>.json --timestamps
.venv\Scripts\python.exe json_to_simple.py output/<id>.json
```

## Cómo se eligieron

Sorteo reproducible sobre el listado del canal (`yt-dlp --flat-playlist`, 683 vídeos,
consultado el 2026-09-10), restringido a los 525 de entre 10 y 90 minutos para dejar
fuera *shorts* y clips sueltos: `random.seed(20260910)` + `random.sample(candidatos, 10)`.
El detalle completo, en [`seleccion.json`](seleccion.json).

## Los diez

| # | Vídeo | Publicado | Duración | Intervenciones | Voces | Guion | JSON |
|---|---|---|---|---|---|---|---|
| 1 | [Debate sobre la IA con ingenieros de Factorial \| Tertulia de itnig](https://www.youtube.com/watch?v=i-ZOzESUG4U) | 2026-04-03 | 1 h 30 min | 301 | 10 | [md](01-debate-sobre-la-ia-con-ingenieros-de-factorial-tertulia.md) | [json](01-debate-sobre-la-ia-con-ingenieros-de-factorial-tertulia.json) |
| 2 | [Wallbox, líder en carga de vehículos eléctricos - Podcast 203](https://www.youtube.com/watch?v=O86d0vLhZ8o) | 2021-08-30 | 1 h 19 min | 130 | 4 | [md](02-wallbox-lider-en-carga-de-vehiculos-electricos-podcast.md) | [json](02-wallbox-lider-en-carga-de-vehiculos-electricos-podcast.json) |
| 3 | [FACTORIAL compra FUELL: TODOS los DETALLES \| Podcast #300](https://www.youtube.com/watch?v=NBRsqb57UGk) | 2023-10-03 | 1 h 12 min | 232 | 6 | [md](03-factorial-compra-fuell-todos-los-detalles-podcast-300.md) | [json](03-factorial-compra-fuell-todos-los-detalles-podcast-300.json) |
| 4 | [Desbancando a la banca con Ritmo - Podcast 202](https://www.youtube.com/watch?v=T1TnElUx_Lc) | 2021-08-09 | 1 h 06 min | 128 | 4 | [md](04-desbancando-a-la-banca-con-ritmo-podcast-202.md) | [json](04-desbancando-a-la-banca-con-ritmo-podcast-202.json) |
| 5 | [Takeaways de Factorial, Veo2 y ¿Vuelve Enron?](https://www.youtube.com/watch?v=rxpnoY6vvqg) | 2024-12-20 | 1 h 06 min | 209 | 3 | [md](05-takeaways-de-factorial-veo2-y-vuelve-enron.md) | [json](05-takeaways-de-factorial-veo2-y-vuelve-enron.json) |
| 6 | [De CEO en Rakuten a ABA English con Marc Vicente - Podcast 99](https://www.youtube.com/watch?v=cskcbNYFUss) | 2019-07-22 | 56 min | 101 | 4 | [md](06-de-ceo-en-rakuten-a-aba-english-con-marc-vicente-podcas.md) | [json](06-de-ceo-en-rakuten-a-aba-english-con-marc-vicente-podcas.json) |
| 7 | [Salir en el New York Times me generó 200M € al año \| Ferran Adrià \| El PLAYBook by Itnig #3](https://www.youtube.com/watch?v=AO8ty6W2rzE) | 2024-06-24 | 48 min | 159 | 4 | [md](07-salir-en-el-new-york-times-me-genero-200m-al-ano-ferran.md) | [json](07-salir-en-el-new-york-times-me-genero-200m-al-ano-ferran.json) |
| 8 | [Alquiler de barcos con Octavi Uyà de Nautal - Podcast 121](https://www.youtube.com/watch?v=yOLw6ncCJwY) | 2020-01-07 | 47 min | 169 | 3 | [md](08-alquiler-de-barcos-con-octavi-uya-de-nautal-podcast-121.md) | [json](08-alquiler-de-barcos-con-octavi-uya-de-nautal-podcast-121.json) |
| 9 | [ChatGPT y su futuro con Microsoft - Tertulia #41](https://www.youtube.com/watch?v=ByUPHrcSoEA) | 2023-01-13 | 43 min | 138 | 5 | [md](09-chatgpt-y-su-futuro-con-microsoft-tertulia-41.md) | [json](09-chatgpt-y-su-futuro-con-microsoft-tertulia-41.json) |
| 10 | [El fiasco de Bard y la guerra de los chatbots - Tertulia #45](https://www.youtube.com/watch?v=csYm72OZNuM) | 2023-02-10 | 43 min | 175 | 6 | [md](10-el-fiasco-de-bard-y-la-guerra-de-los-chatbots-tertulia.md) | [json](10-el-fiasco-de-bard-y-la-guerra-de-los-chatbots-tertulia.json) |

## Qué hay en cada fichero

- `NN-titulo.md` — el guion: una línea por intervención, con marca de tiempo e
  interlocutor (`` `00:12:34` **SPEAKER_01** — … ``). Es la salida de
  `json_to_script.py`, que corta los turnos **por palabra** y no por segmento.
- `NN-titulo.json` — lo mismo en `[{text, speaker, start, end}]`, para procesar.

## Avisos

- Todo es **automático y sin revisar**: Whisper se inventa palabras con audio malo,
  se come nombres propios y puntúa a su manera.
- `SPEAKER_XX` es una etiqueta, no una persona. La diarización agrupa voces por
  parecido acústico; no sabe quién es quién y a veces parte o fusiona hablantes.
- El JSON completo de WhisperX (con `words`, `score`…) pesa ~5 MB por vídeo y no
  está en el repositorio: se regenera con `video_to_text.py`.
- El contenido de los vídeos es de Itnig; esto es una transcripción con fines de
  análisis y búsqueda.
