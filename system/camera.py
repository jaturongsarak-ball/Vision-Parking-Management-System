import os
import threading
import time
import cv2
import database.mysql as mysql

class camera:
    def __init__(self, source, name, role):
        self.source = source
        self.name = name
        self.role = role

        self.capture = self.open_camera(source)
        if not self.capture.isOpened():
            raise ValueError(f'ไม่สามารถเปิดกล้องได้')
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.capture.set(cv2.CAP_PROP_FPS, 30)
        
        self.frame = None
        self.running = True

        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self.update_frame, daemon=True)
        self.thread.start()

        self.record_thread = threading.Thread(target=self.record, daemon=True)
        self.record_thread.start()

    def open_camera(self, source):
        if str(source).isdigit():
            return cv2.VideoCapture(int(source))
        else:
            return cv2.VideoCapture(f'video/demo/{source}')
        
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

    def record(self):
        save_video_path = f'video/{self.role}'
        os.makedirs(save_video_path, exist_ok=True)

        fps = 30
        frame_duration = 1 / fps

        while self.running:
            start_time = time.time()
            
            filename = f'{self.name} {time.strftime("%Y-%m-%d %H-%M-%S", time.localtime(start_time))}.mp4'
            
            fourcc = cv2.VideoWriter_fourcc(*'avc1')
            frame_size = (int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                          int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

            video_writer = cv2.VideoWriter(f'{save_video_path}/{filename}', fourcc, fps, frame_size)

            while self.running:
                frame = self.get_frame()
                if frame is not None:
                    video_writer.write(frame)

                elapsed_time = time.time() - start_time
                if elapsed_time >= 300:
                    break

                time.sleep(frame_duration)

            save_video_sql = 'insert into video (file_path) values (%s)'
            result_save_video = mysql.execute_query(save_video_sql, (f'{self.role}/{filename}'))
            
            if result_save_video:
                video_writer.release()

    def stop(self):
        self.running = False
        self.thread.join()
        self.record_thread.join()
        self.capture.release()
