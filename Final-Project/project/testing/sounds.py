import simpleaudio as sa

def play_sound(func):
    name = func.__name__
    if not name.startswith("play_"):
        raise ValueError("Function name must start with 'play_'")
    file = name[5:]
    def player():
        return sa.WaveObject.from_wave_file(f"../sounds/file.wav").play()
    return player

@play_sound
def play_collect():
    pass

@play_sound
def play_clear():
    pass

@play_sound
def play_estop():
    pass

@play_sound
def play_help():
    pass