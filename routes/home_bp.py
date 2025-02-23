from flask import Blueprint, redirect, url_for

home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/')
def home():
    return redirect(url_for('parking_bp.parking_index'))