from gmdp import app,db
from gmdp.bluetooth import Connector
from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user,login_required,logout_user,current_user
from gmdp.models import User, Seat, User_Seat, connector
from gmdp.forms import LoginForm, RegistrationForm, reservation_form_builder, BTForm
from werkzeug.security import generate_password_hash, check_password_hash
import datetime as dt

#for i in range (0,12):
#    seat = Seat(seat_id = 'A%d' % i)
#    db.session.add(seat)
#    user_seat = User_Seat(seat_id = 'A%d' % i)
#    db.session.add(user_seat)
#    db.session.commit()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/seat_reservation', methods=['GET','POST'])
@login_required
def seat_reservation():
    info = connector.Rvalue()
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

@app.route('/terminate')
def terminate():
    connector.terminate()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
