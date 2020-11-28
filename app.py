# Code template taken from https://github.com/PrettyPrinted/building_user_login_system/
from flask import Flask, render_template, url_for, redirect, session
from flask_bootstrap import Bootstrap
from forms import LoginForm, RegisterForm
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

#Tasks
tasklist = [
    {
        'User': 'User 1',
        'Task':'Task 1',
        'due_date': '1/1/2021',
        'date_posted':'12/1/2020'
    },
    {
        'User': 'User 1',
        'Task':'Task 2',
        'due_date': '1/2/2021',
        'date_posted':'12/1/2020'
    },
    {
        'User': 'User 1',
        'Task':'Task 3',
        'due_date': '1/3/2021',
        'date_posted':'12/1/2020'
    }
]

#Database Model
class User(UserMixin,db.Model): #Add UserMixin to DataBase Model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80),nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}',)"

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(150),nullable=False)
    date_poster = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    

@login_manager.user_loader
def load_user(user_id):
        return User.query.get(int(user_id)) 

@app.route('/')
def index():
    userStatus = current_user.is_active
    return render_template('index.html',user=userStatus)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password,form.password.data):
                login_user(user, remember=form.remember.data) #Allow user to access dashboard once logged in
                return redirect(url_for('dashboard',name=user.username))
                #return render_template('dashboard.html',name=user.username)
        
        return '<h1>Invalid username or password</h1>'
    
    return render_template('login.html',form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashPass = generate_password_hash(form.password.data, method='sha256')
        newUser = User(username=form.username.data, email=form.email.data, password=hashPass)
        
        db.session.add(newUser)
        db.session.commit()
        login_user(newUser,remember=form.remember.data)
        
        return redirect(url_for('dashboard'))
        #return '<h1> Hello '+form.username.data+'!</h1>'

    return render_template('signup.html', form=form)

@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    return render_template('dashboard.html',tasks=tasklist,name=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
