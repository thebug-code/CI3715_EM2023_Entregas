from datetime import date

from SAGTMA.models import Project, db
from SAGTMA.utils import events
from datetime import date


class ProjectError(ValueError):
    pass


# ========== Validaciones ==========
def validate_descrip_project(description: str) -> bool:
    """
    Lanza una excepción si la descripción de un proyecto no es valida.

    Una descripción de un proyecto es válida si:
      -Tiene al menos 6 caracteres y a lo sumo 100 caracteres
      -No tiene caracteres especiales distintos de ' -_?¿¡!:'
    """
    if len(description) < 6 or len(description) > 100:
        raise ProjectError(
            "La descripción del proyecto debe tener entre 6 y 100 caracteres."
        )

    for char in description:
        if not char.isalnum() and char not in " -_?¿¡!:.,":
            raise ProjectError(
                "La descripción de un proyecto no puede contener caracteres especiales."
            )


def validate_date(start_date: date, deadline: date) -> bool:
    """
    Lanza una excepción si la fecha de inicio de un proyecto es despues que su fecha de cierre
    """

    if start_date > deadline:
        raise ProjectError(
            "La fecha de inicio no puede ser mayor que la fecha de cierre."
        )


# ========== Registro de Proyectos ==========
def create_project(description: str, start_date: str, deadline: str):
    """
    Crea y anade un usuario en la base de datos.

    Lanza una excepción ProyectError si hubo algún error.
    """
    # Eliminar espacios al comienzo y final de la descripción
    description = description.strip()
    start_date = start_date.strip()
    deadline = deadline.strip()

    # Verifica que todos los campos estén completos
    if not all([description, start_date, deadline]):
        raise ProjectError("Todos los campos son obligatorios")

    # Verifica si ya existe un proyecto con la misma descripción
    stmt = db.select(Project).where(Project.description == description)
    if db.session.execute(stmt).first():
        raise ProjectError("El proyecto ya existe")

    # Convert fechas a tipo Date usando la libreria datetime
    y, m, d = start_date.split("-")
    start_date_t = date(int(y), int(m), int(d))

    y, m, d = deadline.split("-")
    deadline_t = date(int(y), int(m), int(d))

    # Chequea si los campos ingresados son válidos
    validate_descrip_project(description)
    validate_date(start_date_t, deadline_t)

    # Crea el proyecto en la base de datos
    new_project = Project(description, start_date_t, deadline_t)
    db.session.add(new_project)

    # Registra el evento en la base de datos
    events.add_event(
        "Portafolio de Proyectos", f"Agregar proyecto '{new_project.description}'"
    )


# ========== Modification de Proyectos ==========
def edit_project(project_id: int, description: str, start_date: str, deadline: str):
    """
    Modifica los datos de un proyecto en la base de datos

    Lanza una excepción ProyectError si hubo algún error.
    """
    # Elimina espacios al comienzo y final del input del form
    description = description.strip()
    start_date = start_date.strip()
    deadline = deadline.strip()

    # Verifica que todos los campos estén completos
    if not all([description, start_date, deadline]):
        raise ProjectError("Todos los campos son obligatorios")

    # Verifica si ya existe un proyecto con la misma descripción
    stmt = (
        db.select(Project)
        .where(Project.description == description)
        .where(Project.id != project_id)
    )
    if db.session.execute(stmt).first():
        raise ProjectError("El proyecto ya existe")

    # Selecciona el proyecto con el id indicado y verifica que exista
    stmt = db.select(Project).where(Project.id == project_id)
    project_query = db.session.execute(stmt).first()
    if not project_query:
        raise ProjectError("El proyecto indicado no existe")
    edited_project = project_query[0]

    # Convert fechas a tipo Date usando la libreria datetime
    y, m, d = start_date.split("-")
    start_date_t = date(int(y), int(m), int(d))

    y, m, d = deadline.split("-")
    deadline_t = date(int(y), int(m), int(d))

    # Chequea si los campos ingresados son válidos
    validate_descrip_project(description)
    validate_date(start_date_t, deadline_t)

    # Actualiza los datos del proyecto
    edited_project.description = description
    edited_project.start_date = start_date_t
    edited_project.end_date = deadline_t

    # Registra el evento en la base de datos
    events.add_event("Portafolio de Proyectos", f"Modificar '{description.strip()}'")


# ========== Eliminación de Proyectos ==========
def delete_project(project_id: int):
    """
    Elimina un proyecto de la base de datos

    Lanza una excepción ProyectError si hubo algún error.
    """
    # Selecciona el proyecto con el id indicado y verifica que exista
    stmt = db.select(Project).where(Project.id == project_id)
    project_query = db.session.execute(stmt).first()
    if not project_query:
        raise ProjectError("El proyecto indicado no existe")
    deleted_project = project_query[0]

    # Elimina el proyecto
    db.session.delete(deleted_project)

    # Registra el evento en la base de datos
    events.add_event("Portafolio de Proyectos", f"Eliminar '{deleted_project.description}'")


# ========== Cambio de estado de Proyectos ==========
def toggle_project_status(project_id: int):
    """
    Cambia el estado de un proyecto de la base de datos.

    Lanza una excepción ProyectError si hubo algún error.
    """
    # Selecciona el proyecto con el id indicado y verifica que exista
    stmt = db.select(Project).where(Project.id == project_id)
    project_query = db.session.execute(stmt).first()
    if not project_query:
        raise ProjectError("El proyecto indicado no existe")
    project = project_query[0]

    # Cambia el estado del proyecto
    project.state = not project.state

    # Determina el nuevo estado del proyecto
    state = "Activo" if project.state else "Inactivo"

    # Registra el evento en la base de datos
    events.add_event(
        "Portafolio de Proyectos",
        f"Cambiar estado de '{project.description}' a '{state}'",
    )
