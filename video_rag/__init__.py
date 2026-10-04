"""Video -> text pipeline with WhisperX, plus LLM-based ingestion for RAG.

Hexagonal layout (dependencies only point inwards):

    interfaces      driving adapters (cli/, later api/)
    application     use cases + the ports they depend on
    domain          pure logic: no I/O, no third-party imports
    infrastructure  driven adapters that implement the ports

`container.py` is the composition root: the only module that chooses
concrete adapters.
"""
