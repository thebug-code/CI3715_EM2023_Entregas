import re

from SAGTMA.models import MeasureUnit, db
from SAGTMA.utils import events


class MeasureUnitError(ValueError):
    pass


# =========== Validaciones ===========
def validate_dimension(dimension: str) -> float:
    """
    Lanza una excepción si la dimensión no es válida.

    Una dimensión válida es un número decimal positivo.
    """

    try:
        dimension = float(dimension)
    except ValueError:
        raise MeasureUnitError("La dimensión debe ser un número decimal.")

    if dimension <= 0:
        raise MeasureUnitError("La dimensión debe ser un número positivo.")

    return dimension


def validate_unit(unit: str):
    """
    Lanza una excepcion si la unidad no es válida.

    Una unidad válida es una cadena de texto que contiene al menos un carácter
    alfabético y no contiene caracteres especiales (excepto el espacio).
    """

    if not re.match(r"^[a-zA-Z ]+$", unit):
        raise MeasureUnitError("La unidad solo puede contener caracteres alfabéticos.")


# ========== Registro ==========
def register_measure_unit(dimension: str, unit: str):
    """
    Crear y añade una unidad de medida a la base de datos.

    Lanza una excepción MeasureUnitError si:
        -La dimensión o la unidad no son válidas.
        -Ya existe una unidad de medida con la misma dimensión y unidad.
    """
    # Elimina espacios al comienzo y final del input del form
    dimension = dimension.strip()
    unit = unit.strip()

    if not all([dimension, unit]):
        raise MeasureUnitError("Todos los campos son obligatorios")

    # Chequea si la dimensión es válida
    dimension = validate_dimension(dimension)

    # Chequea si la unidad es válida
    validate_unit(unit)

    # Verifica si ya existe una unidad de medida con la misma dimensión y unidad
    smt = db.select(MeasureUnit).where(
        MeasureUnit.dimension == dimension and MeasureUnit.unit == unit
    )
    if db.session.execute(smt).first():
        raise MeasureUnitError(
            "Ya existe una unidad de medida con la misma dimensión y unidad"
        )

    # Crea la unidad de medida en la base de datos
    new_measure_unit = MeasureUnit(dimension, unit)

    db.session.add(new_measure_unit)

    # Registra el evento en la base de datos
    events.add_event(
        "Unidades de medida",
        f"Agregar unidad de medida '{new_measure_unit.dimension} {new_measure_unit.unit}'",
    )


# ========== Eliminación ==========
def delete_measure_unit(measure_unit_id: int):
    """
    Elimina una unidad de medida de la base de datos.

    Lanza una excepción MeasureUnitError si:
        -No existe una unidad de medida con el id especificado.
    """

    # Selecciona la unidad de medida con el id especificado y verifica que exista
    smt = db.select(MeasureUnit).where(MeasureUnit.id == measure_unit_id)
    measure_unit_query = db.session.execute(smt).first()
    if not measure_unit_query:
        raise MeasureUnitError("No existe una unidad de medida con el id especificado")
    deleted_measure_unit = measure_unit_query[0]

    # Si está asociado a algún material no se puede eliminar
    if deleted_measure_unit.materials:
        raise MeasureUnitError(
            "No se puede eliminar una unidad de medida asociada a un material."
        )

    # Elimina la unidad de medida de la base de datos
    db.session.delete(deleted_measure_unit)

    # Registra el evento en la base de datos
    events.add_event(
        "Unidades de medida",
        f"Eliminar unidad de medida '{deleted_measure_unit.dimension} {deleted_measure_unit.unit}'",
    )


# ========== Modificación ==========
def edit_measure_unit(measure_unit_id: int, dimension: str, unit: str):
    """
    Modifica una unidad de medida en la base de datos.

    Lanza una excepción MeasureUnitError si:
        -No existe una unidad de medida con el id especificado.
        -La dimensión o la unidad no son válidas.
        -Ya existe una unidad de medida con la misma dimensión y unidad.
    """

    # Elimina espacios al comienzo y final del input del form
    dimension = dimension.strip()
    unit = unit.strip()

    if not all([dimension, unit]):
        raise MeasureUnitError("Todos los campos son obligatorios")

    # Chequea si la dimensión es válida
    dimension = validate_dimension(dimension)

    # Chequea si la unidad es válida
    validate_unit(unit)

    # Selecciona la unidad de medida con el id especificado y verifica que exista
    smt = db.select(MeasureUnit).where(MeasureUnit.id == measure_unit_id)
    measure_unit_query = db.session.execute(smt).first()
    if not measure_unit_query:
        raise MeasureUnitError("No existe una unidad de medida con el id especificado")
    edited_measure_unit = measure_unit_query[0]

    # Verifica si ya existe una unidad de medida con la misma dimensión y unidad
    smt = (
        db.select(MeasureUnit)
        .where(MeasureUnit.dimension == dimension and MeasureUnit.unit == unit)
        .where(MeasureUnit.id != measure_unit_id)
    )
    if db.session.execute(smt).first():
        raise MeasureUnitError(
            "Ya existe una unidad de medida con la misma dimensión y unidad"
        )

    # Modifica la unidad de medida en la base de datos
    edited_measure_unit.dimension = dimension
    edited_measure_unit.unit = unit

    # Registra el evento en la base de datos
    events.add_event(
        "Unidades de medida",
        f"Modificar unidad de medida '{edited_measure_unit.dimension} {edited_measure_unit.unit}'",
    )
