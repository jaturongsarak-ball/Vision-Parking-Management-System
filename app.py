from flask import Flask
from routes.camera_bp import camera_bp
from routes.home_bp import home_bp

if __name__ == '__main__':

    app = Flask(__name__)

    app.register_blueprint(home_bp)
    app.register_blueprint(camera_bp, url_prefix='/camera')

    app.run(host='0.0.0.0', port=5000, debug=True)