from datetime import date

from SAGTMA.models import Vehicle, db
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

# ========== Eliminacion de vehiculos ==========
def delete_vehicle(vehicle_id: int):
    """
    Elimina un vehiculo de un cliente de la base de datos

    Lanza una excepción VehicleError si hubo algún error.
    """
    # Busca el vehiculo con el id indicado y verifica si existe
    stmt = db.select(Vehicle).where(Vehicle.id == vehicle_id)
    result = db.session.execute(stmt).first()
    if not result:
        raise VehicleNotFoundError("El vehiculo indicado no existe")

    # Elimina el vehiculo de la base de datos
    db.session.delete(result[0])

    # Registra el evento en la base de datos
    events.add_delete_vehicle(
        result[0].brand, result[0].owner.names, result[0].owner.surnames
    )
