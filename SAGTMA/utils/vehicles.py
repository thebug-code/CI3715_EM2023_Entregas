from datetime import date

from SAGTMA.models import Vehicle, Client, db
from SAGTMA.utils import events
from datetime import date
from SAGTMA.utils.profiles import validate_names


# ========== Excepciones ==========
class VehicleError(ValueError):
    pass


class AlreadyExistingVehicleError(VehicleError):
    pass


class MissingFieldError(VehicleError):
    pass


class VehicleNotFoundError(VehicleError):
    pass


class InvalidLicensePlateError(VehicleError):
    pass


class InvalidSerialNumberError(VehicleError):
    pass


class InvalidColorError(VehicleError):
    pass


class InvalidYearError(VehicleError):
    pass


# ========== Validaciones ==========
def validate_license_plate(license_plate: str) -> bool:
    """Lanza una excepción si la placa de un vehiculo no es válida.

    Una placa es válida si:
      -Tiene al menos 5 caracteres y a lo sumo 10 caracteres
      -No tiene caracteres especiales distintos de '- ' (guión y espacio)
      -No tiene espacios/guiones consecutivos
    """
    if len(license_plate) < 5 or len(license_plate) > 10:
        raise InvalidLicensePlateError("La placa debe tener entre 5 y 10 caracteres")

    if not license_plate[0].isalpha():
        raise InvalidLicensePlateError(
            "La placa debe comenzar con un caracter alfanumérico"
        )

    # Chequea que no haya caracteres especiales más que guiones o espacios, y que no haya espacios consecutivos
    for i, char in enumerate(license_plate):
        if not char.isalnum() and char not in "- ":
            raise InvalidLicensePlateError(
                "La placa solo puede contener caracteres alfanuméricos, guiones y espacios"
            )
        if char in "- " and license_plate[i - 1] in "- ":
            raise InvalidLicensePlateError(
                "La placa no puede contener espacios/guiones consecutivos"
            )


def validate_serial_number(serial_number: str):
    """Lanza una excepción si el número de serie no es válido.

    Un número de serie es válido si:
      -Tiene al menos 5 caracteres y a lo sumo 20 caracteres
      -Solo tiene caracteres alfanuméricos o guiones
    """
    if len(serial_number) < 5 or len(serial_number) > 20:
        raise InvalidSerialNumberError(
            "El número de serie debe tener entre 5 y 20 caracteres"
        )

    for char in serial_number:
        if not char.isalnum() and char != "-":
            raise InvalidSerialNumberError(
                "El número de serie solo puede contener caracteres alfanuméricos y guiones"
            )

        if char in "- " and serial_number[i - 1] in "- ":
            raise InvalidSerialNumberError(
                "La placa no puede contener espacios/guiones consecutivos"
            )


def validate_color(color: str):
    """Lanza una excepción si el color no es válido.

    Un color es válido si:
      -Tiene al menos 2 caracteres y a lo sumo 20 caracteres
      -Solo tiene caracteres alfanuméricos o espacios
    """
    if len(color) < 2 or len(color) > 20:
        raise InvalidColorError("El color debe tener entre 2 y 20 caracteres")

    for char in color:
        if not char.isalnum() and char != " ":
            raise InvalidColorError(
                "El color solo puede contener caracteres alfanuméricos y espacios"
            )


def validate_year(year: int):
    """Lanza una excepción si el año no es válido.

    Un año es válido si:
      -Es un número entero
      -Es menor o igual al año actual
    """
    if year < 1900 or year > date.today().year + 1:
        raise InvalidYearError(
            "El año debe ser un número entero entre 1900 y el año actual + 1"
        )


