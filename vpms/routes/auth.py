from functools import wraps
from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
from databases.mysql import mysql_database
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('home.home'))
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if username and password:
            try:
                connection = mysql_database()
                sql = ('SELECT u.user_id, u.username, u.password, r.role_name FROM users u JOIN roles r ON u.role_id = r.role_id WHERE u.username = %s')
                user = connection.select_one(sql, username)
                if user and check_password_hash(user.get('password'), password):
                    session['user_id'] = user.get('user_id')
                    session['username'] = user.get('username')
                    session['role_name'] = user.get('role_name')
                    print(session)
                    return jsonify({'status': 'ok',
                                    'message': 'เข้าสู่ระบบสำเร็จ'})
                else:
                    return jsonify({'status': 'error',
                                    'message': 'ชื่อผู้ใช้งานหรือรหัสผ่านไม่ถูกต้อง'})
            except Exception as e:
                print(e)
                return jsonify({'status': 'error',
                                'message': 'เข้าสู่ระบบไม่สำเร็จ'})
        else:
            return jsonify({'status': 'error',
                            'message': 'กรุณากรอกข้อมูลให้ครบถ้วน'})
    else:
        return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if username and password:
            try:
                connection = mysql_database()
                sql = ('SELECT u.username FROM users u WHERE u.username = %s')
                result_username = connection.select_one(sql, username)
                if result_username:
                    return jsonify({'status': 'error',
                                    'message': 'ชื่อผู้ใช้งานซ้ำกับในระบบ'})
                else:
                    sql = ('SELECT r.role_id FROM roles r WHERE r.role_name = %s')
                    result_role_id = connection.select_one(sql, 'user')
                    sql = ('INSERT INTO users (username, password, role_id) VALUES (%s, %s, %s)')
                    connection.insert(sql, (username, generate_password_hash(password), result_role_id.get('role_id')))
                    return jsonify({'status': 'ok',
                                    'message': 'สมัครสมาชิกสำเร็จ'})
            except Exception as e:
                print(e)
                return jsonify({'status': 'error',
                                'message': 'สมัครสมาชิกไม่สำเร็จ'})
        else:
            return jsonify({'status': 'error',
                            'message': 'กรุณากรอกข้อมูลให้ครบถ้วน'})
    else:
        return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('home.home'))