from flask import session, flash, redirect, url_for, abort
from functools import wraps

def login_required(f):
    '''Decorador de login requerido para rutas protegidas.

    Si el usuario no ha iniciado sesión, se redirige a la página de
    inicio de sesión.
    '''
    @wraps(f)
    def verify_login(*args, **kwargs):
        if 'username' in session:
            return f(*args, **kwargs)
        else:
            flash('Necesitas iniciar sesión primero')
            return redirect(url_for('login'))
    return verify_login

def logout_required(f):
    '''Decorador de logout requerido para rutas protegidas.

    Si el usuario ya ha iniciado sesión, se redirige a la página de inicio.
    '''
    @wraps(f)
    def verify_logout(*args, **kwargs):
        if 'username' in session:
            return redirect(url_for('home'))
        else:
            return f(*args, **kwargs)
    return verify_logout

def requires_roles(*roles):
    '''Decorador de roles requeridos para rutas protegidas.

    Verifica primero si el usuario ha iniciado sesión, y luego si tiene alguno
    de los roles requeridos, si no, lanza un error 403 de acceso denegado
    '''
    def wrapper(f):
        @login_required
        @wraps(f)
        def wrapped(*args, **kwargs):
            if session.get('role') not in roles:
                abort(403)
            return f(*args, **kwargs)
        return wrapped

    return wrapper