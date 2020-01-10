import os
import random
import cv2
import glob
from PIL import Image, ImageStat
from mutagen.mp4 import MP4
from PIL import Image, ImageDraw, ImageFont
import textwrap
import imageOCR
import threading
import sys

OVERRIDE_OCR = False

def recreate_image(fileName, override=None):
	print("RECREATING IMAGE {}".format(fileName))
	if override == None:
		text = imageOCR.ocr(fileName)
	else:
		text = override
	text = ' '.join(text).capitalize()
	x = Image.open(fileName)
	MAX_W, MAX_H = x.size
	img = Image.new('RGB', (MAX_W, MAX_H), color = (0, 0, 0, 0))
 
	font = ImageFont.truetype('arial.ttf', 30)
	draw = ImageDraw.Draw(img)

	para = textwrap.wrap(text, width=30)

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
	command += '"ytsearch3:{} lyrics" '.format(song)
	command += '--get-id > tmp'
	os.system(command)
	return [x for x in open('tmp').read().split("\n") if len(x) > 0]

def download_by_id(idVal, song, index):
	fileName = "download_" + ''.join([str(random.randint(1,9)) for i in range(10)]) + "{}.mp4".format(index)
	command = "youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' https://www.youtube.com/watch?v={} ".format(idVal)
	command += '--output "{}"'.format(fileName)
	os.system(command)
	# os.system("youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' ytsearch3:'nine in the afternoon lyrics' --get-id")
	return fileName

def create_video():
    os.system("ffmpeg -r 1 -i frame%01d.png -vcodec mpeg4 -y movie.mp4")

# Info is a tuple containing index, val (a url), and the fileName
def create_video_from_info(info):
	index, val, fileName = info
	index += 1
	a = download_by_id(val, songName, index)
	finalFileName = songName.replace(" ", "_") + "{}.mp4".format(index)
	vidcap = cv2.VideoCapture(a)
	success,image = vidcap.read()
	count = 0
	success = True
	db = {}
	os.system("ffmpeg -i {} -vf fps=1 frame_{}_%05d.jpg".format(a, index))
	for frameFile in glob.glob("frame_{}*jpg".format(index)):
		  db[frameFile] = frameFile
		  count += 1
	# count = len(list())
	os.system("ffmpeg -i {} -f mp3 -ab 192000 -vn audio_{}.mp3".format(a, index))
	audio = MP4(a)
	# os.system("cp frame* test/")
	# raw_input(audio.info.length)
	fps = 1
	# print("length of each frame in seconds: {}".format())
	# raw_input("FPS ^")
	vals = [None]
	valsInfo = [None]
	allFiles = list(glob.glob("frame_{}_*.jpg".format(index)))
	allFiles.sort(key=lambda k: int(k.replace("frame_{}_".format(index), "").replace(".jpg", "")))
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
	for val in valsInfo:
		if val != None:
			if OVERRIDE_OCR == True:
				recreate_image(val, "Video {}".format(index))
			else:
				recreate_image(val)
	files = []
	os.system("mkdir temp_{}".format(index))
	os.system("rm temp_{}/*".format(index))
	for k, v in db.iteritems():
		command = "cp {} temp_{}/{}".format(v, index, k)
		os.system(command)
		print(command)
	# os.system("mkdir temp")
	os.system("./finalize.sh {} {}".format(finalFileName, index))
	os.system("./clearAll.sh {}".format(index))
	# allFiles = list(glob.glob("frame*.jpg"))
	# allFiles.sort(key=lambda k: int(k.replace("frame", "").replace(".jpg", "")))
	return


def create_lyric_video(songName):
	allOptions = get_all_song_options(songName)
	# raw_input(allOptions)
	a = []
	for index, val in enumerate(allOptions):
		a.append((index, val, songName))
	thread = [threading.Thread(target=create_video_from_info, args=(info,)) for info in a]
	for t in thread:
		t.start()
	for t in thread:
		t.join()

if __name__ == '__main__':

	if '-f' in sys.argv:
		songs = open(sys.argv[2]).read().split("\n")
	else:
		songs = [" ".join(sys.argv[1:])]

	for songName in songs:
		print songName
	quit()

	for songName in songs:
		try:
			create_lyric_video(songName)
		except Exception as exp:
			print("ERROR {} {}".format(songName, exp))

	quit()
	# recreate_image("frame00020.jpg")
	# raw_input("CONTINUE")
	
	
	


