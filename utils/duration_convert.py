def duration_convertation(duration: int):
    duration = int(duration)
    minutes = duration // 60
    seconds = duration - minutes * 60
    return f"{minutes}:{seconds}"