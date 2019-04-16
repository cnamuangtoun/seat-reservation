import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from gmdp.bluetooth import Connector

# Create a login manager object
login_manager = LoginManager()
#admin = Admin()

app = Flask(__name__)
mail = Mail(app)

# Often people will also separate these into a separate config.py file
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ninjutsupro@gmail.com'
app.config['MAIL_PASSWORD'] = 'wertoo053'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

db = SQLAlchemy(app)
Migrate(app,db)

mail = Mail(app)

# We can now pass in our app to the login manager
login_manager.init_app(app)


# Tell users what view to go to when they need to login.
login_manager.login_view = "login"
