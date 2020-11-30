from werkzeug.security import check_password_hash
from datetime import datetime
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, DateField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Email, Length, EqualTo,ValidationError
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[DataRequired(),InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')
    
    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError("An account with that username does not exist.")

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('Username', validators=[DataRequired(),InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[DataRequired(),InputRequired(), Length(min=8, max=80)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),InputRequired(), Length(min=8, max=80),EqualTo('password')])
    remember = BooleanField('Remember me')
    
    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username is already taken. Please choose another one.")
    
    def validate_email(self,email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("An account is already associated with this email address. Please choose another one.")
    
    
class TaskForm(FlaskForm):
    text = StringField('Task', validators=[DataRequired(),InputRequired(), Length(max=150)])
    #date = DateField('Date Due')
    submit = SubmitField('Add Task')
    
    #def validate_date(form, date):
        #if date.data < datetime.date.today():
            #raise ValidationError("The date cannot be in the past!")