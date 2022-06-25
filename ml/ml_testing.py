import torch
from torchvision import transforms

import numpy as np
import os

import cv2

from PIL import Image

from processing import FrameProcesser, VideoProcesser


def prepare():

	from deep_emotion import Deep_Emotion
	model = Deep_Emotion()
	model.to('cpu')
	model.load_state_dict(torch.load("/home/emperornao/projects/EmotionRecognition/ml/weights.pt", map_location=torch.device('cpu')))
	model.eval()



def test_frame_processor_one(filename):


	from deep_emotion import Deep_Emotion

	model = Deep_Emotion()
	model.to('cpu')
	model.load_state_dict(torch.load("/home/emperornao/projects/EmotionRecognition/ml/weights.pt", map_location=torch.device('cpu')))
	model.eval()


	orig_image = cv2.imread(filename)
	image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2GRAY)

	classes = ('Angry', 'Disgust', 'Fear', 'Happy','Sad', 'Surprise', 'Neutral')

	transformation = transforms.Compose([transforms.ToTensor(),transforms.Normalize((0.5,),(0.5,))])
	processor = FrameProcesser("one", model, preprocessor = lambda img: transformation(cv2.resize(image, (48, 48))).float().unsqueeze(0))

	proba = processor.run(image)
	classname = classes[torch.argmax(proba, dim=1)]

	image = cv2.putText(orig_image, 
		classname, 
		(50, 50),  
		cv2.FONT_HERSHEY_SIMPLEX,
		1, 
		(255, 0, 0), 
		2, 
		cv2.LINE_AA
		)

	cv2.imshow(filename, image)
	cv2.waitKey(0)


def test_frame_processor_all(filename):


	from deep_emotion import Deep_Emotion

	model = Deep_Emotion()
	model.to('cpu')
	model.load_state_dict(torch.load("/home/emperornao/projects/EmotionRecognition/ml/weights.pt", map_location=torch.device('cpu')))
	model.eval()


	image = cv2.imread(filename)
	#image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2GRAY)

	classes = ('Angry', 'Disgust', 'Fear', 'Happy','Sad', 'Surprise', 'Neutral')

	detector = lambda x: cv2.CascadeClassifier('/home/emperornao/projects/EmotionRecognition/ml/haarcascade_frontalface_default.xml').detectMultiScale(cv2.cvtColor(x, cv2.COLOR_BGR2GRAY), 1.1, 4, flags = cv2.CASCADE_SCALE_IMAGE)
	transformation = transforms.Compose([transforms.ToTensor(),transforms.Normalize((0.5,),(0.5,))])
	processor = FrameProcesser("all", model, preprocessor = lambda image: transformation(cv2.resize(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), (48, 48))).float().unsqueeze(0), detector=detector)


	out = processor.run(image)



	for ((x, y, w, h), proba) in out:
		print(proba)
		classname = classes[torch.argmax(proba, dim=1)]
		image = cv2.putText(image, 
		classname, 
		(x, y),  
		cv2.FONT_HERSHEY_SIMPLEX,
		1, 
		(255, 0, 0), 
		2, 
		cv2.LINE_AA
		)

		cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)


	cv2.imshow(filename, image)
	cv2.waitKey(0)


def test_video_processer_emotion(filename):


	from deep_emotion import Deep_Emotion

	model = Deep_Emotion()
	model.to('cpu')
	model.load_state_dict(torch.load("/home/emperornao/projects/EmotionRecognition/ml/weights.pt", map_location=torch.device('cpu')))
	model.eval()

	processer = VideoProcesser(model, "emotion", 7)
	outp = processer.process(filename)
	print(outp)


def test_video_processer_time(filename):


	from deep_emotion import Deep_Emotion

	model = Deep_Emotion()
	model.to('cpu')
	model.load_state_dict(torch.load("/home/emperornao/projects/EmotionRecognition/ml/weights.pt", map_location=torch.device('cpu')))
	model.eval()

	processer = VideoProcesser(model, "timestamptz", 7)
	outp = processer.process(filename)
	for el in outp:
		print(el)
