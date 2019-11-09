import time 
import play_music

def timeUser(userTime):
	Set_Alarm = userTime

	Actual_Time = time.strftime("%H:%M")
	while (str(Actual_Time) != Set_Alarm):
		Actual_Time = time.strftime("%H:%M")
		time.sleep(1) 
	if (Actual_Time == Set_Alarm):
		play_music.play()
		print("Music should keep playing")
def stopAlarm():
	play_music.stopMusic()
