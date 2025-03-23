from functools import wraps
from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
import database.mysql as mysql
from werkzeug.security import generate_password_hash, check_password_hash
from routes.auth_bp import login_required

account_bp = Blueprint('account_bp', __name__)

@account_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == 'POST':
        data = request.get_json()
        user_id = data.get('user_id')
        password = data.get('password')
        if not (user_id and password):
            return jsonify({'status': 'error', 'message': 'กรุณากรอกข้อมูลให้ครบถ้วน'})
        hashed_password = generate_password_hash(password)
        sql = 'UPDATE user SET password = %s WHERE id = %s'
        updated_rows = mysql.execute_query(sql, (hashed_password, user_id))
        if updated_rows:
            return jsonify({'status': 'success', 'message': 'แก้ไขรหัสผ่านสำเร็จ'})
        else:
            return jsonify({'status': 'error', 'message': 'ไม่พบผู้ใช้งาน'})
    else:
        user = {
            "id": session['id'],
            "username": session['username'],
            "role": session['role']
        }
        print(user)
        return render_template('account.html', user=user)