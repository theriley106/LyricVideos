import os
import random

def download_song(song):
	fileName = ''.join([str(random.randint(1,9)) for i in range(10)]) + ".mp4"
	command = "youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' "
	command += '"ytsearch1:{} lyrics" '.format(song)
	command += '--output "{}"'.format(fileName)
	os.system(command)
	return fileName

if __name__ == '__main__':
	download_song('nine in the afternoon')
