# Code template taken from https://github.com/PrettyPrinted/building_user_login_system/

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from forms import LoginForm, RegisterForm
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

#Initialize app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

#login_manager = LoginManager()
#login_manager.init_app(app)
#login_manager.login_view = 'login'

#Database Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        return '<h1>'+form.username.data+' '+form.password.data+'</h1>'
    
    return render_template('login.html',form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        newUser = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(newUser)
        db.session.commit()
        
        return '<h1> Hello '+form.username.data+'!</h1>'
        #return '<h1>'+form.username.data+' '+form.password.data+' '+form.email.data+'</h1>'

    return render_template('signup.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
