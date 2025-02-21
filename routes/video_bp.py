import base64
from datetime import datetime
import os
import re
import cv2
from flask import Blueprint, render_template, request, send_file, url_for
import database.mysql as mysql

video_bp = Blueprint('video_bp', __name__)

def check_file():
    fetch_video_sql = 'SELECT * FROM video'
    result_video = mysql.execute_query(fetch_video_sql)
    
    existing_video_paths = {video['file_path'] for video in result_video}

    for video in result_video:
        file_path = video['file_path']
        video_full_path = f'video/{file_path}'

        if os.path.exists(video_full_path):
            cap = cv2.VideoCapture(video_full_path)
            if not cap.isOpened():
                os.remove(video_full_path)
                delete_video_sql = 'DELETE FROM video WHERE id = %s'
                mysql.execute_query(delete_video_sql, (video['id']))
            cap.release()
        else:
            delete_video_sql = 'DELETE FROM video WHERE id = %s'
            mysql.execute_query(delete_video_sql, (video['id']))

    file_in_directory = {'parking', 'entrance', 'exit'}
    for file in file_in_directory:
        dir_path = f'video/{file}'
        if os.path.exists(dir_path):
            video_files = os.listdir(dir_path)
            for video_file in video_files:
                full_video_path = f'{file}/{video_file}'
                if full_video_path not in existing_video_paths:
                    try:
                        os.remove(f'{dir_path}/{video_file}')
                    except Exception as e:
                        continue

check_file()

@video_bp.route('/')
def search_videos():
    role = request.args.get('role', 'all')
    name = request.args.get('name', '')
    date = request.args.get('date', '')
    
    try:
        page = int(request.args.get('page', 1))
        if page < 1:
            page = 1
    except Exception as e:
        page = 1

    limit = 10
    offset = (page - 1) * limit

    search_video_sql = 'select * from video where 1=1'
    params = []

    if role and role != 'all':
        search_video_sql += ' and file_path like %s'
        params.append(f'{role}%')

    if name:
        search_video_sql += ' and file_path like %s'
        params.append(f'%{name}%')

    if date:
        search_video_sql += ' and file_path like %s'
        params.append(f'%{date}%')

    search_video_sql += ' order by id desc limit %s offset %s'
    params.extend([limit, offset])

    result_search_video = mysql.execute_query(search_video_sql, params)

    total_count_sql = 'select count(*) from video where 1=1'
    total_count_params = []

    if role and role != 'all':
        total_count_sql += ' and file_path like %s'
        total_count_params.append(f'{role}%')

    if name:
        total_count_sql += ' and file_path like %s'
        total_count_params.append(f'%{name}%')

    if date:
        total_count_sql += ' and file_path like %s'
        total_count_params.append(f'%{date}%')

    total_count_result = mysql.execute_query(total_count_sql, total_count_params)
    total_results = total_count_result[0]['count(*)'] if total_count_result else 0
    total_pages = (total_results + limit - 1) // limit

    if result_search_video:
        for video in result_search_video:
            file_path = video['file_path']

            match = re.search(r'^([^/]+)/([^/]+) (\d{4}-\d{2}-\d{2}) ', file_path)
            if match:
                video['role'] = match.group(1)
                video['name'] = match.group(2)

            match = re.search(r' (\d{4}-\d{2}-\d{2}) (\d{2}-\d{2}-\d{2})', file_path)
            if match:
                raw_date = match.group(1)
                formatted_date = datetime.strptime(raw_date, '%Y-%m-%d').strftime('%d-%m-%Y')
                video['date'] = formatted_date

                raw_time = match.group(2)
                formatted_time = raw_time.replace('-', ':')
                video['time'] = formatted_time

            cap = cv2.VideoCapture(f'video/{file_path}')
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    ret, buffer = cv2.imencode('.jpg', frame)
                    video['thumbnail'] = f'data:image/jpeg;base64,{base64.b64encode(buffer).decode('utf-8')}'
            else:
                video['thumbnail'] = None
            cap.release()

            video['video_url'] = url_for('video_bp.send_video') + f'?file_path={file_path}'

        return render_template('video.html', video_data=result_search_video, page=page, total_pages=total_pages)
    else:
        return render_template('video.html', video_data=[], page=page, total_pages=total_pages)

@video_bp.route('/send_video')
def send_video():
    file_path = request.args.get('file_path')

    if file_path and os.path.exists(f'video/{file_path}'):
        return send_file(f'video/{file_path}', mimetype='video/mp4')
    else:
        return None