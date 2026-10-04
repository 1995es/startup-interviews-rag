class VideoRagError(Exception):
    """Base of every expected failure. Interfaces catch it and report the
    message; anything else is a bug and keeps its traceback."""
