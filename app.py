# Code template taken from https://github.com/PrettyPrinted/building_user_login_system/
from flask import Flask, render_template, url_for, redirect, session,flash
from flask_bootstrap import Bootstrap
from forms import LoginForm, RegisterForm, TaskForm
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime

#Initialize app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

#Initialize Flask Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#Database Model
class User(UserMixin,db.Model): #Add UserMixin to DataBase Model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80),nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    
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
    
@login_manager.user_loader
def load_user(user_id):
        return User.query.get(int(user_id)) 

@app.route('/')
def index():
    form = LoginForm()
    formT = TaskForm()
    userStatus = current_user.is_active
    if userStatus:
        return redirect(url_for('dashboard',userStatus=userStatus, tasks=tasklist,name=current_user.username,form=formT))
    else:
        return render_template('login.html',form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    formT = TaskForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password,form.password.data):
                login_user(user, remember=form.remember.data) #Allow user to access dashboard once logged in
                print("LOG IN -'"+str(current_user.username+"'"))
                return redirect(url_for('dashboard',name=user.username,form=formT))
                #return render_template('dashboard.html',name=user.username)
        flash('Invalid username or password','danger')
    
    return render_template('login.html',form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    formT = TaskForm()
    userStatus = current_user.is_active

    if form.validate_on_submit():
        hashPass = generate_password_hash(form.password.data, method='sha256')
        newUser = User(username=form.username.data, email=form.email.data, password=hashPass)
        
        db.session.add(newUser)
        db.session.commit()
        login_user(newUser,remember=form.remember.data)
        
        print("NEW USER -'"+str(current_user.username+"'"))
        
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('dashboard',userStatus=userStatus,name=current_user.username,form=formT))
        #return '<h1> Hello '+form.username.data+'!</h1>'

    return render_template('signup.html', form=form)

@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    form = TaskForm()
    userStatus = current_user.is_active
    
    if form.validate_on_submit():
        newTask = Task(text=form.text.data, user_id=current_user.id)
        
        db.session.add(newTask)
        db.session.commit()
        print("NEW TASK CREATED -'"+str(newTask)+"'")
        flash(f'{current_user.username} created a task!','success')
        return redirect(url_for('dashboard',userStatus=userStatus,tasks=current_user.tasks,name=current_user.username,form=form))
        #return '<h1> Hello '+form.username.data+'!</h1>'
    
    return render_template('dashboard.html',userStatus=userStatus,tasks=current_user.tasks,name=current_user.username ,form=form)

@app.route('/dashboard/profile', methods=['GET','POST'])
@login_required
def profile():
    userStatus = current_user.is_active
    return render_template('profile.html',userStatus=userStatus,user=current_user)

@app.route('/dashboard/settings', methods=['GET','POST'])
@login_required
def settings():
    userStatus = current_user.is_active
    return render_template('settings.html',userStatus=userStatus,user=current_user)

@app.route('/logout')
@login_required
def logout():
    form = LoginForm()
    print("LOG OUT  -'"+str(current_user.username+"'"))
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
