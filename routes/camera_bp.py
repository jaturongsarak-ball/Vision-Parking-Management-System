from flask import Blueprint, jsonify, request
from system.camera import camera as camera_class
import database.mysql as mysql

camera_bp = Blueprint('camera_bp', __name__)

camera_list = {}

@camera_bp.route('/')
def camera_index():
    return 'Welcome Home Camera'

@camera_bp.route('/toggle', methods=["POST"])
def toggle_camera():
    data = request.get_json()
    source = data.get("source")

    if source is not None:
        if source not in camera_list:
            fetch_camera_sql = 'select * from camera where source = %s'
            result_camera = mysql.execute_query(fetch_camera_sql, (source))
            if result_camera:
                camera_list[source] = camera_class(result_camera[0]['source'], result_camera[0]['name'], result_camera[0]['role'])
                print('รายชื่อกล้อง', camera_list)
                return jsonify({'message': 'เปิดกล้องสำเร็จ'})
            else:
                return jsonify({'message': 'เกิดข้อผิดพลาดในการเปิดกล้อง'})
        else:
            del camera_list[source]
            print('รายชื่อกล้อง', camera_list)
            return jsonify({'message': 'ปิดกล้องสำเร็จ'})
    else:
        return jsonify({'message': 'ข้อมูลกล้องไม่ถูกต้อง'})

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
                    return jsonify({'message': 'เปิดกล้องทั้งหมดสำเร็จ'})
                else:
                    return jsonify({'message': f'เปิดกล้องทั้งไม่สำเร็จ {error} ตัว'})
            else:
                return jsonify({'message': 'ไม่พบข้อมูลกล้อง'})
        if action == 'off':
            for source in list(camera_list.keys()):
                del camera_list[source]
            print('รายชื่อกล้อง', camera_list)
            return jsonify({'message': 'ปิดใช้งานกล้องทั้งหมดสำเร็จ'})
        else:
            return jsonify({'message': 'เกิดข้อผิดพลาดในการเปิดกล้อง'})

    else:
        return jsonify({'message': 'เกิดข้อผิดพลาดในการเปิดกล้อง'})

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
            add_camera_sql = 'insert into camera (source, name, role) VALUES (%s, %s, %s)'
            result_add_camera = mysql.execute_query(add_camera_sql, (source, name, role))
            if result_add_camera:
                return jsonify({'message': 'เพิ่มกล้องสำเร็จ'})
            else:
                return jsonify({'message': 'เกิดข้อผิดพลาดในการเพิ่มกล้อง'})
        else:
            return jsonify({'message': 'มีข้อมูลกล้องนี้อยู่แแล้ว'})
    else:
        return jsonify({'message': 'เกิดข้อผิดพลาดในการเพิ่มกล้อง'})

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
            if result_camera[0]['name'] == name and result_camera[0]['role'] == role:
                return jsonify({'message': 'ไม่มีการเปลี่ยนแปลงข้อมูล'})
            else:
                update_camera_sql = 'update camera set name = %s, role = %s where source = %s'
                result_update_camera = mysql.execute_query(update_camera_sql, (name, role, source))
                if result_update_camera:
                    return jsonify({'message': 'แก้ไขข้อมูลกล้องสำเร็จ'})
                else:
                    return jsonify({'message': 'แก้ไขข้อมูลกล้องไม่สำเร็จ'})
        else:
            return jsonify({'message': 'ไม่พบกล้องที่ระบุ'})
    else:
        return jsonify({'message': 'เกิดข้อผิดพลาด'})

@camera_bp.route('/delete', methods=["POST"])
def delete_camera():
    data = request.get_json()
    source = data.get('source')
    
    if source is not None:
        delete_camera_sql = 'delete from camera where source = %s'
        result_delete_camera = mysql.execute_query(delete_camera_sql, (source))
        if result_delete_camera:
            return jsonify({'message': 'ลบกล้องสำเร็จ'})
        else:
            return jsonify({'message': 'เกิดข้อผิดพลาดในการลบกล้อง'})
    else:
        return jsonify({'message': 'เกิดข้อผิดพลาดในการลบกล้อง'})