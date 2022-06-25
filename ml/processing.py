

import numpy as np
import torch.nn.functional as F
from torchvision import transforms
import cv2
import torch


class FrameProcesser:

	def __init__(self, mode, model, preprocessor, detector = None):
		"""
		mode = "one/all"
		model: model to predict
		preprocessor: function to preprocess Image before model
		detector: which detector to use
		"""
		assert mode in ["one", "all"]
		assert not (mode == "all" and not detector)
		self.mode = mode
		self.model = model
		self.preprocessor = preprocessor
		self.detector = detector

	def process_image(self, image: np.ndarray):

		preprocessed_image = self.preprocessor(image)
		output = self.model(preprocessed_image)
		probabilities = F.softmax(output)
		return probabilities

	def run(self, image: np.ndarray):
		"""
		image: image for which make prediction
		--------------------------------------------------------------------------------
		if mode is 'one' returns vector proba of emotions
		return np.ndarray with emotion number size
		--------------------------------------------------------------------------------
		if mode is 'all' returns all bounding boxes and vectors with proba for each
		bounding boxes returns in format left, top, width, height
		return [(l, t, w, h), np.ndarray with emotion number size]
		"""
		
		if self.mode == "one":
			return self.process_image(image)

		elif self.mode == "all":
			out = []
			faces = self.detector(image)
			for (l, t, w, h) in faces:
				face = image[t:t+h, t:t+w]
				out.append([(l, t, w, h), self.process_image(face)])
			return out

		else:
			raise ValueError("Not valide mode: {mode}".format(mode=self.mode))


class VideoProcesser:

	def __init__(self, model, mode, number_of_classes):
		"""
		mode = ["emotion", "timestamptz", "boxes"]
		"""
		assert mode in ["emotion", "timestamptz", "boxes"]
		self.mode = mode
		self.model = model
		self.number_of_classes = number_of_classes

	def process(self, videopath):
		"""
		function to be used in modes for emotion and timestamptz
		--------------------------------------------------------------------------------
		if mode is 'emotion' returns vector proba of emotions
		as relative to longest subsequence for each
		NO: return dict of emotion: longest_subst
		--------------------------------------------------------------------------------
		if mode is 'timestamptz' return list of pairs 
		[(start, end), emotion]

		"""
		if self.mode == "emotion":

			transformation = transforms.Compose([transforms.ToTensor(),transforms.Normalize((0.5,),(0.5,))])
			processor = FrameProcesser("one", self.model, preprocessor = lambda image: transformation(cv2.resize(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), (48, 48))).float().unsqueeze(0))

			self.cap = cv2.VideoCapture(videopath)

			ret, frame = self.cap.read()
			proba_sum = torch.argmax(processor.run(frame), dim=1).item()

			i = 0
			while(self.cap.isOpened()):
				i += 1
				ret, frame = self.cap.read()
				if not ret:
					break
				proba_sum += processor.run(frame)

			return torch.argmax(proba_sum, dim = 1)
			    
		elif self.mode == "timestamptz":

			transformation = transforms.Compose([transforms.ToTensor(),transforms.Normalize((0.5,),(0.5,))])
			processor = FrameProcesser("one", self.model, preprocessor = lambda image: transformation(cv2.resize(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), (48, 48))).float().unsqueeze(0))

			self.cap = cv2.VideoCapture(videopath)

			ret, frame = self.cap.read()
			last_emotion = torch.argmax(processor.run(frame), dim=1).item() 

			fps = float(self.cap.get(cv2.CAP_PROP_FPS))
			frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

			stampz = []
			start_frame = 0
			number_frame = 0

			real_last_emotion = last_emotion
			last_streak = 1


			while(self.cap.isOpened()):
				number_frame += 1
				ret, frame = self.cap.read()
				if not ret:
					break

				proba = processor.run(frame)
				cur_emotion = torch.argmax(proba, dim=1).item() 

				if cur_emotion != last_emotion and proba[0][cur_emotion] > proba[0][last_emotion] * 2:
					# if cur_emotion == real_last_emotion and streak > 3:
					stampz.append(((start_frame / float(fps), number_frame / float(fps)), last_emotion))
					last_emotion = cur_emotion
					start_frame = number_frame
					# if last_emotion != real_last_emotion:
					# 	real_last_emotion = last_emotion
					# 	last_streak = 0

				last_streak += 1

			if start_frame == 0:
				stampz.append(((start_frame / float(fps), number_frame / float(fps)), last_emotion))

			return stampz

		else:
			raise ValueError("Not valide mode: {mode}".format(mode=self.mode))