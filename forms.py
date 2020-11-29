from werkzeug.utils import validate_arguments
from datetime import datetime
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, DateField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Email, Length, EqualTo,ValidationError

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
    
class TaskForm(FlaskForm):
    text = StringField('Task', validators=[DataRequired(),InputRequired(), Length(max=150)])
    #date = DateField('Date Due')
    submit = SubmitField('Add Task')
    
    #def validate_date(form, field):
        #if field.data < datetime.date.today():
            #raise ValidationError("The date cannot be in the past!")