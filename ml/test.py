"""import os
import cv2

#helper_function for real time testing
def load_img(path):
    img = Image.open(path)
    img = transformation(img).float()
    img = torch.autograd.Variable(img,requires_grad = True)
    img = img.unsqueeze(0)
    return img.to(device)


# Load the cascade
face_cascade = cv2.CascadeClassifier('cascade_model/haarcascade_frontalface_default.xml')

# To capture video from webcam.
cap = cv2.VideoCapture(0)
while True:
    # Read the frame
    _, img = cap.read()
    

    print(type(img))
    

    cv2.imshow('img', img)
    # Stop if (Q) key is pressed
    k = cv2.waitKey(1)
    if k==ord("q"):
        break

cap.release()"""

from ml_testing import test_frame_processor_all
from ml_testing import test_video_processer_emotion
from ml_testing import test_video_processer_time

# test_frame_processor_all("/home/emperornao/projects/EmotionRecognition/ml/angry.jpg")
import cv2
import datetime
  

test_video_processer_time("/home/emperornao/projects/EmotionRecognition/ml/tmp.mp4")  
# # create video capture object
#data = cv2.VideoCapture('/home/emperornao/projects/EmotionRecognition/ml/test.mp4')
  
# # count the number of frames
# frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
# fps = int(data.get(cv2.CAP_PROP_FPS))
# print(float(frames)/fps)