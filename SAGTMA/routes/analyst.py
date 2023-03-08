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
from SAGTMA.utils.decorators import requires_roles

from SAGTMA.models import Client, Vehicle, db


# ========== CLIENTES ==========


@current_app.route("/clients-details/", methods=["GET", "POST"])
@requires_roles("Analista de Operaciones")
def clients_details() -> Response:
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

    return render_template("analyst/clients.html", clients=_clients)


@current_app.route("/clients-details/register/", methods=["POST"])
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
            id_number, names, surnames, phone_number, email, address
        )
    except clients.ClientError as e:
        flash(f"{e}")

    # Se permanece en la página
    flash("Cliente añadido exitosamente")
    return redirect(url_for("clients_details"))


# ========== VEHÍCULOS ==========

colors = [
    "Amarillo",
    "Azul",
    "Blanco",
    "Café",
    "Gris",
    "Morado",
    "Negro",
    "Naranja",
    "Rojo",
    "Verde",
]


@current_app.route("/clients-details/<int:client_id>/", methods=["GET", "POST"])
@requires_roles("Analista de Operaciones")
def client_vehicles(client_id: int) -> Response:
    """Muestra la lista de clientes añadidos en el sistema"""
    # Obtiene los datos del cliente
    stmt = db.select(Client).where(Client.id == client_id)
    result = db.session.execute(stmt).fetchone()
    client = result[0]  # Verificar que no sea None

    # Obtiene los vehículos del cliente
    stmt = db.select(Vehicle).where(Vehicle.owner_id == client_id)

    if request.method == "POST":
        # Obtiene los datos del formulario
        vehicle = request.form.get("vehicle-filter")

        if vehicle:
            # WHERE (license_plate) LIKE '%vehicle%' OR
            #     (brand || model) LIKE '%vehicle%' OR
            #     color LIKE '%vehicle%' OR
            #     body_number LIKE '%vehicle%' OR
            #     engine_number LIKE '%vehicle%' OR
            #     problem LIKE '%vehicle%'
            stmt = stmt.where(
                db.or_(
                    Vehicle.license_plate.like(f"%{vehicle}%"),
                    db.func.lower(Vehicle.brand + " " + Vehicle.model).like(
                        f"%{vehicle}%"
                    ),
                    Vehicle.color.like(f"%{vehicle}%"),
                    Vehicle.body_number.like(f"%{vehicle}%"),
                    Vehicle.engine_number.like(f"%{vehicle}%"),
                    Vehicle.problem.like(f"%{vehicle}%"),
                )
            )

        # Añade el evento de búsqueda
        events.add_search_vehicle(vehicle, client.names, client.surnames)

    result = db.session.execute(stmt).fetchall()
    _vehicles = [r for r, in result]

    return render_template(
        "analyst/cars.html", vehicles=_vehicles, client=client, colors=colors
    )


@current_app.route("/clients-details/<int:client_id>/register/", methods=["POST"])
@requires_roles("Analista de Operaciones")
def register_client_vehicle(client_id: int) -> Response:
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
            id_number, names, surnames, phone_number, email, address
        )
    except clients.ClientError as e:
        flash(f"{e}")

    # Se permanece en la página
    flash("Cliente añadido exitosamente")
    return redirect(url_for("clients_details"))
