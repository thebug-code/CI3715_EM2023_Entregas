from flask import Response, abort, current_app, redirect, session, url_for

from SAGTMA.utils.decorators import login_required


@current_app.route('/')
@login_required
def home() -> Response:
    '''Redirige a la página principal según el rol del usuario'''
    user_role = session['role']
    if user_role == 'Administrador':
        return redirect(url_for('users_profiles'))
    elif user_role == 'Gerente de Operaciones':
        return redirect(url_for('portfolio'))

    # Retorna error de acceso denegado si el usuario tiene un rol no implementado
    abort(403)