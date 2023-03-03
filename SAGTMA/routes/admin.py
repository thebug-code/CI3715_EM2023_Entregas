from flask import (Response, current_app, flash, redirect, render_template,
                   request, url_for, session)

from SAGTMA.models import Event, Role, User, db
from SAGTMA.utils import events, profiles
from SAGTMA.utils.decorators import requires_roles


@current_app.route('/user-profiles/',methods=['GET', 'POST'])
@requires_roles('Administrador')
def users_profiles() -> Response:
    '''Muestra la lista de usuarios registrados en el sistema'''
    if request.method == 'POST':
        # Obtiene los datos del formulario
        user = request.form.get('user-filter').lower().strip()
        role = request.form.get('role-filter')

        # SELECT * FROM users
        stmt = db.select(User)
        if user:
            # WHERE (names || surnames) LIKE '%user%' OR
            #     username LIKE '%user%'
            stmt = stmt.where(db.or_(
                db.func.lower(User.names + ' ' + User.surnames).like(f'%{user}%'),
                User.username.like(f'%{user}%')
            ))
        if role:
            # WHERE role_id = role
            stmt = stmt.where(User.role_id == role)

        # Añade el evento de búsqueda
        events.add_search_user(user, role)
    else:
        # Selecciona los usuarios y roles de la base de datos
        stmt = db.select(User)

    result = db.session.execute(stmt).fetchall()
    users = [r for r, in result]

    stmt = db.select(Role).where(Role.id != 1)
    result = db.session.execute(stmt).fetchall()
    roles = [r for r, in result]
    return render_template('admin/users.html', users=users, roles=roles)

@current_app.route('/event-logger/', methods=['GET', 'POST'])
@requires_roles('Administrador')
def logger() -> Response:
    if request.method == 'POST':
        # Obtiene los datos del formulario
        event = request.form.get('event-filter').lower().strip()

        # SELECT * FROM event JOIN user ON event.user_id = user.id
        stmt = db.select(Event).join(User, Event.user_id == User.id)
        if event:
            # WHERE type LIKE '%event%' OR
            #     module LIKE '%event%' OR
            #     user.name LIKE '%event%'
            stmt = stmt.where(db.or_(
                Event.description.like(f'%{event}%'),
                Event.module.like(f'%{event}%'),
                db.func.lower(User.names + ' ' + User.surnames).like(f'%{event}%')
            ))

            # Añade el evento de búsqueda
            events.add_search_log(event)
    else:
        # Selecciona los eventos de la base de datos
        stmt = db.select(Event)

    result = db.session.execute(stmt).fetchall()
    events = [r for r, in result]
    return render_template('admin/logger.html', events=events)

@current_app.route('/user-profiles/register/', methods=['POST'])
@requires_roles('Administrador')
def register() -> Response:
    '''Registra un usuario en la base de datos.'''
    username = request.form.get('username')
    names = request.form.get('names')
    surnames = request.form.get('surnames')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')
    role = request.form.get('role')

    try:
        profiles.register_user(
            username, names, surnames,
            password, confirm_password, role
        )
    except profiles.AuthenticationError as e:
        flash(f'{e}')

    # Se permanece en la página
    flash('Usuario registrado exitosamente')
    return redirect(url_for('users_profiles'))

@current_app.route('/user-profiles/delete/<int:user_id>/', methods=['POST'])
@requires_roles('Administrador')
def delete_user(user_id: int) -> Response:
    '''Elimina un usuario de la base de datos.'''
    try:
        profiles.delete_user(user_id)
    except profiles.AuthenticationError as e:
        flash(f'{e}')
        return redirect(url_for('users_profiles'))

    flash('Usuario eliminado exitosamente')
    return redirect(url_for('users_profiles'))

@current_app.route('/user-profiles/modify/<int:user_id>/', methods=['POST'])
@requires_roles('Administrador')
def edit_user(user_id: int) -> Response:
    '''Edita un usuario en la base de datos.'''
    # Obtiene los datos del formulario
    username = request.form.get('username')
    names = request.form.get('names')
    surnames = request.form.get('surnames')
    role = request.form.get('role')

    try:
        profiles.edit_user(user_id, username, names, surnames, role)

        # Si el usuario editado es el mismo que está logueado, cambia su sesión
        if int(user_id) == session['id']:
            session['username'] = username
    except profiles.AuthenticationError as e:
        flash(f'{e}')
        return redirect(url_for('users_profiles'))

    # Se permanece en la página
    flash('Usuario editado exitosamente')
    return redirect(url_for('users_profiles'))