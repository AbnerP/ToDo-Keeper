from werkzeug.security import check_password_hash
from datetime import datetime
from flask_wtf import FlaskForm 
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField, DateField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Email, Length, EqualTo,ValidationError
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[DataRequired(),InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Keep me logged in?')
    
    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError("An account with that username does not exist.")

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('Username', validators=[DataRequired(),InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[DataRequired(),InputRequired(), Length(min=8, max=80)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),InputRequired(), Length(min=8, max=80),EqualTo('password')])
    remember = BooleanField('Keep me logged in?')
    
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
    date = DateField('Date Due',format='%m/%d/%Y')
    submit = SubmitField('Add Task')
    
    def process_formdata(self, date):
        if date():
            date_str = ' '.join(date()).strip()
            if date_str == '':
                self.data = None
                return
            try:
                self.data = datetime.datetime.strptime(date_str, self.format).date()
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Not a valid date value'))
    #def validate_date(form, date):
        #if date.data < datetime.date.today():
            #raise ValidationError("The date cannot be in the past!")

class UpdateAccoountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),InputRequired(), Length(min=4, max=15)])
    email = StringField('Email', validators=[DataRequired(), InputRequired(), Email(message='Invalid email'), Length(max=50)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')
    
    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username is already taken. Please choose another one.")
    
    def validate_email(self,email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError("An account is already associated with this email address. Please choose another one.")

class NewTag(FlaskForm):
    name = StringField('Tag Name', validators=[DataRequired(),InputRequired(), Length(max=20)])
    submit = SubmitField('Add Tag')