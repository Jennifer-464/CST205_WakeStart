from pygame import mixer

def play():
	mixer.init()
	mixer.music.load("alarm.mp3")
	mixer.music.play(-1)
def stopMusic():
	mixer.music.stop()