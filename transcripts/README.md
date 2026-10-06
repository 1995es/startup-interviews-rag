# Transcripts: 10 Itnig episodes

Full transcripts of 10 videos from the [Itnig](https://www.youtube.com/@itnig) channel,
picked at random (10.2 h of audio · 104,233 words) and produced with this repository's
pipeline:

```bash
poetry run python video_rag/interfaces/cli/prepare.py "<url>" --language es --min-speakers 2
poetry run python video_rag/interfaces/cli/script.py output/<id>.json --timestamps
```

The episodes are in Spanish, and so are the transcripts. They are the sample corpus
used to design and test the ingestion pipeline.

## How they were picked

A reproducible draw over the channel's video list (`yt-dlp --flat-playlist`, 683
videos, fetched on 2026-09-10), restricted to the 525 lasting between 10 and 90 minutes
to leave out shorts and loose clips: `random.seed(20260910)` +
`random.sample(candidates, 10)`. The full details are in
[`selection.json`](selection.json).

## The ten episodes

| # | Video | Published | Duration | Turns | Voices | Script | JSON |
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

## What each file holds

- `NN-title.json`: the pipeline output, `[{text, speaker, start, end}]`, one element
  per turn, with turns cut **per word** rather than per segment.
- `NN-title.md`: the same content laid out with `script.py`, one line per turn with a
  timestamp and a speaker (`` `00:12:34` **SPEAKER_01** — … ``). The header with the
  video link, date and duration was added by hand from
  [`selection.json`](selection.json); the rest of the file comes straight from the
  script. These files were generated with an earlier version of `script.py`, so their
  fixed labels are still in Spanish (*intervenciones*, *interlocutores*).

## Caveats

- Everything is **automatic and unreviewed**: Whisper invents words on bad audio, mangles
  proper names and punctuates its own way.
- `SPEAKER_XX` is a label, not a person. Diarization groups voices by acoustic
  similarity; it does not know who is who, and sometimes splits or merges speakers.
- WhisperX's raw JSON (with `words`, `score`…, ~5 MB per video) is not kept: the
  pipeline groups the turns and writes the flat list directly.
- The content of the videos belongs to Itnig; these transcripts are here for analysis
  and search purposes only.
