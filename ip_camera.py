import cv2

# ใส่ URL ของ IP Camera (ต้องตรวจสอบว่าใช้โปรโตคอลที่ถูกต้อง เช่น rtsp หรือ http)
ip_camera_url = "rtsp://username:password@ip_address:554/cam/realmonitor?channel=1&subtype=0"

# เปิดการเชื่อมต่อกับกล้อง
cap = cv2.VideoCapture(ip_camera_url)

if not cap.isOpened():
    print("ไม่สามารถเชื่อมต่อกับ IP Camera ได้")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("ไม่สามารถอ่านเฟรมจากกล้องได้")
        break

    cv2.imshow("IP Camera Stream", frame)

    # กด 'q' เพื่อออกจากโปรแกรม
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ปิดการเชื่อมต่อ
cap.release()
cv2.destroyAllWindows()