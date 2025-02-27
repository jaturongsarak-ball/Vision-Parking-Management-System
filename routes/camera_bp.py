import time
import cv2
from flask import Blueprint, Response, jsonify, render_template, request
from system.camera import camera as camera_class
import database.mysql as mysql

camera_bp = Blueprint('camera_bp', __name__)

camera_list = {}

@camera_bp.route('/')
def camera_index():
    fetch_camera_sql = 'select * from camera'
    result_camera = mysql.execute_query(fetch_camera_sql)
    if result_camera:
        for camera in result_camera:
                    if camera['source'] in camera_list:
                        camera['status'] = 'on'
                    else:
                        camera['status'] = 'off'
        return render_template('camera.html', camera_data = result_camera)
    else:
        return render_template('camera.html', camera_data = [])

@camera_bp.route('/toggle', methods=["POST"])
def toggle_camera():
    data = request.get_json()
    source = data.get("source")

    if source is not None:
        if source not in camera_list:
            fetch_camera_sql = 'select * from camera where source = %s'
            result_camera = mysql.execute_query(fetch_camera_sql, (source))
            if result_camera:
                try:
                    camera_list[source] = camera_class(result_camera[0]['source'], result_camera[0]['name'], result_camera[0]['role'])
                    print('รายชื่อกล้อง', camera_list)
                    return jsonify({'status': 'success', 'message': 'เปิดกล้องสำเร็จ'})
                except Exception as e:
                    print('รายชื่อกล้อง', camera_list)
                    return jsonify({'status': 'error', 'message': 'เกิดข้อผิดพลาดในการเปิดกล้อง'})
            else:
                return jsonify({'status': 'error', 'message': 'เกิดข้อผิดพลาดในการเปิดกล้อง'})
        else:
            camera_list[source].stop()
            del camera_list[source]
            print('รายชื่อกล้อง', camera_list)
            return jsonify({'status': 'success', 'message': 'ปิดกล้องสำเร็จ'})
    else:
        return jsonify({'status': 'error', 'message': 'ข้อมูลกล้องไม่ถูกต้อง'})

@camera_bp.route('/toggle_all', methods=["POST"])
def toggle_all_camera():
    data = request.get_json()
    action = data.get("action")
    if action is not None:

        if action == 'on':
            fetch_camera_list = 'select * from camera'
            result_camera_list = mysql.execute_query(fetch_camera_list)
            if result_camera_list:
                error = 0
                for list_camera in result_camera_list:
                    if list_camera['source'] not in camera_list:
                        try:
                            camera_list[list_camera['source']] = camera_class(list_camera['source'], list_camera['name'], list_camera['role'])
                        except Exception as e:
                            error += 1
                print('รายชื่อกล้อง', camera_list)
                if error < 1:
                    return jsonify({'status': 'success', 'message': 'เปิดกล้องทั้งหมดสำเร็จ'})
                else:
                    return jsonify({'status': 'warning', 'message': f'เปิดกล้องทั้งไม่สำเร็จ {error} ตัว'})
            else:
                return jsonify({'status': 'error', 'message': 'ไม่พบข้อมูลกล้อง'})
        if action == 'off':
            for source in list(camera_list.keys()):
                camera_list[source].stop()
                del camera_list[source]
            print('รายชื่อกล้อง', camera_list)
            return jsonify({'status': 'success', 'message': 'ปิดใช้งานกล้องทั้งหมดสำเร็จ'})
        else:
            return jsonify({'status': 'error', 'message': 'เกิดข้อผิดพลาดในการเปิดกล้อง'})

    else:
        return jsonify({'status': 'error', 'message': 'เกิดข้อผิดพลาดในการเปิดกล้อง'})

def generate_frame(source):
    if source not in camera_list:
        yield (b'--frame\r\n'
               b'Content-Type: text/plain\r\n\r\n' + b"Source not found!\r\n")
        return
    while True:
        time.sleep(0.03)
        try:
            frame = camera_list[source].get_frame()
            if frame is None:
                yield (b'--frame\r\n'
                    b'Content-Type: text/plain\r\n\r\n' + b"Unable to retrieve frame!\r\n")
                continue
            
            ret, buffer = cv2.imencode('.jpg', frame)
            if ret:
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                yield (b'--frame\r\n'
                    b'Content-Type: text/plain\r\n\r\n' + b"Failed to encode frame as JPEG\r\n")
        except Exception as e:
            yield (b'--frame\r\n'
                b'Content-Type: text/plain\r\n\r\n' + b"Source not found!\r\n")
            return

@camera_bp.route('/thumbnail')
def thumbnail():
    source = request.args.get('source')
    frame = None
    while frame is None:
        frame = camera_list[source].get_frame()
        if frame is None:
            continue
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
    return Response(frame, mimetype='image/jpeg')

