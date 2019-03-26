from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField,SelectField,TextField,
                     TextAreaField,SubmitField,PasswordField)
from wtforms.validators import DataRequired,Email,EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):

    #type = RadioField(choices=[('type_one','Student'),('type_two','Guest')])
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm Password',validators=[DataRequired()])
    email = StringField('Email Address',validators=[DataRequired(),Email()])
    submit = SubmitField('Register')

    def check_email(self, field):
        # Check if not None for that user email!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def check_username(self, field):
        # Check if not None for that username!
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')

class ReservationForm(FlaskForm):
    seat_id = [BooleanField('A1'), BooleanField('A2'), BooleanField('A3'), BooleanField('A4'), BooleanField('A5')
            , BooleanField('A6'), BooleanField('A7'), BooleanField('A8'), BooleanField('A9'), BooleanField('A10')
            , BooleanField('A11'), BooleanField('A12')]
