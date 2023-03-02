from flask import session

from SAGTMA.models import Event, db
from SAGTMA.utils import auth

# Modulo usuario
def add_register(username: str):
    _add_event('Perfiles de Usuarios', f"Agregar usuario '{username}'")

def add_search_user(search: str, role: str):
    _add_event(
        'Perfiles de Usuarios',
        f"Buscar '{search}' en " + ('todos los roles' if not role else f"el rol '{role}'")
    )

# Modulo proyecto
def add_project(description: str):
    _add_event('Portafolio de proyectos', f"Agregar proyecto '{description}'")

def add_search_project(search: str):
    _add_event('Portafolio de proyectos', f"Buscar '{search}'")

def add_modify_project(description: str):
    _add_event('Portafolio de proyectos', f"Modificar '{description}'")
    
# Modulo evento
def add_search_log(search: str):
    _add_event('Logger de Eventos', f"Buscar '{search}'")

def _add_event(module: str, description: str):
    '''Crea y anade un nuevo a la base de datos'''
    current_user = auth.get_current_user(session['id'])
    new_event = Event(
        current_user,
        module,
        description
    )
    db.session.add(new_event)
    db.session.commit()

