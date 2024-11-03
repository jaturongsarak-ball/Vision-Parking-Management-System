from config import Envelopment
from flask import Flask

app = Flask(__name__)
app.config.from_object(Envelopment)

from routes.index import index_bp
app.register_blueprint(index_bp)

from routes.auth import auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

from routes.dashboard import dashboard_bp
app.register_blueprint(dashboard_bp, url_prefix='/admin')

if __name__ == '__main__':
    app.run()