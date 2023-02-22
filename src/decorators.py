from flask import session, flash, redirect, url_for
from src.models import User, Role
from functools import wraps

# Decoradores
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

def requires_access_level(role):
    """Verifica si el usuario puede acceder a la vista""" 
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = User.query.filter_by(username=session['username']).first()
            if user != None and user.role.name == role:
                return f(*args, **kwargs)
            else:
                flash("You do not have access to that page. Sorry!")
                return redirect(url_for('perfiles')) #tal vez hay que cambiar esto luego
        return decorated_function
    return decorator

