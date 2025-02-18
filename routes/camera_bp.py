from flask import Blueprint, jsonify, request
from system.camera import camera as camera_class

camera_bp = Blueprint('camera_bp', __name__)

camera_list = {}

@camera_bp.route('/')
def camera():
    return 'Hello from Blueprint!'

@camera_bp.route('/toggle', methods=["POST"])
def toggle():
    data = request.get_json()
    source = data.get("source")

    if source is not None:

        if source not in camera_list:
            camera_list[source] = camera_class(source)
            print(camera_list)
            return jsonify({'message': 'เปิดกล้องสำเร็จ'})
        else:
            del camera_list[source]
            print(camera_list)
            return jsonify({'message': 'ปิดกล้องสำเร็จ'})
    
    else:
        return jsonify({'message': 'ข้อมูลกล้องไม่ถูกต้อง'})