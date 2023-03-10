from flask import (
    Response,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from SAGTMA.utils import clients, events, vehicles
from SAGTMA.utils.decorators import login_required, requires_roles

from SAGTMA.models import Client, Vehicle, db


# ========== CLIENTES ==========


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
    """Registra un vehiculo de un cliente en la base de datos."""
    license_plate = request.form.get("license-plate")
    brand = request.form.get("brand")
    model = request.form.get("model")
    year = request.form.get("year")
    body_number = request.form.get("body-number")
    engine_number = request.form.get("engine-number")
    color = request.form.get("color")
    problem = request.form.get("problem")

    try:
        client_id = vehicles.register_client_vehicle(
                  client_id,
                  license_plate,
                  brand, 
                  model, 
                  year, 
                  body_number,
                  engine_number, 
                  color, 
                  problem)
    except vehicles.VehicleError as e:
        flash(f"{e}")
        return redirect(url_for("client_details"))

    # Se permanece en la página
    flash("Vehiculo añadido exitosamente")
    return redirect(url_for("client_vehicles", client_id=client_id))


@current_app.route("/client-details/<int:vehicle_id>/modify/", methods=["POST"])
@login_required
@requires_roles("Analista de Operaciones")
def modify_client_vehicle(vehicle_id) -> Response:
    """Modifica los datos de un vehiculo de un cliente de la base de datos"""
    license_plate = request.form.get("license-plate")
    brand = request.form.get("brand")
    model = request.form.get("model")
    year = int(request.form.get("year"))
    body_number = request.form.get("body-number")
    engine_number = request.form.get("engine-number")
    color = request.form.get("color")
    problem = request.form.get("problem")

    try:
        client_id = vehicles.modify_vehicle(
                  vehicle_id,
                  license_plate,
                  brand, 
                  model, 
                  year, 
                  body_number,
                  engine_number, 
                  color, 
                  problem)
    except vehicles.VehicleError as e:
        # El vehiculo indicado no existe
        flash(f"{e}")
        return redirect(url_for("client_details"))


    # Se permanece en la pagina
    flash("Vehiculo modificado exitosamente")
    return redirect(url_for("client_vehicles", client_id=client_id))


@current_app.route("/client-details/<int:vehicle_id>/delete/", methods=["POST"])
@login_required
@requires_roles("Analista de Operaciones")
def delete_client_vehicle(vehicle_id) -> Response:
    """Elimina un vehiculo de un cliente de la base de datos"""

    try:
        client_id = vehicles.delete_vehicle(vehicle_id)
    except vehicles.VehicleError as e:
        # El vehiculo indicado no existe
        flash(f"{e}")
        return redirect(url_for("client_details"))


    # Se permanece en la pagina
    flash("Vehiculo eliminado exitosamente")
    return redirect(url_for("client_vehicles", client_id=client_id))
