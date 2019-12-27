import os
import random
import cv2
import glob
print(cv2.__version__)
from PIL import Image, ImageStat
from mutagen.mp4 import MP4
import pytesseract
from PIL import Image, ImageDraw, ImageFont
 


def recreate_image(fileName):
	text = pytesseract.image_to_string(Image.open(fileName))
	x = Image.open(fileName)
	width, height = x.size
	img = Image.new('RGB', (width, height), color = (73, 109, 137))
 
	fnt = ImageFont.truetype('arial.ttf', 30)
	d = ImageDraw.Draw(img)
	d.text((10,10), text, font=fnt, fill=(255, 255, 0))
	 
	img.save(fileName)

def hash_image(image_path):
    img = Image.open(image_path).resize((8,8), Image.LANCZOS).convert(mode="L")
    mean = ImageStat.Stat(img).mean[0]
    return sum((1 if p > mean else 0) << i for i, p in enumerate(img.getdata()))

def download_song(song):
	fileName = "download_" + ''.join([str(random.randint(1,9)) for i in range(10)]) + ".mp4"
	command = "youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' "
	command += '"ytsearch1:{} lyrics" '.format(song)
	command += '--output "{}"'.format(fileName)
	os.system(command)
	return fileName

def create_video():
    os.system("ffmpeg -r 1 -i frame%01d.png -vcodec mpeg4 -y movie.mp4")

def create_lyric_video(songName):
	a = download_song(songName)
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



if __name__ == '__main__':
	for songName in open("songs.txt").read().split("\n"):
		try:
			# songName = raw_input("Song Name: ")
			create_lyric_video(songName)
		except Exception as exp:
			print("ERROR {} {}".format(songName, exp))
	
	


