from flask import Blueprint, Response, jsonify, render_template, request
import database.mysql as mysql

parking_bp = Blueprint('parking_bp', __name__)

@parking_bp.route('/', methods=["POST", "GET"])
def parking_index():
    fetch_parking_space = '''select name,
                                count(*) as total,
                                coalesce(sum(case when status = 'occupied' then 1 else 0 end), 0) as occupied,
                                coalesce(sum(case when status = 'available' then 1 else 0 end), 0) as available
                                from parking_space
                                group by name'''
    result_parking_space = mysql.execute_query(fetch_parking_space)
    for space in result_parking_space:
        percentage = space['occupied']/space['total']
        if percentage >= 1:
            space['color'] = 'danger'
        elif percentage >= 0.5:
            space['color'] = 'warning'
        elif percentage < 0.5: 
            space['color'] = 'success'

    if request.method == 'GET':
        return render_template('parking_status.html', parking_status=result_parking_space)
    else :
        return jsonify({'status': 'success', 'message': 'เรียกข้อมูลสำเร็จ', 'parking_status': result_parking_space})