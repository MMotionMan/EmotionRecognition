from os import walk
import numpy as np
import cv2
import os
import pandas as pd


f = []
for (dirpath, dirnames, filenames) in walk("/home/emperornao/projects/EmotionRecognition/ml/tmp"):
    for name in filenames:
        f.append(os.path.join(dirpath, name))


data = []


for ind, file in enumerate(f):
	img = cv2.resize(cv2.cvtColor(cv2.imread(str(file)), cv2.COLOR_BGR2GRAY),(48,48))
	print(img.shape)
	str = " ".join(map(str, img.reshape(-1).tolist()))

	data.append({"emotion":7, "pixels": str})
	if ind > 50000:
		break


df = pd.DataFrame(data, columns = ['emotion', 'pixels'])
df.to_csv("tmp.csv")

