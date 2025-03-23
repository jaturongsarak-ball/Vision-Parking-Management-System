from functools import wraps
from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
import database.mysql as mysql
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth_bp', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('auth_bp.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'admin' == session['role']:
            return redirect(url_for('home_hp.home'))
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if username and password:
            sql = ('SELECT id, username, password, role FROM user WHERE username = %s')
            user = mysql.execute_query(sql, username)[0]
            if user and check_password_hash(user.get('password'), password):
                session['id'] = user.get('id')
                session['username'] = user.get('username')
                session['role'] = user.get('role')
                return jsonify({'status': 'success', 'message': 'เข้าสู่ระบบสำเร็จ'})
            else:
                return jsonify({'status': 'error', 'message': 'ผู้ใช้งานหรือรหัสผ่านไม่ถูกต้อง'})
        else:
            return jsonify({'status': 'error', 'message': 'กรุณากรอกข้อมูลให้ครบถ้วน'})
    else:
        if 'username' in session:
            return redirect(url_for('home_bp.home'))
        else:
            return render_template('login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if username and password:
            sql = ('SELECT username FROM user WHERE username = %s')
            result_username = mysql.execute_query(sql, username)
            if result_username:
                return jsonify({'status': 'error', 'message': 'ผู้ใช้งานซ้ำกับในระบบ'})
            else:
                sql = ('INSERT INTO user (username, password, role) VALUES (%s, %s, %s)')
                result = mysql.execute_query(sql, (username, generate_password_hash(password), 'user'))
                if result:
                    return jsonify({'status': 'success', 'message': 'สมัครสมาชิกสำเร็จ'})
                else:
                    return jsonify({'status': 'error', 'message': 'สมัครสมาชิกไม่สำเร็จ'})
        else:
            return jsonify({'status': 'error', 'message': 'กรุณากรอกข้อมูลให้ครบถ้วน'})
    else:
        return render_template('signup.html')

@auth_bp.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('auth_bp.login'))