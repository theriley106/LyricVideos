import os
import random
import cv2
import glob
print(cv2.__version__)
from PIL import Image, ImageStat
from mutagen.mp4 import MP4



def hash_image(image_path):
    img = Image.open(image_path).resize((8,8), Image.LANCZOS).convert(mode="L")
    mean = ImageStat.Stat(img).mean[0]
    return sum((1 if p > mean else 0) << i for i, p in enumerate(img.getdata()))

def download_song(song):
	fileName = ''.join([str(random.randint(1,9)) for i in range(10)]) + ".mp4"
	command = "youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' "
	command += '"ytsearch1:{} lyrics" '.format(song)
	command += '--output "{}"'.format(fileName)
	os.system(command)
	return fileName

def create_video():
    os.system("ffmpeg -r 1 -i frame%01d.png -vcodec mpeg4 -y movie.mp4")




if __name__ == '__main__':
	a = download_song('nine in the afternoon')
	vidcap = cv2.VideoCapture(a)
	success,image = vidcap.read()
	count = 0
	success = True
	while success:
		  cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
		  success,image = vidcap.read()
		  count += 1
	audio = MP4(a)

	# raw_input(audio.info.length)
	# print(os.path.getsize(a))
	print("length of each frame in seconds: {}".format(audio.info.length / float(count)))
	# raw_input()
	vals = [None]
	allFiles = list(glob.glob("frame*.jpg"))
	allFiles.sort(key=lambda k: int(k.replace("frame", "").replace(".jpg", "")))
	for i, imageVal in enumerate(allFiles):
		print imageVal
		result = hash_image(imageVal)
		# print result
		if result == vals[-1]:
			# print("removed")
			os.system("rm {}".format(imageVal))
		else:
			vals.append(result)
		# print(i)

