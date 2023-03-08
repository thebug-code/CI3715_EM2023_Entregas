from flask import (
    Response,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from SAGTMA.utils import clients, events
from SAGTMA.utils.decorators import login_required, requires_roles

from SAGTMA.models import Client, db


@current_app.route("/client-details/", methods=["GET", "POST"])
@requires_roles("Analista de Operaciones")
def client_details() -> Response:
    """Muestra la lista de clientes añadidos en el sistema"""
    # SELECT * FROM client
    stmt = db.select(Client)

    if request.method == "POST":
        # Obtiene los datos del formulario
        client = request.form.get("client-filter")

        if client:
            # WHERE (names || surnames) LIKE '%client%' OR
            #     id_number LIKE '%client%' OR
            #     phone_number LIKE '%client%' OR
            #     email LIKE '%client%' OR
            #     address LIKE '%client%'
            stmt = stmt.where(
                db.or_(
                    db.func.lower(Client.names + " " + Client.surnames).like(
                        f"%{client}%"
                    ),
                    Client.id_number.like(f"%{client}%"),
                    Client.phone_number.like(f"%{client}%"),
                    Client.email.like(f"%{client}%"),
                    Client.address.like(f"%{client}%"),
                )
            )

        # Añade el evento de búsqueda
        events.add_search_client(client)

    result = db.session.execute(stmt).fetchall()
    _clients = [r for r, in result]
    print(_clients)

    return render_template("analyst/clients.html", clients=_clients)


@current_app.route("/client-details/register/", methods=["POST"])
@requires_roles("Analista de Operaciones")
def register_client() -> Response:
    """Registra un cliente en la base de datos."""
    id_number = request.form.get("id-number")
    names = request.form.get("names")
    surnames = request.form.get("surnames")
    birthdate = request.form.get("birthdate")
    phone_number = request.form.get("phone-number")
    email = request.form.get("email")
    address = request.form.get("address")

    try:
        clients.register_client(
            id_number, names, surnames, birthdate, phone_number, email, address
        )
    except clients.ClientError as e:
        flash(f"{e}")

    # Se permanece en la página
    flash("Cliente añadido exitosamente")
    return redirect(url_for("client_details"))


@current_app.route("/client-details/modify/<int:client_id>/", methods=["POST"])
@login_required
@requires_roles("Analista de Operaciones")
def modify_client(client_id):
    """Modifica los datos de un cliente en la base de datos"""
    id_number = request.form.get("id-number")
    names = request.form.get("names")
    surnames = request.form.get("surnames")
    birthdate = request.form.get("birthdate")
    phone_number = request.form.get("phone-number")
    email = request.form.get("email")
    address = request.form.get("address")

    try:
        clients.modify_client(
            client_id, id_number, names, surnames, birthdate, \
                phone_number, email, address
        )
    except clients.ClientError as e:
        flash(f"{e}")

    # Se permanece en la página
    flash("Cliente modificado exitosamente")
    return redirect(url_for("client_details"))

@current_app.route("/client-details/delete/<int:client_id>/", methods=["POST"])
@login_required
@requires_roles("Analista de Operaciones")
def delete_client(client_id) -> Response:
    """Elimina un cliente de la base de datos"""
    try:
        clients.delete_client(client_id)
    except clients.ClientError as e:
        flash(f"{e}")

    # Se permanece en la pagina
    flash("Cliente eliminado exitosamente")
    return redirect(url_for("client_details"))
