import vlc


def playSong(player):
	if player:
		player.stop()
	name = input("Name of the song:  ")
	player = vlc.MediaPlayer("GreatWar.mp3")
	player.play()
	return player


def stopSong(player):
	player.stop()
	return player

player = ""
player = playSong(player)
while True:
	action = input("Action: ")
	if action == "play":
		player = playSong(player)
	elif action == "stop":
		player = stopSong(player)
	elif action == "quit":
		break



