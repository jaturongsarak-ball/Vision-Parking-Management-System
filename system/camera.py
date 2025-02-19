import threading
import cv2

class camera:
    def __init__(self, source, name, role):
        self.source = source
        self.name = name
        self.role = role

        self.capture = self.open_camera(source)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.capture.set(cv2.CAP_PROP_FPS, 30)

        self.frame = None

        self.running = True
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self.update_frame)
        self.thread.start()

    def open_camera(self, source):
        if str(source).isdigit():
            return cv2.VideoCapture(int(source))
        else:
            return cv2.VideoCapture(str(f'video/demo/{source}'))
        
    def update_frame(self):
        while self.running:
            ret, frame = self.capture.read()
            if ret:
                with self.lock:
                    self.frame = frame
            else:
                self.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
    def get_frame(self):
        with self.lock:
            return self.frame

    def stop(self):
        self.running = False
        self.thread.join()
        self.capture.release()