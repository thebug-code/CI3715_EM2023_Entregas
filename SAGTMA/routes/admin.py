from flask import (
    Response,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    session,
)

from SAGTMA.models import Event, Role, User, Department, db
from SAGTMA.utils import events, profiles, departments
from SAGTMA.utils.decorators import requires_roles


# ========== Perfiles de Usuario ==========
@current_app.route("/user-profiles/", methods=["GET", "POST"])
@requires_roles("Administrador")
def users_profiles() -> Response:
    """Muestra la lista de usuarios registrados en el sistema"""
    # SELECT * FROM user
    stmt = db.select(User)

    if request.method == "POST":
        # Obtiene los datos del formulario
        user = request.form.get("user-filter").lower().strip()
        role = request.form.get("role-filter")

        if user:
            # WHERE (names || surnames) LIKE '%user%' OR
            #     username LIKE '%user%'
            stmt = stmt.where(
                db.or_(
                    db.func.lower(User.names + " " + User.surnames).like(f"%{user}%"),
                    User.username.like(f"%{user}%"),
                )
            )
        if role:
            # WHERE role_id = role
            stmt = stmt.where(User.role_id == role)

        # Añade el evento de búsqueda
        events.add_event(
            "Perfiles de Usuarios",
            f"Buscar '{user}' en "
            + ("todos los roles" if not role else f"el rol '{role}'"),
        )

    result = db.session.execute(stmt).fetchall()
    users = [r for r, in result]

    stmt = db.select(Role).where(Role.id != 1)
    result = db.session.execute(stmt).fetchall()
    roles = [r for r, in result]
    return render_template("admin/users.html", users=users, roles=roles)


@current_app.route("/user-profiles/register/", methods=["POST"])
@requires_roles("Administrador")
def register() -> Response:
    """Registra un usuario en la base de datos."""
    # Obtiene los datos del formulario
    id_number = request.form.get("id-number")
    username = request.form.get("username")
    names = request.form.get("names")
    surnames = request.form.get("surnames")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm-password")
    role = request.form.get("role")

    try:
        profiles.register_user(
            id_number, username, names, surnames, password, confirm_password, role
        )
    except profiles.ProfileError as e:
        flash(f"{e}")
        return redirect(url_for("users_profiles"))

    # Se permanece en la página
    flash("Usuario registrado exitosamente")
    return redirect(url_for("users_profiles"))


@current_app.route("/user-profiles/<int:user_id>/delete/", methods=["POST"])
@requires_roles("Administrador")
def delete_user(user_id: int) -> Response:
    """Elimina un usuario de la base de datos."""
    try:
        profiles.delete_user(user_id)
    except profiles.ProfileError as e:
        flash(f"{e}")
        return redirect(url_for("users_profiles"))

    flash("Usuario eliminado exitosamente")
    return redirect(url_for("users_profiles"))


@current_app.route("/user-profiles/<int:user_id>/edit/", methods=["POST"])
@requires_roles("Administrador")
def edit_user(user_id: int) -> Response:
    """Modifica los datos de un usuario en la base de datos."""
    # Obtiene los datos del formulario
    id_number = request.form.get("id-number")
    username = request.form.get("username")
    names = request.form.get("names")
    surnames = request.form.get("surnames")
    role = request.form.get("role")

    try:
        profiles.edit_user(user_id, id_number, username, names, surnames, role)

        # Si el usuario editado es el mismo que está logueado, cambia su sesión
        if user_id == session["id"]:
            session["username"] = username
    except profiles.ProfileError as e:
        flash(f"{e}")
        return redirect(url_for("users_profiles"))

    # Se permanece en la página
    flash("Usuario editado exitosamente")
    return redirect(url_for("users_profiles"))


# ========== Logger ==========
@current_app.route("/event-logger/", methods=["GET", "POST"])
@requires_roles("Administrador")
def logger() -> Response:
    if request.method == "POST":
        # Obtiene los datos del formulario
        event = request.form.get("event-filter").lower().strip()

        # SELECT * FROM event JOIN user ON event.user_id = user.id
        stmt = db.select(Event).join(User, Event.user_id == User.id)
        if event:
            # WHERE description LIKE '%event%' OR
            #     module LIKE '%event%' OR
            #     user.username LIKE '%event%'
            stmt = stmt.where(
                db.or_(
                    Event.description.like(f"%{event}%"),
                    Event.module.like(f"%{event}%"),
                    db.func.lower(User.username).like(f"%{event}%"),
                )
            )

            # Añade el evento de búsqueda
            events.add_event("Logger de Eventos", f"Buscar '{event}'")
    else:
        # Selecciona los eventos de la base de datos
        stmt = db.select(Event)

    result = db.session.execute(stmt).fetchall()
    _events = [r for r, in result]
    return render_template("admin/logger.html", events=_events)


@current_app.route("/event-logger/delete/<int:event_id>/", methods=["POST"])
@requires_roles("Administrador")
def delete_event(event_id: int) -> Response:
    """Elimina un evento de la base de datos."""
    try:
        events.delete_event(event_id)
    except events.EventError as e:
        flash(f"{e}")
        return redirect(url_for("logger"))

    flash("Evento eliminado exitosamente")
    return redirect(url_for("logger"))


# ========== Departamentos del taller ==========
@current_app.route("/workshop-departments/", methods=["GET", "POST"])
@requires_roles("Administrador")
def ws_depts() -> Response:
    """Muestra la lista de departamentos del taller anadidos en el sistema."""
    # SELECT * FROM department
    stmt = db.select(Department)

    if request.method == "POST":
        # Obtiene los datos del formulario
        dept = request.form.get("dept-filter").lower().strip()

        if dept:
            # WHERE description LIKE '%dept%'
            stmt = stmt.where(Department.description.like(f"%{dept}%"))

        # Añade el evento de búsqueda
        events.add_event("Departamentos del Taller", f"Buscar '{dept}'")

    result = db.session.execute(stmt).fetchall()
    _depts = [r for r, in result]

    return render_template("admin/departments.html", departments=_depts)


@current_app.route("/workshop-departments/register/", methods=["POST"])
@requires_roles("Administrador")
def register_dept() -> Response:
    """Registra un departamento en la base de datos."""
    description = request.form.get("description")

    try:
        departments.register_dept(description)
    except departments.DepartmentError as e:
        flash(f"{e}")
        return redirect(url_for("ws_depts"))

    # Se permanece en la página
    flash("Departamento añadido exitosamente")
    return redirect(url_for("ws_depts"))


@current_app.route("/workshop-departments/delete/<int:dept_id>/", methods=["POST"])
@requires_roles("Administrador")
def delete_dept(dept_id: int) -> Response:
    """Elimina un departamento de la base de datos."""
    try:
        departments.delete_dept(dept_id)
    except departments.DepartmentError as e:
        flash(f"{e}")
        return redirect(url_for("ws_depts"))

    # Se permanece en la página
    flash("Departamento eliminado exitosamente")
    return redirect(url_for("ws_depts"))


@current_app.route("/workshop-departments/edit/<int:dept_id>/", methods=["POST"])
@requires_roles("Administrador")
def edit_dept(dept_id: int) -> Response:
    """Modifica un departamento en la base de datos"""
    description = request.form.get("description")

    try:
        departments.edit_dept(dept_id, description)
    except departments.DepartmentError as e:
        flash(f"{e}")
        return redirect(url_for("ws_depts"))

    # Se permanece en la página
    flash("Departamento modificado exitosamente")
    return redirect(url_for("ws_depts"))
