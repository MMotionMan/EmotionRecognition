

import numpy as np
import torch.nn.functional as F


class FrameProcesser:

	def __init__(self, mode, model, preprocessor, detector = None):
		"""
		mode = "one/all"
		model: model to predict
		preprocessor: function to preprocess Image before model
		detector: which detector to use
		"""
		assert mode in ["one", "all"]
		assert not (mode == "all" and detector)
		self.mode = mode
		self.model = model
		self.preprocessor = preprocessor

	def process_image(self, image: np.ndarray):

		print(type(image))
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
			faces = detector(image)
			for (l, t, w, h) in faces:
				face = img[t:t+h, t:t+w]
				out.append([(l, t, w, h), self.process_image(face)])
			return out

		else:
			raise ValueError("Not valide mode: {mode}".format(mode=self.mode))




