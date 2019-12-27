import os
import random
import cv2
import glob
print(cv2.__version__)
from PIL import Image, ImageStat
from mutagen.mp4 import MP4
from PIL import Image, ImageDraw, ImageFont
import textwrap
import imageOCR

def recreate_image(fileName):
	text = imageOCR.ocr(fileName)
	text = ' '.join(text)
	x = Image.open(fileName)
	MAX_W, MAX_H = x.size
	img = Image.new('RGB', (MAX_W, MAX_H), color = (0, 0, 0, 0))
 
	font = ImageFont.truetype('arial.ttf', 30)
	draw = ImageDraw.Draw(img)

	para = textwrap.wrap(text, width=15)

	current_h, pad = 50, 10
	for line in para:
	    w, h = draw.textsize(line, font=font)
	    draw.text(((MAX_W - w) / 2, current_h), line, font=font)
	    current_h += h + pad

	# d.text((10,10), text, font=fnt, fill=(255, 255, 0))
	 
	img.save(fileName)

def hash_image(image_path):
    img = Image.open(image_path).resize((8,8), Image.LANCZOS).convert(mode="L")
    mean = ImageStat.Stat(img).mean[0]
    return sum((1 if p > mean else 0) << i for i, p in enumerate(img.getdata()))

def get_all_song_options(song):
	a = []
	command = "youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' "
	command += '"ytsearch1:{} lyrics" '.format(song)
	command += '--get-id > tmp'
	os.system(command)
	return [x for x in open('tmp').read().split("\n") if len(x) > 0]

def download_song(song):
	fileName = "download_" + ''.join([str(random.randint(1,9)) for i in range(10)]) + ".mp4"
	command = "youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' "
	command += '"ytsearch1:{} lyrics" '.format(song)
	command += '--output "{}"'.format(fileName)
	os.system(command)
	os.system("youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' ytsearch3:'nine in the afternoon lyrics' --get-id")
	return fileName

def download_by_id(idVal, song):
	fileName = "download_" + ''.join([str(random.randint(1,9)) for i in range(10)]) + ".mp4"
	command = "youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' https://www.youtube.com/watch?v={} ".format(idVal)
	command += '--output "{}"'.format(fileName)
	os.system(command)
	# os.system("youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' ytsearch3:'nine in the afternoon lyrics' --get-id")
	return fileName


def create_video():
    os.system("ffmpeg -r 1 -i frame%01d.png -vcodec mpeg4 -y movie.mp4")

def create_lyric_video(songName):
	allOptions = get_all_song_options(songName)
	for index, val in enumerate(allOptions):
		raw_input(allOptions)
		a = download_by_id(val, songName)
		finalFileName = songName.replace(" ", "_") + ".mp4"
		vidcap = cv2.VideoCapture(a)
		success,image = vidcap.read()
		count = 0
		success = True
		db = {}
		while success:
			  frameFile = "frame{}.jpg".format(str(count).zfill(5))
			  cv2.imwrite(frameFile, image)     # save frame as JPEG file
			  success,image = vidcap.read()
			  db[frameFile] = frameFile
			  count += 1
		os.system("ffmpeg -i {} -f mp3 -ab 192000 -vn audio.mp3".format(a))
		audio = MP4(a)
		# os.system("cp frame* test/")
		# raw_input(audio.info.length)
		# print(os.path.getsize(a))
		fps = int(float(count) / audio.info.length)
		# print("length of each frame in seconds: {}".format())
		# raw_input("FPS ^")
		vals = [None]
		valsInfo = [None]
		allFiles = list(glob.glob("frame*.jpg"))
		allFiles.sort(key=lambda k: int(k.replace("frame", "").replace(".jpg", "")))
		for i, imageVal in enumerate(allFiles):
			print imageVal
			result = hash_image(imageVal)
			# print result
			if result == vals[-1]:
				# print("removed")
				os.system("rm {}".format(imageVal))
				db[imageVal] = valsInfo[-1]
			else:
				vals.append(result)
				valsInfo.append(imageVal)
			# print(i)
		if len(valsInfo) < 100 or index == len(allFiles) - 1:
			for val in valsInfo:
				if val != None:
					recreate_image(val)
			files = []
			os.system("mkdir temp")
			os.system("rm temp/*")
			for k, v in db.iteritems():
				command = "cp {} temp/{}".format(v, k)
				os.system(command)
				print(command)
			# os.system("mkdir temp")
			os.system("ffmpeg -framerate 30 -i temp/frame%05d.jpg Project.mp4")
			os.system("ffmpeg -i Project.mp4 -i audio.mp3 -c copy -map 0:v:0 -map 1:a:0 final.mp4")
			os.system("rm temp/*")
			os.system("rm Project.mp4")
			os.system("rm *.mp3")
			os.system("rm frame*")
			os.system("rm download_*")
			os.system("mv final.mp4 {}".format(finalFileName))
			# allFiles = list(glob.glob("frame*.jpg"))
			# allFiles.sort(key=lambda k: int(k.replace("frame", "").replace(".jpg", "")))
			return
		else:
			print("Trying next video...")
			os.system("rm *.mp3")
			os.system("rm frame*")
			os.system("rm download_*")


if __name__ == '__main__':
	# recreate_image("frame00020.jpg")
	# raw_input("CONTINUE")
	for songName in open("songs.txt").read().split("\n"):
		try:
			# songName = raw_input("Song Name: ")
			create_lyric_video(songName)
		except Exception as exp:
			print("ERROR {} {}".format(songName, exp))
	
	


