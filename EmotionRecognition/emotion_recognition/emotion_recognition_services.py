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
        }

        self.final_video_emotion = self.emotions[-1]

    def set_mode(self, json_data):
        self.mode = json_data['mode']

        if self.mode == 1:
            self.processing_first_mode()

    def processing_first_mode(self, file_name, file_url):

        # start in thread
        # need get which will use state as data provider
        self.file_name, self.file_url = file_name, file_url

        # if state.is_ready:
        #     send state.data
        # else:
        #     send false




