from typing import Tuple

import bcrypt

from SAGTMA.models import Role, User, db
from SAGTMA.utils import events


# ========== Excepciones ==========
class AuthenticationError(ValueError):
    pass

class AlreadyExistingUserError(AuthenticationError):
    pass

class InvalidNameError(AuthenticationError):
    pass

class InvalidUsernameError(AuthenticationError):
    pass

class InvalidPasswordError(AuthenticationError):
    pass

class PasswordMismatchError(AuthenticationError):
    pass

class MissingFieldError(AuthenticationError):
    pass

class UserNotFoundError(AuthenticationError):
    pass

class IncorrectPasswordError(AuthenticationError):
    pass

class InvalidRoleError(AuthenticationError):
    pass

# ========== Validaciones ==========
def validate_username(username: str) -> bool:
    '''Lanza una excepción si el nombre de usuario no es válido.

    Un nombre de usuario es válido si:
      -Tiene al menos 3 caracteres y a lo sumo 20 caracteres
      -No tiene caracteres especiales distintos de '_' (guión bajo)
      -No comienza con un caracter numérico
    '''
    if len(username) < 3 or len(username) > 20:
            raise InvalidUsernameError('El nombre de usuario debe tener entre 3 y 20 caracteres.')

    if username[0].isdigit():
        raise InvalidUsernameError('El nombre de usuario no puede comenzar con un número.')

    for char in username:
        if not char.isalnum() and char != '_':
            raise InvalidUsernameError('El nombre de usuario no puede contener caracteres especiales.')

def validate_names(names: str) -> bool:
    '''Lanza una excepción si el nombre no es válido.

    Un nombre es válido si:
      -Tiene al menos 2 caracteres y a lo sumo 50 caracteres
      -No tiene caracteres especiales distintos de ' ' (espacio)
    '''
    if len(names) < 2 or len(names) > 50:
        raise InvalidNameError('El nombre debe tener entre 2 y 50 caracteres.')

    for char in names:
        if not char.isalnum() and char != ' ':
            raise InvalidNameError('El nombre no puede contener caracteres especiales.')

def validate_password(password: str) -> bool:
    '''Lanza una excepción si la contraseña no es válida.

    La contraseña es válida si:
      -Tiene al menos 6 caracteres y a lo sumo 20 caracteres
      -Tiene al menos un número
      -Tiene al menos una mayúscula y una minúscula
      -Tiene al menos un caracter especial
    '''
    if len(password) < 6 or len(password) > 20:
        raise InvalidPasswordError('La contraseña debe tener entre 6 y 20 caracteres.')

    no_number = True
    no_upper = True
    no_lower = True
    no_special = True
    for char in password:
        if char.isdigit():
            no_number = False
        elif char.isupper():
            no_upper = False
        elif char.islower():
            no_lower = False
        elif not char.isalnum():
            no_special = False

    if no_number:
        raise InvalidPasswordError('La contraseña debe contener al menos un número.')
    elif no_upper or no_lower:
        raise InvalidPasswordError('La contraseña debe contener al menos una mayúscula y una minúscula')
    elif no_special:
        raise InvalidPasswordError('La contraseña debe contener al menos un caracter especial.')

# ========== Registro ==========
def register_user(
    username: str,
    names: str,
    surnames: str,
    password: str,
    confirm_password: str,
    role_id: str
):
    '''Registra un usuario en la base de datos.

    Lanza una excepción AuthenticationError si hubo algún error.
    '''
    if not all([username, names, surnames, password, confirm_password, role_id]):
        raise MissingFieldError('Todos los campos son obliglatorios')

    # Verifica si ya existe un usuario con el mismo nombre de usuario
    stmt = db.select(User).where(User.username == username)
    if db.session.execute(stmt).first():
        raise AlreadyExistingUserError('El nombre de usuario ya existe')

    # Chequea si los campos ingresados son válidos
    validate_username(username)
    validate_names(names)
    validate_names(surnames)
    validate_password(password)

    if password != confirm_password:
        raise PasswordMismatchError('Las contraseñas ingresadas no coinciden')
    
    # Busca el rol con el nombre ingresado
    stmt = db.select(Role).where(Role.id == role_id)
    query_role = db.session.execute(stmt).first()
    if not query_role:
        raise InvalidRoleError('El rol ingresado no existe')

    # Crea el usuario en la base de datos
    new_user = User(username, names, surnames, hash_password(password), query_role[0])
    db.session.add(new_user)

    # Registra el evento en la base de datos
    events.add_register(new_user.username)

