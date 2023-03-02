from typing import Tuple
from datetime import date

import bcrypt

from SAGTMA.models import Project, User, db
from SAGTMA.utils import events


# ========== Excepciones ==========
class CreateProjectError(ValueError):
    pass

class AlreadyExistingProjectError(CreateProjectError):
    pass

class InvalidDescripProjectError(CreateProjectError):
    pass

class InvalidProjectDate(CreateProjectError):
    pass

class MissingFieldError(CreateProjectError):
    pass

# ========== Validaciones ==========
def validate_descrip_project(description: str) -> bool:
    '''Lanza una excepción si la descripcion de un proyecto no es valida.

    Una descripcion de un proyecto es válida si:
      -Tiene al menos 10 caracteres y a lo sumo 200 caracteres
      -No tiene caracteres especiales distintos de '_' (guión bajo)
      -No comienza con un caracter numérico
    '''
    if len(description) < 10 or len(description) > 200:
            raise InvalidDescripProjectError('La descripcion del proyecto debe tener entre 10 y 200 caracteres.')

    if description[0].isdigit():
        raise InvalidDescripProjectError('La descripcion de un proyecto no puede comenzar con un número.')

    for char in description:
        if not char.isalnum() and char != '_' and char != ' ':
            raise InvalidDescripProjectError('La descripcion de un proyeto no puede contener caracteres especiales.')

# Falta tipo de parametro
def validate_date(start_date, deadline) -> bool:
    '''Lanza una excepción si la fecha de inicio de un proyecto es despues que su fecha de cierre'''

    if start_date > deadline:
        raise InvalidProjectDate('La fecha de inicio no puede ser mayor que la fecha de cierre.')

# ========== Anadidura ==========
# Falta tipo de parametro
def create_project(
    description: str,
    start_date,
    deadline
):
    '''Crea y anade un usuario en la base de datos.

    Lanza una excepción CreateProyectError si hubo algún error.
    '''
    if not all([description, start_date, deadline]):
        raise MissingFieldError('Todos los campos son obliglatorios')

    # Verifica si ya existe un proyecto con la mima descripcion
    stmt = db.select(Project).where(Project.description == description)
    if db.session.execute(stmt).first():
        raise AlreadyExistingProjectError('El proyecto ya existe')
    
    # Eliminar espacios al comienzo y final de la descripcion
    description = description.strip()

    # Convert fechas a tipo Date
    y, m, d = start_date.split('-')
    start_date_t = date(int(y), int(m), int(d))

    y, m, d = deadline.split('-')
    deadline_t = date(int(y), int(m), int(d))

    # Chequea si los campos ingresados son válidos
    validate_descrip_project(description)
    validate_date(start_date_t, deadline_t)

    # Crea el proyecto en la base de datos
    new_project = Project(description, start_date_t, deadline_t)
    db.session.add(new_project)

    # Registra el evento en la base de datos
    events.add_project(new_project.description)

# ========== Modificar ==========
def modify_project(
    project_id: int, 
    description: str, 
    start_date, 
    deadline
):
    '''Modifica los datos de un proyecto en la base de datos
        
    Lanza una excepción CreateProyectError si hubo algún error.
    '''
    if not all([description, start_date, deadline]):
        raise MissingFieldError('Todos los campos son obliglatorios')

    # Verifica si ya existe un proyecto con la mima descripcion
    stmt = db.select(Project).where(Project.description == description)
    if db.session.execute(stmt).first():
        raise AlreadyExistingProjectError('El proyecto ya existe')

    # Busca el proyecto con el id indicado
    stmt = db.select(Project).where(Project.id == project_id)
    project_query = db.session.execute(stmt).first()
    if not project_query:
        raise InvalidProjectError('El proyecto indicado no existe')

    # Convert fechas a tipo Date
    y, m, d = start_date.split('-')
    start_date_t = date(int(y), int(m), int(d))

    y, m, d = deadline.split('-')
    deadline_t = date(int(y), int(m), int(d))

    # Chequea si los campos ingresados son válidos
    validate_descrip_project(description)
    validate_date(start_date_t, deadline_t)

    # Actualiza los datos del proyecto
    project_query[0].description = description.strip() 
    project_query[0].start_date = start_date_t
    project_query[0].end_date = deadline_t

    # Registra el evento en la base de datos
    events.add_modify_project(new_project.description)

    db.session.commit()
