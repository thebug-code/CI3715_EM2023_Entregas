import re

from SAGTMA.models import MeasureUnit, db
from SAGTMA.utils import events


class MeasureUnitError(ValueError):
    pass


#=========== Validaciones ===========
def validate_dimension(dimension: str) -> float:
    """
    Lanza una excepción si la dimensión no es válida.

    Una dimensión válida es un número decimal positivo.
    """
    
    try:
        dimension = float(dimension)
    except ValueError:
        raise ValueError("La dimensión debe ser un número decimal.")
    
    if dimension <= 0:
        raise ValueError("La dimensión debe ser un número positivo.")
    
    return dimension


def validate_unit(unit: str):
    """
    Lanza una excepcion si la unidad no es válida.

    Una unidad válida es una cadena de texto que contiene al menos un carácter 
    alfabético y no contiene caracteres especiales.
    """

    if not re.search(r"[a-zA-Z]", unit):
        raise ValueError("La unidad solo puede contener caracteres alfabéticos.")


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
        raise ValueError("Todos los campos son obligatorios")

    # Chequea si la dimensión es válida
    dimension = validate_dimension(dimension)

    # Chequea si la unidad es válida
    validate_unit(unit)

    # Verifica si ya existe una unidad de medida con la misma dimensión y unidad
    smt = db.select(MeasureUnit).where(
        MeasureUnit.dimension == dimension and MeasureUnit.unit == unit
    )
    if db.session.execute(smt).first():
        raise ValueError("Ya existe una unidad de medida con la misma dimensión y unidad")

    # Crea la unidad de medida en la base de datos
    new_measure_unit = MeasureUnit(dimension, unit)

    db.session.add(new_measure_unit)

    # Registra el evento en la base de datos
    events.add_event(
        "Unidades de medida", f"Agregar unidad de medida '{new_measure_unit.dimension} {new_measure_unit.unit}'"
    )