def hash_password(password: str):
    '''Crea un hash de la contraseña ingresada.'''
    return bcrypt.hashpw(str.encode(password), bcrypt.gensalt())

# ========== Inicio de sesión ==========
def log_user(username: str, password: str) -> Tuple[int, str]:
    '''Inicia la sesión de un usuario retorna su id.

    Lanza una excepción AuthenticationError si hubo algún error.

    Retorna una tupla con el id del usuario y el nombre de su rol
    '''
    if not username or not password:
        raise MissingFieldError('Todos los campos son obligatorios')

    stmt = db.select(User).where(User.username == username)
    query_user = db.session.execute(stmt).first()

    if not query_user:
        raise UserNotFoundError('El usuario ingresado no existe')
    elif not check_password(password, query_user[0].password):
        raise IncorrectPasswordError('Las credenciales ingresadas son incorrectas')

    return (query_user[0].id, query_user[0].role.name)

def check_password(password, hash) -> bool:
    '''Comprueba si la contraseña coincide con el hash de la base de datos'''
    return bcrypt.checkpw(str.encode(password), hash)

# ========== Obtención de datos ==========
def get_current_user(user_id: int) -> User:
    '''Retorna el usuario con el id ingresado.'''
    stmt = db.select(User).where(User.id == user_id)
    return db.session.execute(stmt).first()[0]

# ========== Edición de datos ==========
def edit_user( user_id: int, username: str, names: str, surnames: str, role_id: str):
    '''Edita los datos de un usuario en la base de datos.

    Lanza una excepción AuthenticationError si hubo algún error.
    '''
    if not all([user_id, username, names, surnames, role_id]):
        raise MissingFieldError('Todos los campos son obligatorios')

    # Busca el usuario en la base de datos
    stmt = db.select(User).where(User.id == user_id)
    result = db.session.execute(stmt).fetchone()
    if not result:
        raise UserNotFoundError('El usuario indicado no existe')
    edited_user, = result

    # Busca el rol en la base de datos
    stmt = db.select(Role).where(Role.id == role_id)
    result = db.session.execute(stmt).fetchone()
    if not result:
        # Si no existe, se permanece en la página
        raise InvalidRoleError('El rol indicado no existe')
    new_role, = result

    # Verifica si ya existe un usuario distinto con el mismo nombre de usuario
    stmt = db.select(User).where(User.username == username).where(User.id != user_id)
    result = db.session.execute(stmt).first()
    if result:
        raise AlreadyExistingUserError('El nombre de usuario ya existe')

    # Chequea si los campos ingresados son válidos
    validate_username(username)
    validate_names(names)
    validate_names(surnames)

    if new_role.name == 'Administrador':
        # No se puede editar el rol de un usuario a administrador
        if edited_user.role.name != 'Administrador':
            raise InvalidRoleError('No se puede editar el rol de un usuario a administrador')
    else:
        # No se puede editar el rol de un administrador
        if edited_user.role.name == 'Administrador':
            raise InvalidRoleError('No se puede editar el rol de un administrador')

    # Edita el usuario en la base de datos
    edited_user.username = username
    edited_user.names = names
    edited_user.surnames = surnames
    edited_user.role = new_role

    db.session.commit()

    # Añade el evento de edición
    events.add_edit_user(username)
    
# ========== Eliminación de usuarios ==========
def delete_user(user_id: int):
    '''Elimina un usuario de la base de datos.

    Lanza una excepción AuthenticationError si hubo algún error.
    '''
    if not user_id:
        raise MissingFieldError('Todos los campos son obligatorios')

    # Busca el usuario en la base de datos
    stmt = db.select(User).where(User.id == user_id)
    result = db.session.execute(stmt).fetchone()
    if not result:
        raise UserNotFoundError('El usuario indicado no existe')
    deleted_user, = result

    # No se puede eliminar un administrador
    if deleted_user.role.name == 'Administrador':
        raise InvalidRoleError('No se puede eliminar un administrador')

    # Elimina el usuario de la base de datos
    db.session.delete(deleted_user)

    db.session.commit()

    # Añade el evento de eliminación
    events.add_delete_user(deleted_user.username)
