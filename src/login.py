from flask import Flask, render_template, request, url_for, redirect, flash, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from app import app, db
from src.models import User, Role
from functools import wraps
from src.decorators import login_required, requires_access_level
from src.perfiles import *

@app.route("/signup/", methods=["GET", "POST"])
@login_required
@requires_access_level("Administrator")
def signup():
    """
    Implements signup functionality. Allows username and password for new user.
    Hashes password with salt using werkzeug.security.
    Stores username and hashed password inside database.
    Username should to be unique else raises sqlalchemy.exc.IntegrityError.
    """

    if request.method == "POST":
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        user_rol = request.form['user_rol']
        password = request.form['password']
        confirm_password = request.form['confirmpassword']
        
        
        if not (username and first_name and last_name and password and confirm_password):
            flash("Username, First name, Last name Password or Confirm Password cannot be empty")
            return redirect(url_for('signup'))
        elif password != confirm_password:
            flash("The passwords do not match")
            return redirect(url_for('signup'))
        elif Role.query.filter_by(name=user_rol).first() == None:
            flash("Invalid user role")
            return redirect(url_for('signup'))
        else:
            username = username.strip()
            password = password.strip()

        # Returns salted pwd hash in format : method$salt$hashedvalue
        hashed_pwd = generate_password_hash(password, 'sha256')
        print(Role.query.filter_by(name=user_rol).first())
        new_user = User(username=username, first_name=first_name,\
            last_name=last_name, rol=Role.query.filter_by(name=user_rol).first().id,\
                pass_hash=hashed_pwd)
        db.session.add(new_user)

        try:
            db.session.commit()
        except exc.IntegrityError:
            flash("Username {u} is not available.".format(u=username))
            return redirect(url_for('signup'))

        flash("User account has been created.")
        return redirect(url_for("perfiles"))

    return render_template("signup.html")

@app.route("/")
@app.route("/login/", methods=["GET", "POST"])
def login():
    """
    Provides login functionality by rendering login form on get request.
    On post checks password hash from db for given input username and password.
    If hash matches redirects authorized user to home page else redirect to
    login page with error message.
    """

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if not (username and password):
            flash("Username or Password cannot be empty.")
            return redirect(url_for('login'))
        else:
            username = username.strip()
            password = password.strip()

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.pass_hash, password):
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for("home", username=username))
        else:
            flash("Invalid username or password.")

    return render_template("login_form.html")

@app.route("/user/<username>")
@login_required
def home(username):
    """
    Home page for validated users.
    """
    return render_template('home.html', username=username)

@app.route("/logout/")
@login_required
def logout():
    """ Logout user and redirect to login page with success message."""
    session.pop('logged_in', None)
    session.pop('username', None)
    flash("successfully logged out.")
    return redirect(url_for('login'))
