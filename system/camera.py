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
                cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
            else:
                cap = cv2.VideoCapture(source, cv2.CAP_FFMPEG)
        return cap

        
    def update_frame(self):
        target_fps = 30
        frame_time = 1.0 / target_fps
        while self.running:
            start_time = time.time()

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

            elapsed_time = time.time() - start_time
            sleep_time = max(0, frame_time - elapsed_time)
            time.sleep(sleep_time)

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
                        prev_x, prev_y, old_frame = self.object_positions[obj_id]
                        movement = np.linalg.norm([center_x - prev_x, center_y - prev_y])
                        if movement < 1:
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
                        self.object_positions[obj_id] = (center_x, center_y, old_frame)
                    else:
                        self.object_positions[obj_id] = (center_x, center_y, frame)
                    frame = self.put_thai_text(frame, f'{license_plate_text}', (x1, y1  - 45), color=(255, 255, 255))
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        for obj_id in list(self.current_obj_ocr.keys()):
            if obj_id not in active_obj_ids:
                ocr_texts = self.current_obj_ocr[obj_id]
                if ocr_texts:
                    text_counter = Counter(ocr_texts)
                    most_common_text, count = text_counter.most_common(1)[0]
                    _, _, old_frame = self.object_positions[obj_id]
                    datetime_crop = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                    most_common_text = most_common_text.replace(' ', '')
                    os.makedirs(f'image/{self.role}', exist_ok=True)
                    image_filename = f'{most_common_text} {datetime_crop}.jpg'

                    if self.role == 'entrance':
                        check_parking_stat_sql = 'select * from parking_stat where plate_number = %s and datetime_exit is null'
                        check_parking_stat = mysql.execute_query(check_parking_stat_sql, (most_common_text))
                        if not check_parking_stat:
                            parking_stat_insert_sql = 'insert into parking_stat (plate_number, 	image_entrance, datetime_entrance) values (%s, %s, %s)'
                            result_insert = mysql.execute_query(parking_stat_insert_sql, (most_common_text, image_filename, datetime_crop))
                            if result_insert:
                                cv2.imwrite(f'image/{self.role}/{image_filename}', old_frame)
                    if self.role == 'exit':
                        check_parking_stat_sql = 'select * from parking_stat where plate_number = %s and datetime_exit is null'
                        check_parking_stat = mysql.execute_query(check_parking_stat_sql, (most_common_text))
                        if check_parking_stat:
                            parking_stat_update_sql = 'update parking_stat set image_exit = %s, datetime_exit = %s where plate_number = %s and datetime_exit is null'
                            result_update = mysql.execute_query(parking_stat_update_sql, (image_filename, datetime_crop, most_common_text))   
                            if result_update:
                                cv2.imwrite(f'image/{self.role}/{image_filename}', old_frame)

                del self.current_obj_ocr[obj_id]

        for obj_id in list(self.object_positions.keys()):
            if obj_id not in active_obj_ids:
                del self.object_positions[obj_id]

        return frame

    def process_parking(self, frame):
        results = self.model.predict(frame, conf=0.6, verbose=False)

        def is_parking(space, x1, y1, x2, y2):
            return x1 <= space['x'] <= x2 and y1 <= space['y'] <= y2

        occupied_spaces = set()
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])

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

        fps =  30
        frame_duration = 1 / fps
        video__duration = 300

        while self.running:
            start_time = time.time()
            
            filename = f'{self.name} {time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(start_time))}.mp4'
            output_video_path = f'{save_video_path}/{filename}'

            fourcc = cv2.VideoWriter_fourcc(*'avc1')

            frame_size = (int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                          int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

            video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, frame_size)

            while self.running:
                start_time_ = time.time()
                frame = self.get_frame()
                if frame is not None:
                    video_writer.write(frame)

                elapsed_time = time.time() - start_time
                if elapsed_time >= video__duration:
                    break
                else:
                    elapsed_time_ = time.time() - start_time_
                    sleep_time = max(0, frame_duration - elapsed_time_)
                    time.sleep(sleep_time)

            video_writer.release()

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
