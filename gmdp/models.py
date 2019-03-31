from gmdp import app,db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for

# By inheriting the UserMixin we get access to a lot of built-in attributes
# which we will be able to call in our views!
# is_authenticated()
# is_active()
# is_anonymous()
# get_id()


# The user_loader decorator allows flask-login to load the current user
# and grab their id.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    #type = db.Column(db.String(16))
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    #seat_num = db.Column()

    def __init__(self, email, username, password):
        #self.type = type
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
        return check_password_hash(self.password_hash,password)

class Seat(db.Model):
    __tablename__ = 'seats'

    id = db.Column(db.Integer, primary_key = True)
    seat_id = db.Column(db.String(2))
    status = db.Column(db.Integer)

    def __init__(self, seat_id):
        self.seat_id = seat_id
        self.status = 0

class User_Seat(db.Model):
    __tablename__ = 'user_seat'

    id = db.Column(db.Integer, primary_key = True)
    user_email = db.Column(db.String(64), index=True)
    seat_id = db.Column(db.String(2))

    def __init__(self, seat_id):
        self.seat_id = seat_id
        self.user_email = ""

class MyModelView(ModelView):
    def  is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

admin = Admin(app, name='admin', template_mode='bootstrap3', index_view = MyAdminIndexView())
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Seat, db.session))
admin.add_view(MyModelView(User_Seat, db.session))
