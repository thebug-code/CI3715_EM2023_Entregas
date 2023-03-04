from flask import Response, abort, current_app, redirect, session, url_for

from SAGTMA.utils.decorators import login_required

dispatcher = {
    "Administrador": "users_profiles",
    "Gerente de Operaciones": "portfolio",
    "Analista de Operaciones": "clients_details",
}


@current_app.route("/")
@login_required
def home() -> Response:
    """Redirige a la página principal según el rol del usuario"""
    user_role = session["role"]
    if user_role in dispatcher:
        return redirect(url_for(dispatcher[user_role]))

    # Retorna error de acceso denegado si el usuario tiene un rol no implementado
    abort(403)
