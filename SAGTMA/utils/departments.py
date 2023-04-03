import re

from SAGTMA.models import Department, db
from SAGTMA.utils import events


class DepartmentError(ValueError):
    pass


# ========== Validaciones ==========
def validate_descrip_dept(description: str) -> bool:
    """
    Lanza una excepción si la descripción de un departamento no es válida.

    Una descripción de un departamento es válida si:
      -Tiene al menos 6 caracteres a lo sumo 100 caracteres
      -No tiene caracteres especiales distintos de ' -_?¿¡!:'
    """
    if len(description) < 6 or len(description) > 100:
        raise DepartmentError(
            "La descripción del departamento debe tener entre 6 y 100 caracteres."
        )

    regex = r"^[\w\s\-?¿¡!:.]*$"
    if not re.search(regex, description):
        raise DepartmentError(
            "La descripción del departamento no puede contener caracteres especiales."
        )


# ========== Registro ==========
def register_dept(description: str):
    """
    Crear y añade un departamento a la base de datos.

    Lanza una excepción DepartmentError si hubo algún error.
    """
    # Elimina espacios al comienzo y final del input del form
    description = description.strip()

    if not all([description]):
        raise DepartmentError("Todos los campos son obligatorios")

    # Chequea si la descripción es válida
    validate_descrip_dept(description)

    # Verifica si ya existe un departamento con la misma descripción
    smt = db.select(Department).where(Department.description == description)
    if db.session.execute(smt).first():
        raise DepartmentError("Ya existe un departamento con la misma descripción")

    # Crea el departamento en la base de datos
    new_dept = Department(description)

    db.session.add(new_dept)

    # Registra el evento en la base de datos
    events.add_event(
        "Departamentos del Taller", f"Agregar departamento '{new_dept.description}'"
    )


# ========== Eliminacion de un departamento ==========
def delete_dept(dept_id: int):
    """
    Elimina un departamento de la base de datos

    Lanza una excepción DepartmentError si hubo algún error.
    """
    # Selecciona el departamento con el id indicado y verifica si existe
    stmt = db.select(Department).where(Department.id == dept_id)
    dept_query = db.session.execute(stmt).first()
    if not dept_query:
        raise DepartmentError("El departamento indicado no existe")
    dept = dept_query[0]

    # Elimina el departamento de la base de datos
    db.session.delete(dept)

    # Registra el evento en la base de datos
    events.add_event(
        "Departamentos del Taller", f"Eliminar departamento '{dept.description}'"
    )


# ========== Modificacion de un departamento ==========
def edit_dept(dept_id: int, description: str):
    """
    Modifica un departamento de la base de datos

    Lanza una excepción DepartmentError si hubo algún error.
    """
    # Elimina espacios al comienzo y final del input del form
    description = description.strip()

    if not all([description]):
        raise DepartmentError("Todos los campos son obligatorios")

    # Verifica si ya existe un departamento con la misma descripción
    smt = (
        db.select(Department)
        .where(Department.description == description)
        .where(Department.id != dept_id)
    )
    if db.session.execute(smt).first():
        raise DepartmentError("Ya existe un departamento con la misma descripción")

    # Selecciona el departamento con el id indicado y verifica si existe
    stmt = db.select(Department).where(Department.id == dept_id)
    dept_query = db.session.execute(stmt).first()
    if not dept_query:
        raise DepartmentError("El departamento indicado no existe")
    edited_dept = dept_query[0]

    # Chequea si la descripción es válida
    validate_descrip_dept(description)

    # Modifica el departamento en la base de datos
    edited_dept.description = description

    # Registra el evento en la base de datos
    events.add_event(
        "Departamentos del Taller",
        f"Editar departamento '{edited_dept.description}'",
    )
