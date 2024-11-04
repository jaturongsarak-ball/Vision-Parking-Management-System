from config import envelopment
from flask import Flask

app = Flask(__name__)
app.config.from_object(envelopment)

from routes.home import home_bp
app.register_blueprint(home_bp)

from routes.auth import auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

from routes.account import account_bp
app.register_blueprint(account_bp, url_prefix='/account')

if __name__ == '__main__':
    app.run()
