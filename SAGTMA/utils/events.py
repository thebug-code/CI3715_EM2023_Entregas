from flask import session

from SAGTMA.models import Event, db
from SAGTMA.utils import profiles


class EventError(ValueError):
    pass


class InvalidEventError(EventError):
    pass


# ========== Perfiles de Usuarios ==========
def add_register(username: str):
    _add_event("Perfiles de Usuarios", f"Agregar usuario '{username}'")


def add_search_user(search: str, role: str):
    _add_event(
        "Perfiles de Usuarios",
        f"Buscar '{search}' en "
        + ("todos los roles" if not role else f"el rol '{role}'"),
    )


def add_edit_user(username: str):
    _add_event("Perfiles de Usuarios", f"Editar usuario '{username}'")


def add_delete_user(username: str):
    _add_event("Perfiles de Usuarios", f"Eliminar usuario '{username}'")


# ========== Portafolios de Proyectos ==========
def add_project(description: str):
    _add_event("Portafolio de Proyectos", f"Agregar proyecto '{description}'")


def add_search_project(search: str):
    _add_event("Portafolio de Proyectos", f"Buscar '{search}'")


def add_modify_project(description: str):
    _add_event("Portafolio de Proyectos", f"Modificar '{description}'")


def add_delete_project(description: str):
    _add_event("Portafolio de Proyectos", f"Eliminar '{description}'")


# ========== Logger de Eventos ==========
def add_search_log(search: str):
    _add_event("Logger de Eventos", f"Buscar '{search}'")


def delete_event(event_id: int):
    """Elimina un usuario de la base de datos y"""
    if not event_id:
        raise InvalidEventError("El evento indicado no existe")

    # Busca el evento en la base de datos
    stmt = db.select(Event).where(Event.id == event_id)
    result = db.session.execute(stmt).fetchone()
    if not result:
        raise InvalidEventError("El evento indicado no existe")
    (deleted_event,) = result

    # Elimina el evento de la base de datos
    db.session.delete(deleted_event)
    db.session.commit()

    # Añade el evento de eliminación
    _add_event("Logger de eventos", f"Eliminar '{deleted_event.description}'")


# =========== Vehículos de los Clientes ===========
def add_search_vehicle(search: str, client_names: str, client_surnames: str):
    _add_event(
        "Vehículos de los Clientes",
        f"Buscar '{search}' del cliente '{client_names} {client_surnames}'",
    )


# =========== Detalles de los Clientes ===========
def add_search_client(search: str):
    _add_event("Detalles de los Clientes", f"Buscar '{search}'")


# =========== Funciones Auxiliares ==========


def _add_event(module: str, description: str):
    """Crea y anade un nuevo a la base de datos"""
    current_user = profiles.get_current_user(session["id"])
    new_event = Event(current_user, module, description)
    db.session.add(new_event)
    db.session.commit()
