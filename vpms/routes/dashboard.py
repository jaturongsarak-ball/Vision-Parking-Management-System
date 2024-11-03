from flask import Blueprint, render_template
from vpms.routes.auth import login_required, permission_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
@permission_required
def dashboard():
    return render_template('dashboard.html')