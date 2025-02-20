import os
import cv2
from flask import Blueprint, jsonify, render_template, request
import database.mysql as mysql

video_bp = Blueprint('video_bp', __name__)

import os
import cv2

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
def video_index():
    fetch_video_sql = 'SELECT * FROM video'
    result_video = mysql.execute_query(fetch_video_sql)
    print(result_video)
    return render_template('video.html')

@video_bp.route('/search')
def search_videos():
    role = request.args.get('role', 'all')
    date = request.args.get('date', '')
    
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1

    search_video_sql = 'select id, file_path from video'
    mysql.execute_query(search_video_sql)
    
    print(role, date, page)
    
    return jsonify({
        'role': role,
        'date': date,
        'page': page,
    })