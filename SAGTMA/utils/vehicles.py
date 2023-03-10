from datetime import date

from SAGTMA.models import Vehicle, Client, db
from SAGTMA.utils import events
from datetime import date


# ========== Excepciones ==========
class VehicleError(ValueError):
    pass


class AlreadyExistingVehicleError(VehicleError):
    pass


class MissingFieldError(VehicleError):
    pass


class VehicleNotFoundError(VehicleError):
    pass


# ========== Validaciones ==========

# ========== Registro de Vehiculos ==========
def register_client_vehicle(
        client_id: int,
        license_plate: str, 
        brand: str, 
        model: str, 
        year: str, 
        body_number: str,
        engine_number: str, 
        color: str, 
        problem: str
) -> int:
    """
    Registra un vehiculo de un cliente de la base de datos

    Lanza una excepción VehicleError si hubo algún error.
    """
    # Elimina espacios al comienzo y final del input del form
    license_plate = license_plate.strip()
    brand = brand.strip()
    model = model.strip()
    year = year.strip()
    body_number = body_number.strip()
    engine_number = engine_number.strip()
    color = color.strip()
    problem = problem.strip()

    # Verifica si no hay campos vacios
    if not all([
                license_plate, 
                brand, 
                model, 
                year,
                body_number,
                engine_number, 
                color, 
                problem]
    ):
        raise MissingFieldError("Todos los campos son obligatorios")

    # ---------------------------------
    # FALTA VERIFICAR TODOS LOS PARAMETROS
    # ---------------------------------

    # Verifica si ya existe un vehiculo con la misma placa
    stmt = db.select(Vehicle).where(Vehicle.license_plate == license_plate)
    if db.session.execute(stmt).first():
        raise AlreadyExistingVehicleError("El vehiculo indicado ya existe")

    # Crea el Vehiculo en la base de datos
    new_vehicle = Vehicle(
                license_plate, 
                brand, 
                model, 
                year, 
                body_number, 
                engine_number,
                color, 
                problem)

    # Busca al cliente y le anade su nuevo vehiculo
    stmt = db.select(Client).where(Client.id == client_id)
    client_query = db.session.execute(stmt).first()
    client_query[0].vehicles.append(new_vehicle)

    # Registra el evento en la base de datos
    events.add_vehicle(
            new_vehicle.brand, 
            new_vehicle.owner.names, 
            new_vehicle.owner.surnames
    )
    
    return new_vehicle.owner.id


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
        problem: str
) -> int:
    """
    Modifica los datos un vehiculo de un cliente de la base de datos

    Lanza una excepción VehicleError si hubo algún error.
    """
    print("fjffjfjfjfjfj")

    # Elimina espacios al comienzo y final del input del form
    license_plate = license_plate.strip()
    brand = brand.strip()
    model = model.strip()
    body_number = body_number.strip()
    engine_number = engine_number.strip()
    color = color.strip()
    problem = problem.strip()

    # Verifica si no hay campos vacios
    if not all([
                license_plate, 
                brand, 
                model, 
                year,
                body_number,
                engine_number, 
                color, 
                problem]
    ):
        raise MissingFieldError("Todos los campos son obligatorios")

    # ---------------------------------
    # FALTA VERIFICAR TODOS LOS PARAMETROS
    # ---------------------------------

    # Verifica si ya existe un vehiculo con la misma placa
    stmt = (
        db.select(Vehicle)
        .where(Vehicle.license_plate == license_plate)
        .where(Vehicle.id != vehicle_id)
    )
    if db.session.execute(stmt).first():
        raise AlreadyExistingVehicleError("El vehiculo ya existe")

    # Busca el vehiculo con el id indicado y verifica si existe
    stmt = db.select(Vehicle).where(Vehicle.id == vehicle_id)
    vehicle_query = db.session.execute(stmt).first()
    if not vehicle_query:
        raise VehicleNotFoundError("El vehiculo indicado no existe")

    # Actualiza los datos del vehiculo
    vehicle_query[0].license_plate = license_plate
    vehicle_query[0].brand = brand
    vehicle_query[0].model = model
    vehicle_query[0].year = year
    vehicle_query[0].body_number = body_number
    vehicle_query[0].engine_number = engine_number
    vehicle_query[0].color = color
    vehicle_query[0].problem = problem

    # Registra el evento en la base de datos
    events.add_modify_vehicle(
        vehicle_query[0].brand, 
        vehicle_query[0].owner.names,
        vehicle_query[0].owner.surnames)

    return vehicle_query[0].owner.id


def delete_vehicle(vehicle_id: int) -> int:
    """
    Elimina un vehiculo de un cliente de la base de datos

    Lanza una excepción VehicleError si hubo algún error.
    """
    # Busca el vehiculo con el id indicado y verifica si existe
    stmt = db.select(Vehicle).where(Vehicle.id == vehicle_id)
    result = db.session.execute(stmt).first()
    if not result:
        raise VehicleNotFoundError("El vehiculo indicado no existe")
    
    client_id = result[0].owner.id 

    # Elimina el vehiculo de la base de datos
    db.session.delete(result[0])

    # Registra el evento en la base de datos
    events.add_delete_vehicle(
        result[0].brand, 
        result[0].owner.names, 
        result[0].owner.surnames
    )

    return client_id
