import torch
from torchvision import transforms

import numpy as np
import os

os.environ.pop("QT_QPA_PLATFORM")
import cv2

from PIL import Image

from processing import FrameProcesser


def test_frame_processor(filename):


	print(cv2.__version__ )
	from deep_emotion import Deep_Emotion

	model = Deep_Emotion()
	model.to('cpu')
	model.load_state_dict(torch.load("/home/emperornao/projects/EmotionRecognition/ml/weights.pt", map_location=torch.device('cpu')))
	model.eval()

	image = np.array(Image.open(filename))
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	image = cv2.resize(image, (48, 48))

	classes = ('Angry', 'Disgust', 'Fear', 'Happy','Sad', 'Surprise', 'Neutral')

	transformation = transforms.Compose([transforms.ToTensor(),transforms.Normalize((0.5,),(0.5,))])
	processor = FrameProcesser("one", model, preprocessor = lambda img: transformation(img).float().unsqueeze(0))


	proba = processor.run(image)
	classname = classes[torch.argmax(proba, dim=1)]

	image = cv2.putText(image, 
		classname, 
		(50, 50),  
		cv2.FONT_HERSHEY_SIMPLEX,
		1, 
		(255, 0, 0), 
		2, 
		cv2.LINE_AA
		)

	while True:
		cv2.imshow(filename, np.array(Image.open(filename)))

