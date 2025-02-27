from datetime import datetime
import os
import subprocess
import threading
import time
import cv2
from ultralytics import YOLO
import database.mysql as mysql
import numpy as np
from PIL import Image, ImageDraw, ImageFont

class camera:
    def __init__(self, source, name, role):
        self.source = source
        self.name = name
        self.role = role
        self.parking_space = None
        if role == 'parking':
            self.model = YOLO('system/car_model.pt', verbose=False)
            self.update_parking_space()
        elif role == 'entrance' or role == 'exit':
            self.model = YOLO('system/license_plate_model.pt', verbose=False)
        else:
            raise ValueError(f'ไม่สามารถเปิดกล้องได้')

        self.capture = self.open_camera(source)
        if not self.capture.isOpened():
            raise ValueError(f'ไม่สามารถเปิดกล้องได้')
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 10)
        # self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        # self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        # self.capture.set(cv2.CAP_PROP_FPS, 30)
        
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
            return cv2.VideoCapture(source)

        
    def update_frame(self):
        while self.running:
            ret, frame = self.capture.read()
            if ret:
                with self.lock:
                    if self.role == 'parking':
                        frame = self.process_parking(frame)
                    elif self.role == 'entrance' or self.role == 'exit':
                        frame = self.process_entrance_exit(frame)
                    self.frame = frame
            else:
                self.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def process_entrance_exit(self, frame):
        results = self.model.track(frame, tracker='bytetrack.yaml', persist=True, conf=0.6, verbose=False)

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = box.conf[0]
                # object_id = box.id[0]
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 1)
                frame = self.put_thai_text(frame, f'{confidence*100:.2f}%', (x1, y1 - 25), color=(255, 255, 255))

        return frame

    def process_parking(self, frame):
        results = self.model.track(frame, tracker='bytetrack.yaml', persist=True, conf=0.6, verbose=False)

        def is_parking(space, x1, y1, x2, y2):
            return x1 <= space['x'] <= x2 and y1 <= space['y'] <= y2

        occupied_spaces = set()
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = box.conf[0]
                # object_id = box.id[0]
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 1)
                frame = self.put_thai_text(frame, f'{confidence*100:.2f}%', (x1, y1 - 25), color=(255, 255, 255))

                for space in self.parking_space:
                    if is_parking(space, x1, y1, x2, y2):
                        occupied_spaces.add(space['id'])

        for space in self.parking_space:
            color = (0, 0, 255) if space['id'] in occupied_spaces else (0, 255, 0)
            frame = cv2.circle(frame, (space['x'], space['y']), 5, color, -1)
            status = 'occupied' if space['id'] in occupied_spaces else 'available'
            status_update_sql = 'update parking_space set status = %s where id = %s'
            mysql.execute_query(status_update_sql, (status, space['id']))

        self.update_parking_space()
        return frame


    def get_frame(self):
        with self.lock:
            return self.frame

    def record(self):
        save_video_path = f'video/{self.role}'
        os.makedirs(save_video_path, exist_ok=True)

        fps = fps = self.capture.get(cv2.CAP_PROP_FPS)
        frame_duration = 1 / fps
        video__duration = 300

        while self.running:
            start_time = time.time()
            
            filename = f'{self.name} {time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(start_time))}.mp4'
            input_video_path = f'{save_video_path}/before_{filename}'
            output_video_path = f'{save_video_path}/{filename}'

            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            frame_size = (int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                          int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

            video_writer = cv2.VideoWriter(input_video_path, fourcc, fps, frame_size)

            while self.running:
                frame = self.get_frame()
                if frame is not None:
                    video_writer.write(frame)

                elapsed_time = time.time() - start_time
                if elapsed_time >= video__duration:
                    break

                time.sleep(frame_duration)

            video_writer.release()

            ffmpeg_cmd = [
                "ffmpeg", "-y",
                "-i", input_video_path,
                "-vcodec", "libx264",
                "-crf", "18",
                "-preset", "slow",
                "-pix_fmt", "yuv420p",
                output_video_path
            ]

            subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            os.remove(input_video_path)

            save_video_sql = 'insert into video (file_path) values (%s)'
            mysql.execute_query(save_video_sql, (f'{self.role}/{filename}'))

    def update_parking_space(self):
        update_parking_space_sql = 'select * from parking_space where source = %s'
        self.parking_space = mysql.execute_query(update_parking_space_sql, (self.source))

    def stop(self):
        self.running = False
        self.thread.join()
        self.record_thread.join()
        self.capture.release()

    def put_thai_text(self, image, text, position, font_path='system/Pridi.ttf', font_size=20, color=(0, 0, 255)):
        image_pil = Image.fromarray(image)
        draw = ImageDraw.Draw(image_pil)
        font = ImageFont.truetype(font_path, font_size)
        draw.text(position, text, font=font, fill=color)
        return np.array(image_pil)
