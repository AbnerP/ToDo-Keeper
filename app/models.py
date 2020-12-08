from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
        return User.query.get(int(user_id)) 

#Database Model
class User(UserMixin,db.Model): #Add UserMixin to DataBase Model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80),nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    security_question_1 = db.Column(db.String(15))
    security_answer_1 = db.Column(db.String(80))
    security_question_2 = db.Column(db.String(15))
    security_answer_2 = db.Column(db.String(80))
    
    tasks = db.relationship('Task',backref='creatorOfTask',lazy=True) 
    #Task references actually model class
    #lazy means sqlalchemy will load the data from the database automatically
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(150),nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    #date_due = db.Column(db.DateTime)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    #ForeignKey references actual table name and column name hence user(table).id(column)
    
    def __repr__(self):
        return f"Task('{self.text}', '{self.date_posted}')" 