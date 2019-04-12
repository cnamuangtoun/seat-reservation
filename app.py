from gmdp import app,db
from flask import render_template, redirect, request, url_for, flash, abort
from gmdp.bluetooth import Connector
from flask_login import login_user,login_required,logout_user,current_user
from gmdp.models import User, Seat, User_Seat
from gmdp.forms import LoginForm, RegistrationForm, reservation_form_builder, BTForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO, emit
from threading import Thread, Event
import datetime as dt
import atexit
import serial
import time

#for i in range (0,12):
#    seat = Seat(seat_id = 'A%d' % i)
#    db.session.add(seat)
#    user_seat = User_Seat(seat_id = 'A%d' % i)
#    db.session.add(user_seat)
#    db.session.commit()

socketio = SocketIO(app)

#random number Generator Thread

connector = Connector("COM6")

thread = Thread()
thread_stop_event = Event()

# global connector

class RandomThread(Thread):
    def __init__(self, connector):
        self.delay = 1
        self.connection = connector
        super(RandomThread,self).__init__()

    def dataTransfer(self):
        """
        Generate a random number every 1 second and emit to a socketio instance (broadcast)
        Ideally to be run in a separate thread?
        """
        #infinite loop of magical random numbers
        while not thread_stop_event.isSet():
            try:
                status = self.connection.Rvalue()
                print(status)
                # else:
                # socketio.emit('newstatus', {'status': status}, namespace='/test')
            except:
                print("Cant decode")

            try:
                if int(status[0]):
                    warning = 1
                    socketio.emit('warning', {'warning': warning}, namespace='/test')

                if int(status[1]):
                    seat = Seat.query.filter_by(seat_id="A0").first()
                    seat.status = 0;
                    user_seat = User_Seat.query.filter_by(seat_id="A0").first()
                    user_seat.user_email = ""
                    db.session.commit()
                    time_out = 1
                    socketio.emit('time_out', {'time_out': time_out}, namespace='/test')
            except:
                print("trying again")

            time.sleep(self.delay)

    def run(self):
        self.dataTransfer()

@app.route('/')
def home():
    return render_template('home.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global connector
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = RandomThread(connector)
        thread.start()

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/seat_reservation', methods=['GET','POST'])
@login_required
def seat_reservation():
    return render_template('seat_reservation.html')

@app.route('/seat_reservation/floor_1')
@login_required
def foor_1():
    return render_template('floor/floor_1.html')

@app.route('/seat_reservation/floor_2', methods=['GET','POST'])
@login_required
def floor_2():

    seats = ['A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11']

    ReservationForm = reservation_form_builder(seats)
    err = False
    disp = []
    data = Seat.query.all()
    for seat_num in data:
        user_seat = User_Seat.query.filter_by(seat_id= seat_num.seat_id).first()
        if current_user.email != user_seat.user_email and seat_num.status:
            disp.append(2)
        else:
            disp.append(int(seat_num.status == 1))

    if ReservationForm.validate_on_submit():
        #if not err:
        for forms in ReservationForm:
            #ignores submit form and the csrf_token at the end of ReservationForm
            if forms.id != 'submit' and forms.id != 'csrf_token':
                seat = Seat.query.filter_by(seat_id=forms.description).first()
                user_seat = User_Seat.query.filter_by(seat_id=forms.description).first()
                change = seat.status != forms.data
                #if the seat is reserved by the current user and he wants to un-reserve it or he wants to reserved an unoccupied seats
                #change the seat status accordingly
                if (current_user.email == user_seat.user_email and not forms.data) or forms.data:
                    seat.status = forms.data
                #update user_seat if the person is reserving a seat else if he is unreserving a seat only update user_seat if the seat
                #is reserved by current user
                if forms.data and change:
                    user_seat.user_email = current_user.email
                elif not forms.data and change and user_seat.user_email == current_user.email:
                    user_seat.user_email = ""
                db.session.commit()
                reserved = True
        if reserved:
            connector.Wvalue("r")
            flash('Sucessful Reservation')
        return (redirect(url_for('floor_2')))

    return render_template('floor/floor_2.html', form = ReservationForm, disp = disp)

@app.route('/seat_reservation/floor_3')
@login_required
def foor_3():
    return render_template('floor/floor_3.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have logged out')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if (current_user.is_authenticated):
        return redirect(url_for('seat_reservation'))
    # Create instance of the form.
    form = LoginForm()
    # If the form is valid on submission
    if form.validate_on_submit():
        # Grab the data from the breed on the form.
        user = User.query.filter_by(email=form.email.data).first()
        #session['id'] = form.id.data
        #session['pwd'] = form.pwd.data

        if user is not None and user.check_password(form.password.data):
            #Log in the user

            login_user(user)
            flash('Logged in successfully.')
            next = request.args.get('next')

            if next == None or not next[0]=='/':
                next = url_for('seat_reservation')

            return redirect(next)
        else:
            flash('Invalid Username or Password')

    return render_template('login.html', form=form)

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    # Create instance of the form.
    form = RegistrationForm()
    # If the form is valid on submission

    if form.validate_on_submit():
        # Grab the data from the breed on the form.
        user = User(#type=form.type.data,
                    email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')

        return redirect(url_for('login'))
    return render_template('sign_up.html', form=form)

# @app.route('/test', methods=['GET','POST'])
# def test():
#     form = BTForm()
#     connector.Flush()
#     if form.validate_on_submit():
#         if form.turnOn.data:
#             connector.Wvalue('e')
#         else:
#             connector.Wvalue('g')
#         time.sleep(0.5)
#         read = connector.Rvalue()
#         print(read)
#         #read = connector2.Rvalue()
#
#         return redirect(url_for('test'))
#
#     return render_template('test.html', form = form)

if __name__ == '__main__':
    app.run()
