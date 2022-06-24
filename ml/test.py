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

from ml_testing import test_frame_processor

test_frame_processor("/home/emperornao/projects/EmotionRecognition/ml/angry.jpg")