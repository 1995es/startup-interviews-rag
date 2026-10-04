def hhmmss(seconds: float | None) -> str:
    if seconds is None:
        return "--:--:--"
    s = int(float(seconds))
    return f"{s // 3600:02d}:{(s % 3600) // 60:02d}:{s % 60:02d}"
