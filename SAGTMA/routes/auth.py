from flask import (Response, current_app, flash, redirect, render_template,
                   request, session, url_for)

from SAGTMA.utils import auth
from SAGTMA.utils.decorators import login_required, logout_required


@current_app.route('/login/',methods=['GET', 'POST'])
@logout_required
def login() -> Response:
    '''Inicia la sesión de un usuario y guarda el correo electrónico y nombre
    en la sesión.
    '''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            id, role = auth.log_user(username, password)

            # Guarda la id del usuario y su nombre de usuario en la sesión
            session['id'] = id
            session['username'] = username
            session['role'] = role
        except auth.AuthenticationError as e:
            # Si algo salió mal, permanece en la página
            flash(f'{e}')
            return redirect(request.url)

        # Si el inicion de sesión es exitoso, redirige a la paǵina principal
        return redirect(url_for('home'))

    return render_template('base/login.html')

@current_app.route('/logout/',methods=['POST'])
@login_required
def logout() -> Response:
    '''Cierra la sesión de un usuario y elimina los datos de la sesión.'''
    # Elimina los datos de la sesión
    session.clear()
    return redirect(url_for('login'))