import os
import time
import cv2
from flask import Flask, Response, request

app = Flask(__name__)

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = (
    "rtsp_transport;tcp|timeout;5000|max_delay;0|fflags;nobuffer|flags;low_delay"
    "|probesize;1000000|analyzeduration;500000|thread_queue_size;1024|framedrop;1|skip_frame;nonref"
    "|flags2;showall|sync;ext|avioflags;direct|reorder_queue_size;0"
)

def generate_frames(rtsp_url):
    cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
    if not cap.isOpened():
        print(f"❌ ไม่สามารถเชื่อมต่อ RTSP: {rtsp_url}")
        return
    else:
        print(f"✅ เชื่อมต่อกล้องสำเร็จ")
    
    target_fps = 30
    frame_time = 1.0 / target_fps


    while True:

        start_time = time.time()

        success, frame = cap.read()
        if not success:
            print("⚠️ ไม่สามารถอ่านภาพจาก RTSP stream ได้ กำลังพยายามเชื่อมต่อใหม่...")
            cap.release()
            cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
            if not cap.isOpened():
                print(f"❌ ไม่สามารถเชื่อมต่อ RTSP: {rtsp_url}")
            else:
                print(f"✅ เชื่อมต่อกล้องสำเร็จ")
            continue

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
        elapsed_time = time.time() - start_time
        sleep_time = max(0, frame_time - elapsed_time)
        time.sleep(sleep_time)

@app.route('/', methods=['GET'])
def mjpeg_feed():
    rtsp_url = request.args.get('rtsp_url')
    print(f"🎥 กำลังเชื่อมต่อกล้อง: {rtsp_url}")
    if not rtsp_url:
        return "❌ กรุณาใส่ rtsp_url", 400

    return Response(generate_frames(rtsp_url),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, threaded=True)
