from flask_login import LoginManager
from flask_mail import Mail
from flask import Flask
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "xxkxcZKH2TxsSw7bew8D9gLpCaa3YYnn"

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('DB_USER')
app.config['MAIL_PASSWORD'] = 'yeojdrntrqscgxit'

mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)

