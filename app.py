from flask import Flask
from routes import video_bp
from routes.camera_bp import camera_bp
from routes.home_bp import home_bp
from routes.video_bp import video_bp
from routes.parking_bp import parking_bp

if __name__ == '__main__':

    app = Flask(__name__)

    app.register_blueprint(home_bp)
    app.register_blueprint(camera_bp, url_prefix='/camera')
    app.register_blueprint(video_bp, url_prefix='/video')
    app.register_blueprint(parking_bp, url_prefix='/parking')

    app.run(host='0.0.0.0', port=5000, debug=True)