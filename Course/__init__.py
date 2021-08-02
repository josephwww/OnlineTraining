from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
# from flask_admin import Admin
from flask_qrcode import QRcode

app = Flask(__name__)
app.config['SECRET_KEY'] = '8f186ba1cefa1b933177d06bfe418cf5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
# admin = Admin(app)
qrcode = QRcode(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from Course import routes
