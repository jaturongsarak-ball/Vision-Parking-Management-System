from datetime import datetime
import os
import re
import subprocess
import threading
import time
from collections import Counter
import cv2
import requests
from ultralytics import YOLO
import database.mysql as mysql
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import easyocr

class camera:
    def __init__(self, source, name, role):
        self.source = source
        self.name = name
        self.role = role
        self.parking_space = None

        self.capture = self.open_camera(source)
        if not self.capture.isOpened():
            raise ValueError(f'ไม่สามารถเปิดกล้องได้')

        if role == 'parking':
            self.model = YOLO('system/car_model.pt', verbose=False)
            self.update_parking_space()
        elif role == 'entrance' or role == 'exit':
            self.model = YOLO('system/license_plate_model.pt', verbose=False)
            self.reader = easyocr.Reader(['th', 'en'])
            self.object_positions = {}
            self.current_obj_ocr = {}
        else:
            raise ValueError(f'ไม่สามารถเปิดกล้องได้')
        
        self.frame = None
        self.running = True

        self.thread = threading.Thread(target=self.update_frame, daemon=True)
        self.thread.start()

        self.record_thread = threading.Thread(target=self.record, daemon=True)
        self.record_thread.start()

    def open_camera(self, source):
        if str(source).isdigit():
            cap = cv2.VideoCapture(int(source))
        else:
            if 'rtsp' in source:
                url = f'http://localhost:4000/?rtsp_url={source}'
                print('url', url)
                cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
            else:
                cap = cv2.VideoCapture(source, cv2.CAP_FFMPEG)
        return cap

        
    def update_frame(self):
        while self.running:
            ret, frame = self.capture.read()
            if ret:
                if self.role == 'parking':
                    frame = self.process_parking(frame)
                elif self.role == 'entrance' or self.role == 'exit':
                    frame = self.process_entrance_exit(frame)

                vieo_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                frame = self.put_thai_text(frame, vieo_time, (20, 20), color=(255, 255, 255))
                
                self.frame = frame
            else:
                self.capture.release()
                self.capture = self.open_camera(self.source)

    def process_entrance_exit(self, frame):
        results = self.model.track(frame, tracker='bytetrack.yaml', persist=True, conf=0.6, verbose=False)
        active_obj_ids = set()
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2
                license_plate_text = ''
                color = (0, 255, 0)
                obj_id = int(box.id[0]) if box.id is not None else None
                if obj_id:
                    active_obj_ids.add(obj_id)
                    if obj_id in self.object_positions:
                        prev_x, prev_y, old_frame, old_datetime = self.object_positions[obj_id]
                        movement = np.linalg.norm([center_x - prev_x, center_y - prev_y])
                        if movement < 0.5:
                            cropped_img = frame[y1:y2, x1:x2]
                            gray_cropped_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
                            ocr_results = self.reader.readtext(gray_cropped_img)
                            if ocr_results:
                                for (bbox, text, ocr_conf) in ocr_results:
                                    if ocr_conf >= 0.5:
                                        license_plate_text += ''.join(re.findall(r'[ก-ฮ๐-๙a-zA-Z0-9]', text)) + " "
                                        if (obj_id not in self.current_obj_ocr) and (license_plate_text):
                                            self.current_obj_ocr[obj_id] = []
                                        if (obj_id in self.current_obj_ocr) and (license_plate_text):
                                            self.current_obj_ocr[obj_id].append(license_plate_text)
                                
                                color = (0, 0, 255)
                        self.object_positions[obj_id] = (center_x, center_y, old_frame, old_datetime)
                    else:
                        datetime_ = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                        self.object_positions[obj_id] = (center_x, center_y, frame, datetime_)
                    frame = self.put_thai_text(frame, f'{license_plate_text}', (x1, y1  - 45), color=(255, 255, 255))
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
        for obj_id in list(self.object_positions.keys()):
            if obj_id not in active_obj_ids:
                del self.object_positions[obj_id]
        for obj_id in list(self.current_obj_ocr.keys()):
            if obj_id not in active_obj_ids:
                ocr_texts = self.current_obj_ocr[obj_id]
                if ocr_texts:
                    text_counter = Counter(ocr_texts)
                    most_common_text, count = text_counter.most_common(1)[0]
                    print(f'ข้อความที่พบบ่อยที่สุด ({count} ครั้ง): {most_common_text}')
                del self.current_obj_ocr[obj_id]

        return frame

    def process_parking(self, frame):
        # results = self.model.track(frame, tracker='bytetrack.yaml', persist=True, conf=0.6, verbose=False)
        results = self.model.predict(frame, conf=0.6, verbose=False)

        def is_parking(space, x1, y1, x2, y2):
            return x1 <= space['x'] <= x2 and y1 <= space['y'] <= y2

        occupied_spaces = set()
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = box.conf[0]
                # if box.id:
                #     object_id = box.id[0]
                # frame = self.put_thai_text(frame, f'{confidence*100:.2f}%', (x1, y1 - 25), color=(255, 255, 255))
                
                color = (0, 255, 0)

                for space in self.parking_space:
                    if is_parking(space, x1, y1, x2, y2):
                        occupied_spaces.add(space['id'])
                        color = (0, 0, 255)
                        break

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        for space in self.parking_space:
            color = (0, 0, 255) if space['id'] in occupied_spaces else (0, 255, 0)
            frame = cv2.circle(frame, (space['x'], space['y']), 5, color, -1)
            status = 'occupied' if space['id'] in occupied_spaces else 'available'
            status_update_sql = 'update parking_space set status = %s where id = %s'
            mysql.execute_query(status_update_sql, (status, space['id']))

        self.update_parking_space()
        return frame


    def get_frame(self):
        return self.frame

    def record(self):
        save_video_path = f'video/{self.role}'
        os.makedirs(save_video_path, exist_ok=True)

        fps =  10
        frame_duration = 1 / fps
        video__duration = 300

        while self.running:
            start_time = time.time()
            
            filename = f'{self.name} {time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(start_time))}.mp4'
            input_video_path = f'{save_video_path}/temp_{filename}'
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

    def put_thai_text(self, image, text, position, font_path='system/Pridi.ttf', font_size=40, color=(0, 0, 255)):
        image_pil = Image.fromarray(image)
        draw = ImageDraw.Draw(image_pil)
        font = ImageFont.truetype(font_path, font_size)
        draw.text(position, text, font=font, fill=color)
        return np.array(image_pil)
