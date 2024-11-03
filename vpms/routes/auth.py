from functools import wraps
from flask import Blueprint, request, redirect, url_for, session, render_template
from vpms.databases.mysql_database import MySQL_Database
from werkzeug.security import generate_password_hash, check_password_hash


auth_bp = Blueprint('auth', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def permission_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role_name' not in session or session['role_name'] != 'admin':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        try:
            connection = MySQL_Database()
            # ตรวจสอบว่าชื่อผู้ใช้หรืออีเมลมีอยู่แล้วหรือไม่
            sql = ('SELECT username '
                   'FROM users '
                   'WHERE username = %s')
            result_username = connection.select_fetchone(sql, username)
            if result_username:
                error = 'Username ถูกใช้งานแล้ว'
            else:
                sql = ('SELECT email '
                       'FROM users '
                       'WHERE email = %s')
                result_email = connection.select_fetchone(sql, email)
                if result_email:
                    error = 'Email ถูกใช้งานแล้ว'
                else:
                    hashed_password = generate_password_hash(password)
                    sql = ('INSERT INTO users (user_role, first_name, last_name, username, password, email) '
                           'VALUES (%s, %s, %s, %s, %s, %s)')
                    connection.insert(sql, (2, first_name, last_name, username, hashed_password, email))
        except Exception as e:
            print(e)
            error = 'เกิดข้อผิดพลาดลองใหม่อีกครั้ง'
        finally:
            if error:
                return render_template('register.html', error=error)
            else:
                return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            connection = MySQL_Database()
            sql = ('SELECT u.user_role, u.username, u.password, r.role_name '
                   'FROM users u '
                   'LEFT JOIN roles r ON u.user_role = r.role_id '
                   'WHERE u.username = %s')
            user = connection.select_fetchone(sql, username)
            if user and check_password_hash(user['password'], password):
                # หากตรวจสอบรหัสผ่านผ่าน ให้บันทึกข้อมูลผู้ใช้ใน session
                session['username'] = user['username']
                session['role_name'] = user['role_name']
            else:
                error = 'Username หรือ Password ไม่ถูกต้อง'
        except Exception as e:
            print(e)
            error = 'เกิดข้อผิดพลาดลองใหม่อีกครั้ง'
        finally:
            if error:
                return render_template('login.html', error=error)
            else:
                return redirect(url_for('dashboard.dashboard'))

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
