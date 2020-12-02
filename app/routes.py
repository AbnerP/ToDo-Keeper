from flask import render_template, url_for, redirect, session,flash
from flask.globals import request
from app import app,db,login_manager
from app.forms import LoginForm, RegisterForm, TaskForm, UpdateAccoountForm
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import os
from app.models import User,Task

#Initialize Flask Login

    
@login_manager.user_loader
def load_user(user_id):
        return User.query.get(int(user_id)) 

@app.route('/')
def index():
    form = LoginForm()
    formT = TaskForm()
    userStatus = current_user.is_active
    if userStatus:
        return redirect(url_for('dashboard',userStatus=userStatus,tasks=current_user.tasks,name=current_user.username,form=formT))
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

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex+f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics',picture_filename)
    form_picture.save(picture_path)
    return picture_filename



@app.route('/dashboard/profile', methods=['GET','POST'])
@login_required
def profile():
    form = UpdateAccoountForm()
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    userStatus = current_user.is_active
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        
        flash('Your account has been updated!','success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('profile.html',userStatus=userStatus,user=current_user,image_file=image_file,form=form)

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
