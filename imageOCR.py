import pprint
import boto3
try:
	from keys import *
	USE_AWS = True
except:
	import pytesseract
	from PIL import Image
	USE_AWS = False

def ocr(imageFile):
	allWords = []
	if USE_AWS == True:
		client = boto3.client('rekognition', "us-east-1", aws_access_key_id=AWS_ACCESS_KEY,
		aws_secret_access_key=AWS_SECRET_KEY)

		# Our source image: http://i.imgur.com/OK8aDRq.jpg
		with open(imageFile, 'rb') as source_image:
			source_bytes = source_image.read()

		response = client.detect_text(
		Image={ 'Bytes': source_bytes }
		)
		# return response['Labels']

		for val in response["TextDetections"]:
			if val['Type'] == 'WORD':
				allWords.append(val['DetectedText'])
	else:
		for val in pytesseract.image_to_string(Image.open(imageFile)).split(" "):
			for word in val.split("\n"):
				allWords.append(word)
	return allWords

if __name__ == '__main__':
	print ocr("frame00020.jpg")
	