@camera_bp.route('/live')
def camera_live():
    source = request.args.get('source')
    return Response(generate_frame(source), mimetype='multipart/x-mixed-replace; boundary=frame')

@camera_bp.route('/parking_stream_live')
def camera_stream_live():
    source = request.args.get('source')
    return render_template('camera_live.html', source=source)

@camera_bp.route('/parking_space')
def camera_parking_space():
    source = request.args.get('source')
    fetch_parking_space_sql = 'select name, x, y, source from parking_space where source = %s'
    result_parking_space = mysql.execute_query(fetch_parking_space_sql, (source))
    return render_template('camera_parking_space.html', source=source, parking_space=result_parking_space)

@camera_bp.route('/save_parking_space', methods=["POST"])
def save_parking_space():
    source = request.args.get('source')
    data = request.get_json()
    if data:
        delete_parking_space_sql = 'delete from parking_space where source = %s'
        mysql.execute_query(delete_parking_space_sql, (source))
        for parking_space in data:
            add_parking_space = 'insert into parking_space (name, x, y, source, status) values (%s, %s, %s, %s, %s)'
            mysql.execute_query(add_parking_space, (parking_space['name'], parking_space['x'], parking_space['y'], source, 'available'))
        camera_list[source].update_parking_space()
        return jsonify({'status': 'success', 'message': 'บันทึกข้อมูลสำเร็จ'})
    else:
        delete_parking_space_sql = 'delete from parking_space where source = %s'
        mysql.execute_query(delete_parking_space_sql, (source))
        camera_list[source].update_parking_space()
        return jsonify({'status': 'success', 'message': 'บันทึกข้อมูลสำเร็จ'})


@camera_bp.route('/add', methods=["POST"])
def add_camera():
    data = request.get_json()
    source = data.get('source')
    name = data.get('name')
    role = data.get('role')

    if None not in [source, name, role]:
        fetch_camera_sql = 'select * from camera where source = %s or name = %s'
        result_camera = mysql.execute_query(fetch_camera_sql, (source, name))
        if not result_camera:
            add_camera_sql = 'insert into camera (source, name, role) values (%s, %s, %s)'
            result_add_camera = mysql.execute_query(add_camera_sql, (source, name, role))
            if result_add_camera:
                return jsonify({'status': 'success', 'message': 'เพิ่มกล้องสำเร็จ'})
            else:
                return jsonify({'status': 'error', 'message': 'เกิดข้อผิดพลาดในการเพิ่มกล้อง'})
        else:
            return jsonify({'status': 'error', 'message': 'มีข้อมูลกล้องนี้อยู่แแล้ว'})
    else:
        return jsonify({'status': 'error', 'message': 'เกิดข้อผิดพลาดในการเพิ่มกล้อง'})

@camera_bp.route('/update', methods=["POST"])
def update_camera():
    data = request.get_json()
    source = data.get('source')
    name = data.get('name')
    role = data.get('role')

    if None not in [source, name, role]:
        fetch_camera_sql = 'select * from camera where source = %s or name = %s'
        result_camera = mysql.execute_query(fetch_camera_sql, (source, name))
        if result_camera:
            if result_camera[0]['source'] == source and result_camera[0]['name'] == name and result_camera[0]['role'] == role:
                return jsonify({'status': 'warning', 'message': 'ไม่มีการเปลี่ยนแปลงข้อมูล'})
            else:
                update_camera_sql = 'update camera set source = %s, name = %s, role = %s where id = %s'
                result_update_camera = mysql.execute_query(update_camera_sql, (source, name, role, result_camera[0]['id']))
                if result_update_camera:
                    if role != 'parking' and result_camera[0]['role'] == 'parking':
                        delete_parking_space_sql = 'delete from parking_space where source = %s'
                        mysql.execute_query(delete_parking_space_sql, (source))
                    return jsonify({'status': 'success', 'message': 'แก้ไขข้อมูลกล้องสำเร็จ'})
                else:
                    return jsonify({'status': 'error', 'message': 'แก้ไขข้อมูลกล้องไม่สำเร็จ'})
        else:
            return jsonify({'status': 'error', 'message': 'ไม่พบกล้องที่ระบุ'})
    else:
        return jsonify({'status': 'error', 'message': 'เกิดข้อผิดพลาด'})

@camera_bp.route('/delete', methods=["POST"])
def delete_camera():
    data = request.get_json()
    source = data.get('source')
    
    if source is not None:
        delete_camera_sql = 'delete from camera where source = %s'
        result_delete_camera = mysql.execute_query(delete_camera_sql, (source))
        if result_delete_camera:
            return jsonify({'status': 'success', 'message': 'ลบกล้องสำเร็จ'})
        else:
            return jsonify({'status': 'error', 'message': 'เกิดข้อผิดพลาดในการลบกล้อง'})
    else:
        return jsonify({'status': 'error', 'message': 'เกิดข้อผิดพลาดในการลบกล้อง'})