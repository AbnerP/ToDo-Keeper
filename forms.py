from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, InputRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[DataRequired(),InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('Username', validators=[DataRequired(),InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[DataRequired(),InputRequired(), Length(min=8, max=80)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),InputRequired(), Length(min=8, max=80),EqualTo('password')])
    remember = BooleanField('Remember me')