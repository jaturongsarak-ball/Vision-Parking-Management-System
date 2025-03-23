import os
from flask import Blueprint, render_template, request, send_file
import database.mysql as mysql
from routes.auth_bp import admin_required, login_required

parking_stat_bp = Blueprint('parking_stat_bp', __name__)

video_bp = Blueprint('video_bp', __name__)

def check_file():
    fetch_parking_stat_sql = 'SELECT * FROM parking_stat'
    result_parking_stat = mysql.execute_query(fetch_parking_stat_sql)
    
    existing_parking_stat_paths = {
        parking_stat['image_entrance'] for parking_stat in result_parking_stat
    }.union({
        parking_stat['image_exit'] for parking_stat in result_parking_stat
    })

    directories = ['image/entrance', 'image/exit']

    for dir_path in directories:
        if os.path.exists(dir_path):
            for image_file in os.listdir(dir_path):
                image_path = f'{image_file}'
                
                if image_path not in existing_parking_stat_paths:
                    try:
                        os.remove(f'{dir_path}/{image_path}')
                    except Exception as e:
                        continue

@parking_stat_bp.route('/')
@login_required
@admin_required
def parking_stat():
    # check_file()
        
    date_start = request.args.get('date_start', '')
    date_end = request.args.get('date_end', '')

    try:
        page = int(request.args.get('page', 1))
        if page < 1:
            page = 1
    except Exception as e:
        page = 1

    limit = 10
    offset = (page - 1) * limit

    fetch_parking_stat_sql = 'select * from parking_stat where 1=1'
    params = []

    if date_start:
        fetch_parking_stat_sql += ' and datetime_entrance >= %s'
        params.append(f'{date_start} 00:00:00')

    if date_end:
        fetch_parking_stat_sql += ' and datetime_entrance <= %s'
        params.append(f'{date_end} 23:59:59')

    fetch_parking_stat_sql += ' order by id desc limit %s offset %s'
    params.extend([limit, offset])

    result_parking_stat = mysql.execute_query(fetch_parking_stat_sql, params)

    total_count_sql = 'select count(*) from parking_stat where 1=1'
    total_count_params = []

    if date_start:
        total_count_sql += ' and datetime_entrance >= %s'
        total_count_params.append(f'{date_start} 00:00:00')

    if date_end:
        total_count_sql += ' and datetime_entrance <= %s'
        total_count_params.append(f'{date_end} 23:59:59')

    total_count_result = mysql.execute_query(total_count_sql, total_count_params)
    total_count = total_count_result[0]['count(*)'] if total_count_result else 0
    total_pages = (total_count + limit - 1) // limit

    start_page = max(1, page - 4)
    end_page = min(total_pages, start_page + 9)

    fetch_stat = '''select count(*) as total_cars,
                        ROUND(avg(TIMESTAMPDIFF(MINUTE, datetime_entrance, datetime_exit)), 0) AS avg_parking_duration,
                        ROUND(max(TIMESTAMPDIFF(MINUTE, datetime_entrance, datetime_exit)), 0) AS max_parking_duration,
                        ROUND(min(TIMESTAMPDIFF(MINUTE, datetime_entrance, datetime_exit)), 0) AS min_parking_duration
                    from parking_stat where 1=1'''
    
    params = []

    if date_start:
        fetch_stat += ' and datetime_entrance >= %s'
        params.append(f'{date_start} 00:00:00')

    if date_end:
        fetch_stat += ' and datetime_entrance <= %s'
        params.append(f'{date_end} 23:59:59')

    parking_stat_result = mysql.execute_query(fetch_stat, params)

    time_slots_sql = '''select hour(datetime_entrance) as hour,
                            count(*) as cars_in_hour
                        from parking_stat where 1=1'''
    
    params = []

    if date_start:
        time_slots_sql += ' and datetime_entrance >= %s'
        params.append(f'{date_start} 00:00:00')

    if date_end:
        time_slots_sql += ' and datetime_entrance <= %s'
        params.append(f'{date_end} 23:59:59')

    time_slots_sql += ' group by hour(datetime_entrance) order by hour'
    time_slots_result = mysql.execute_query(time_slots_sql, params)

    return render_template('parking_stat.html',
                            parking_data=result_parking_stat if result_parking_stat else [],
                            time_slots=time_slots_result if time_slots_result else [],
                            parking_stat=parking_stat_result[0] if parking_stat_result else {},
                            page=page, total_pages=total_pages,
                            start_page=start_page,
                            end_page=end_page)

@parking_stat_bp.route('/get_image', methods=['GET'])
@login_required
@admin_required
def get_image():
    image_path = request.args.get('path', '')

    if not image_path or not os.path.exists(image_path):
        return {"error": "File not found"}, 404

    return send_file(image_path, mimetype='image/jpeg')