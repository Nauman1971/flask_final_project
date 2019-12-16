from flask import render_template, redirect, url_for, request, flash, send_file
from flask_login import login_user, login_required, logout_user, current_user
from flask import current_app as app
from ..forms import SignupForm, LoginForm
from ..models import db, User


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/users')
def show_users():
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/profile', methods=["POST", "GET"])
def profile():
    username = request.form["profile"]
    profiles = User.query.filter_by(username=username)
    return render_template("profile.html", profiles=profiles)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    username = request.form['target_user']
    user_found = User.query.filter_by(username=username).first()
    db.session.delete(user_found)
    db.session.commit()

    users = User.query.all()
    return redirect(url_for('show_users', users=users))


@app.route('/update_profile', methods=["POST"])
def update_profile():
    username = request.form['target_user']
    roles = request.form['target_role']
    email = request.form['target_email']
    number = request.form['target_number']
    user_found = User.query.filter_by(username=username).first()
    user_found.username = username
    user_found.email = email
    user_found.roles = roles
    user_found.number = number

    db.session.add(user_found)
    db.session.commit()
    users = User.query.all()
    return redirect(url_for('show_users', users=users))


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    password = form.password.data
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user.password == password:
            login_user(user)
            flash("You are logged in as {}".format(form.username.data), "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid Credentials", "danger")
    return render_template('login.html', form=form)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        password = request.form["password"]
        email = form.email.data
        number = form.number.data
        roles = form.roles.data
        file = form.file.data
        file = file.read()
        existing_username = User.query.filter_by(username=username).first()
        if existing_username is None:
            newUser = User(username=username, password=password, email=email, number=number, roles=roles, file=file)
            db.session.add(newUser)
            db.session.commit()
            flash("User {} is created successfully".format(newUser.username), 'success')
        else:
            flash("A user is Already Exist with this username", 'danger')
    return render_template('signup.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    send_f = send_file(current_user.file)
    return render_template('/dashboard.html', name=current_user.username, send_f=send_f)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
