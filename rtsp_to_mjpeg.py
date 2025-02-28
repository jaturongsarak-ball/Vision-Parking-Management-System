import os
import time
import cv2
from flask import Flask, Response, request

app = Flask(__name__)

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = (
    "rtsp_transport;tcp|timeout;8000|max_delay;800000|fflags;nobuffer|flags;low_delay"
    "|probesize;500000|analyzeduration;250000|thread_queue_size;4096|framedrop;0|skip_frame;default"
    "|flags2;showall|sync;ext|avioflags;direct|reorder_queue_size;16"
)

def generate_frames(rtsp_url):
    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        print(f"❌ ไม่สามารถเชื่อมต่อ RTSP: {rtsp_url}")
        return
    else:
        print(f"✅ เชื่อมต่อกล้องสำเร็จ")

    while True:
        success, frame = cap.read()
        if not success:
            print("⚠️ ไม่สามารถอ่านภาพจาก RTSP stream ได้ กำลังพยายามเชื่อมต่อใหม่...")
            cap.release()
            cap = cv2.VideoCapture(rtsp_url)
            if not cap.isOpened():
                print(f"❌ ไม่สามารถเชื่อมต่อ RTSP: {rtsp_url}")
            else:
                print(f"✅ เชื่อมต่อกล้องสำเร็จ")
            continue

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

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
