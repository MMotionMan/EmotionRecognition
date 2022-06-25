import torch
from torchvision import transforms

from ml.deep_emotion import Deep_Emotion
from ml.processing import VideoProcesser, FrameProcesser, get_answer

from multiprocessing import Process
from collections import deque

import cv2
import os
import numpy as np


class State:
    def __init__(self):
        self.mode = 0
        self.file_name = ''
        self.file_url = ''
        self.is_ready = False

        self.emotions = {
            -1: 'none',
            0: 'angry',
            1: 'disgust',
            2: 'fear',
            3: 'happy',
            4: 'sad',
            5: 'surprise',
            6: 'neutral',
            7: 'noface',
        }

        self.final_video_emotion = self.emotions[-1]

    def set_mode(self, json_data):
        self.is_rt_processing = False
        self.mode = json_data['mode']
        if self.mode == 21:
            model = Deep_Emotion()
            model.to('cpu')
            model.load_state_dict(
                torch.load("/home/igor/code/EmotionRecognition/ml/weights.pt", map_location=torch.device('cpu')))
            model.eval()

            transformation = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
            self.processor = FrameProcesser("one", model, preprocessor=lambda image: transformation(
                cv2.resize(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), (48, 48))).float().unsqueeze(0))

            self.is_rt_processing = True
            self.q_frames = deque()
            self.q_emotions = deque()

            p = Process(target=self.rt_frame_processing)
            p.start()

    def rt_frame_processing(self):

        while self.is_rt_processing:
            if not self.q_frames:
                continue
            frame = np.array(self.q_frames.popleft().split()).reshape((800, 500, 3))
            print(frame.shape, frame[0])
            emotion = get_answer(self.processor.run(frame))
            print("emotion {}" % emotion)
            self.q_emotions.append(emotion)

    def processing_first_mode(self):
        print("YAHOOO")
        path = '/home/igor/code/EmotionRecognition/EmotionRecognition/media'
        model = Deep_Emotion()
        model.to('cpu')
        model.load_state_dict(
            torch.load("/home/igor/code/EmotionRecognition/ml/weights.pt", map_location=torch.device('cpu'))
        )
        model.eval()

        processer = VideoProcesser(model, "emotion", 7)
        outp = processer.process(os.path.join(path, self.file_name))
        self.is_ready = True
        self.final_video_emotion = outp
