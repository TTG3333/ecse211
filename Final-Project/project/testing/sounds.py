import simpleaudio as sa

def play_collect():
    return sa.WaveObject.from_wave_file("../sounds/collect.wav").play()

def play_clear():
    return sa.WaveObject.from_wave_file("../sounds/clear.wav").play()

def play_estop():
    return sa.WaveObject.from_wave_file("../sounds/estop.wav").play()

def play_help():
    return sa.WaveObject.from_wave_file("../sounds/help.wav").play()