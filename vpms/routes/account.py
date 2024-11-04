from flask import Blueprint, jsonify, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from databases.mysql import mysql_database
from routes.auth import login_required

account_bp = Blueprint('account', __name__)

@account_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    username = session.get('username')
    role_name = session.get('role_name')
    if request.method == 'POST':
        data = request.get_json()
        password = data.get('password')
        if password:
            try:
                connection = mysql_database()
                sql = ('SELECT u.password FROM users u WHERE u.username = %s')
                old_password = connection.select_one(sql, username)
                if old_password:
                    if check_password_hash(old_password.get('password'), password):  # เปรียบเทียบรหัสผ่านเก่าและใหม่
                        return jsonify({'status': 'error', 'message': 'รหัสผ่านใหม่ไม่สามารถตรงกับรหัสผ่านเก่าได้'})
                    else:
                        sql = ('UPDATE users SET password = %s WHERE username = %s')
                        connection.update(sql, (generate_password_hash(password), username))
                        return jsonify({'status': 'ok',
                                    'message': 'แก้ไขข้อมูลสำเร็จ'})
                else:
                    return jsonify({'status': 'error',
                                    'message': 'แก้ไขข้อมูลไม่สำเร็จ'})
            except Exception as e:
                print(e)
                return jsonify({'status': 'error',
                                'message': 'แก้ไขข้อมูลไม่สำเร็จ'})
    else:
        return render_template('account.html', role_name = role_name, username = username)
