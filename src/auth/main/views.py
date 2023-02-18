from flask import Flask, render_template, request, url_for, redirect, flash, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from auth.main import bp
from auth.extensions import db
from auth.models.user import User

@bp.route("/signup/", methods=["GET", "POST"])
def signup():
    """
    Implements signup functionality. Allows username and password for new user.
    Hashes password with salt using werkzeug.security.
    Stores username and hashed password inside database.
    Username should to be unique else raises sqlalchemy.exc.IntegrityError.
    """

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirmpassword']

        if not (username and password and confirm_password):
            flash("Username, Password or Confirm Password cannot be empty")
            return redirect(url_for('main.signup'))
        elif password != confirm_password:
            flash("The passwords do not match")
            return redirect(url_for('main.signup'))
        else:
            username = username.strip()
            password = password.strip()

        # Returns salted pwd hash in format : method$salt$hashedvalue
        hashed_pwd = generate_password_hash(password, 'sha256')

        new_user = User(username=username, pass_hash=hashed_pwd)
        db.session.add(new_user)

        try:
            db.session.commit()
        except exc.IntegrityError:
            flash("Username {u} is not available.".format(u=username))
            return redirect(url_for('main.signup'))

        flash("User account has been created.")
        return redirect(url_for("main.login"))

    return render_template("signup.html")


@bp.route("/", methods=["GET", "POST"])
@bp.route("/login/", methods=["GET", "POST"])
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
            return redirect(url_for('main.login'))
        else:
            username = username.strip()
            password = password.strip()

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.pass_hash, password):
            session[username] = True
            return redirect(url_for("main.user_home", username=username))
        else:
            flash("Invalid username or password.")

    return render_template("login_form.html")


@bp.route("/user/<username>/")
def user_home(username):
    """
    Home page for validated users.
    """
    if not session.get(username):
        abort(401)

    return render_template("user_home.html", username=username)


@bp.route("/logout/<username>")
def logout(username):
    """ Logout user and redirect to login page with success message."""
    session.pop(username, None)
    flash("successfully logged out.")
    return redirect(url_for('main.login'))

@bp.route("/cms/", methods=["GET"])
def cms():
    """
    Render the cms.html template.
    """
    return render_template("cms.html")

@bp.route("/cms/panel", methods=["GET"])
def panel():
    """
    Render the cms.html template.
    """
    return render_template("panel.html")
