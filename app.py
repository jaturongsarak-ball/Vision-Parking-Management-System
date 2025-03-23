from flask import Flask
from routes import video_bp
from routes.camera_bp import camera_bp
from routes.home_bp import home_bp
from routes.video_bp import video_bp
from routes.parking_bp import parking_bp
from routes.parking_stat_bp import parking_stat_bp
from routes.auth_bp import auth_bp
from routes.account_bp import account_bp

if __name__ == '__main__':

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'SECRET_KEY'

    app.register_blueprint(home_bp)
    app.register_blueprint(camera_bp, url_prefix='/camera')
    app.register_blueprint(video_bp, url_prefix='/video')
    app.register_blueprint(parking_bp, url_prefix='/parking')
    app.register_blueprint(parking_stat_bp, url_prefix='/parking_stat')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(account_bp, url_prefix='/account')


    app.run(host='0.0.0.0', port=5000, debug=True)