# ========== Registro de Vehiculos ==========
def register_client_vehicle(
    client_id: int,
    license_plate: str,
    brand: str,
    model: str,
    year: int,
    body_number: str,
    engine_number: str,
    color: str,
    problem: str,
) -> int:
    """
    Registra un vehiculo de un cliente de la base de datos

    Lanza una excepción VehicleError si hubo algún error.
    """
    # Elimina espacios al comienzo y final del input del form
    license_plate = license_plate.strip()
    brand = brand.strip()
    model = model.strip()
    body_number = body_number.strip()
    engine_number = engine_number.strip()
    problem = problem.strip()

    # Verifica si no hay campos vacios
    if not all(
        [license_plate, brand, model, year, body_number, engine_number, color, problem]
    ):
        raise MissingFieldError("Todos los campos son obligatorios")

    # Chequea si los campos son válidos
    validate_license_plate(license_plate)
    validate_names(brand)
    validate_names(model)
    validate_serial_number(body_number)
    validate_serial_number(engine_number)
    validate_color(color)
    validate_year(year)

    if len(problem) > 120:
        raise VehicleError(
            "La descripción del problema no puede tener más de 120 caracteres"
        )

    # Verifica si ya existe un vehiculo con la misma placa
    stmt = db.select(Vehicle).where(Vehicle.license_plate == license_plate)
    if db.session.execute(stmt).first():
        raise AlreadyExistingVehicleError("El vehículo indicado ya existe")

    # Crea el Vehiculo en la base de datos
    new_vehicle = Vehicle(
        license_plate, brand, model, year, body_number, engine_number, color, problem
    )

    # Busca al cliente y le añade su nuevo vehiculo
    stmt = db.select(Client).where(Client.id == client_id)
    client_query = db.session.execute(stmt).first()
    client_query[0].vehicles.append(new_vehicle)

    # Registra el evento en la base de datos
    events.add_vehicle(new_vehicle.brand, new_vehicle.owner.id_number)


# ========== Modicar datos de Vehiculos ==========
def modify_vehicle(
    vehicle_id: int,
    license_plate: str,
    brand: str,
    model: str,
    year: int,
    body_number: str,
    engine_number: str,
    color: str,
    problem: str,
):
    """
    Modifica los datos un vehiculo de un cliente de la base de datos

    Lanza una excepción VehicleError si hubo algún error.
    """
    # Elimina espacios al comienzo y final del input del form
    license_plate = license_plate.strip()
    brand = brand.strip()
    model = model.strip()
    body_number = body_number.strip()
    engine_number = engine_number.strip()
    problem = problem.strip()

    # Verifica si no hay campos vacios
    if not all(
        [license_plate, brand, model, year, body_number, engine_number, color, problem]
    ):
        raise MissingFieldError("Todos los campos son obligatorios")

    # Chequea si los campos son válidos
    validate_license_plate(license_plate)
    validate_names(brand)
    validate_names(model)
    validate_serial_number(body_number)
    validate_serial_number(engine_number)
    validate_color(color)
    validate_year(year)

    if len(problem) > 120:
        raise VehicleError(
            "La descripción del problema no puede tener más de 120 caracteres"
        )

    # Verifica si ya existe un vehiculo con la misma placa
    stmt = (
        db.select(Vehicle)
        .where(Vehicle.license_plate == license_plate)
        .where(Vehicle.id != vehicle_id)
    )
    if db.session.execute(stmt).first():
        raise AlreadyExistingVehicleError("El vehículo ya existe")

    # Busca el vehiculo con el id indicado y verifica si existe
    stmt = db.select(Vehicle).where(Vehicle.id == vehicle_id)
    vehicle_query = db.session.execute(stmt).first()
    if not vehicle_query:
        raise VehicleNotFoundError("El vehículo indicado no existe")
    (edited_vehicle,) = vehicle_query

    # Actualiza los datos del vehiculo
    edited_vehicle.license_plate = license_plate
    edited_vehicle.brand = brand
    edited_vehicle.model = model
    edited_vehicle.year = year
    edited_vehicle.body_number = body_number
    edited_vehicle.engine_number = engine_number
    edited_vehicle.color = color
    edited_vehicle.problem = problem

    # Registra el evento en la base de datos
    events.add_modify_vehicle(edited_vehicle.brand, edited_vehicle.owner.id_number)


def delete_vehicle(vehicle_id: int) -> int:
    """
    Elimina un vehiculo de un cliente de la base de datos

    Lanza una excepción VehicleError si hubo algún error.
    """
    # Busca el vehiculo con el id indicado y verifica si existe
    stmt = db.select(Vehicle).where(Vehicle.id == vehicle_id)
    result = db.session.execute(stmt).first()
    if not result:
        raise VehicleNotFoundError("El vehículo indicado no existe")

    # Elimina el vehiculo de la base de datos
    db.session.delete(result[0])

    # Registra el evento en la base de datos
    events.add_delete_vehicle(result[0].brand, result[0].owner.id_number)
