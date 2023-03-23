from flask import session

from SAGTMA.models import Event, db
from SAGTMA.utils import profiles


class EventError(ValueError):
    pass

def add_event(module: str, description: str):
    """Crea y anade un nuevo a la base de datos"""
    current_user = profiles.get_current_user(session["id"])
    new_event = Event(current_user, module, description)
    db.session.add(new_event)
    db.session.commit()

def delete_event(event_id: int):
    """Elimina un usuario de la base de datos y"""
    if not event_id:
        raise EventError("El evento indicado no existe")

    # Busca el evento en la base de datos
    stmt = db.select(Event).where(Event.id == event_id)
    result = db.session.execute(stmt).fetchone()
    if not result:
        raise EventError("El evento indicado no existe")
    (deleted_event,) = result

    # Elimina el evento de la base de datos
    db.session.delete(deleted_event)
    db.session.commit()

    # Añade el evento de eliminación
    add_event("Logger de eventos", f"Eliminar '{deleted_event.description}'")
