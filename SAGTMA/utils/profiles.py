from typing import Tuple

import bcrypt

from SAGTMA.models import Role, User, db
from SAGTMA.utils import events


class AuthenticationError(ValueError):
    pass


# ========== Validaciones ==========
def validate_username(username: str) -> bool:
    """
    Lanza una excepción si el nombre de usuario no es válido.

    Un nombre de usuario es válido si:
      -Tiene al menos 3 caracteres y a lo sumo 20 caracteres
      -No tiene caracteres especiales distintos de '_' (guión bajo)
      -No comienza con un caracter numérico
    """
    if len(username) < 3 or len(username) > 20:
        raise AuthenticationError(
            "El nombre de usuario debe tener entre 3 y 20 caracteres."
        )

    if username[0].isdigit():
        raise AuthenticationError(
            "El nombre de usuario no puede comenzar con un número."
        )

    for char in username:
        if not char.isalnum() and char != "_":
            raise AuthenticationError(
                "El nombre de usuario no puede contener caracteres especiales."
            )


def validate_names(names: str) -> bool:
    """
    Lanza una excepción si el nombre no es válido.

    Un nombre es válido si:
      -Tiene al menos 2 caracteres y a lo sumo 50 caracteres
      -No tiene caracteres especiales distintos de ' ' (espacio)
    """
    if len(names) < 2 or len(names) > 50:
        raise AuthenticationError("El nombre debe tener entre 2 y 50 caracteres.")

    for char in names:
        if not char.isalnum() and char != " ":
            raise AuthenticationError(
                "El nombre no puede contener caracteres especiales."
            )


def validate_password(password: str) -> bool:
    """
    Lanza una excepción si la contraseña no es válida.

    La contraseña es válida si:
      -Tiene al menos 6 caracteres y a lo sumo 20 caracteres
      -Tiene al menos un número
      -Tiene al menos una mayúscula y una minúscula
      -Tiene al menos un caracter especial
    """
    if len(password) < 6 or len(password) > 20:
        raise AuthenticationError("La contraseña debe tener entre 6 y 20 caracteres.")

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
        raise AuthenticationError("La contraseña debe contener al menos un número.")
    elif no_upper or no_lower:
        raise AuthenticationError(
            "La contraseña debe contener al menos una mayúscula y una minúscula"
        )
    elif no_special:
        raise AuthenticationError(
            "La contraseña debe contener al menos un caracter especial."
        )


# ========== Registro ==========
def register_user(
    id_number: str,
    username: str,
    names: str,
    surnames: str,
    password: str,
    confirm_password: str,
    role_id: str,
):
    """
    Registra un usuario en la base de datos.

    Lanza una excepción AuthenticationError si hubo algún error.
    """
    # Elimina los espacios en blanco al inicio y al final de los campos
    id_number = id_number.strip()
    username = username.strip()
    names = names.strip()
    surnames = surnames.strip()

    # Verifica que no haya campos vacíos
    if not all(
        [id_number, username, names, surnames, password, confirm_password, role_id]
    ):
        raise AuthenticationError("Todos los campos son obligatorios")

    # Verifica si ya existe un usuario con el mismo nombre de usuario
    stmt = db.select(User).where(User.username == username)
    if db.session.execute(stmt).first():
        raise AuthenticationError("El nombre de usuario ya existe")

    # Chequea si los campos ingresados son válidos
    # validate_id(id_number)
    validate_username(username)
    validate_names(names)
    validate_names(surnames)
    validate_password(password)

    if password != confirm_password:
        raise AuthenticationError("Las contraseñas ingresadas no coinciden")

    # Busca el rol con el nombre ingresado
    stmt = db.select(Role).where(Role.id == role_id)
    query_role = db.session.execute(stmt).first()
    if not query_role:
        raise AuthenticationError("El rol ingresado no existe")

    # Crea el usuario en la base de datos
    new_user = User(
        id_number, username, names, surnames, hash_password(password), query_role[0]
    )
    db.session.add(new_user)

    # Registra el evento en la base de datos
    events.add_event("Perfiles de Usuarios", f"Agregar usuario '{new_user.username}'")


def hash_password(password: str):
    """Crea un hash de la contraseña ingresada."""
    return bcrypt.hashpw(str.encode(password), bcrypt.gensalt())


# ========== Inicio de sesión ==========
def log_user(username: str, password: str) -> Tuple[int, str]:
    """
    Inicia la sesión de un usuario retorna su id.

    Lanza una excepción AuthenticationError si hubo algún error.

    Retorna una tupla con el id del usuario y el nombre de su rol
    """
    if not username or not password:
        raise AuthenticationError("Todos los campos son obligatorios")

    stmt = db.select(User).where(User.username == username)
    query_user = db.session.execute(stmt).first()

    if not query_user:
        raise AuthenticationError("El usuario ingresado no existe")
    elif not check_password(password, query_user[0].password):
        raise AuthenticationError("Las credenciales ingresadas son incorrectas")

    return (query_user[0].id, query_user[0].role.name)


def check_password(password, hash) -> bool:
    """Comprueba si la contraseña coincide con el hash de la base de datos"""
    return bcrypt.checkpw(str.encode(password), hash)


# ========== Obtención de datos ==========
def get_current_user(user_id: int) -> User:
    """Retorna el usuario con el id ingresado."""
    stmt = db.select(User).where(User.id == user_id)
    return db.session.execute(stmt).first()[0]


# ========== Edición de datos ==========
def edit_user(
    user_id: int, 
    id_number: str,
    username: str,
    names: str, 
    surnames: str,
    role_id: str
):
    """
    Edita los datos de un usuario en la base de datos.

    Lanza una excepción AuthenticationError si hubo algún error.
    """
    # Elimina los espacios en blanco al principio y al final
    id_number = id_number.strip()
    username = username.strip()
    names = names.strip()
    surnames = surnames.strip()
    
    # Verifica que no haya campos vacíos
    if not all(
        [user_id, id_number, username, names, surnames, role_id]
    ):
        raise AuthenticationError("Todos los campos son obligatorios")

    # Busca el usuario en la base de datos
    stmt = db.select(User).where(User.id == user_id)
    result = db.session.execute(stmt).fetchone()
    if not result:
        raise AuthenticationError("El usuario indicado no existe")
    (edited_user,) = result

    # Busca el rol en la base de datos
    stmt = db.select(Role).where(Role.id == role_id)
    result = db.session.execute(stmt).fetchone()
    if not result:
        # Si no existe, se permanece en la página
        raise AuthenticationError("El rol indicado no existe")
    (new_role,) = result

    # Verifica si ya existe un usuario distinto con el mismo nombre de usuario
    stmt = (
        db.select(User)
        .where(User.username == username)
        .where(User.id != user_id)
    )
    result = db.session.execute(stmt).first()
    if result:
        raise AuthenticationError("El nombre de usuario ya existe")

    # Chequea si los campos ingresados son válidos
    validate_username(username)
    validate_names(names)
    validate_names(surnames)

    if new_role.name == "Administrador":
        # No se puede editar el rol de un usuario a administrador
        if edited_user.role.name != "Administrador":
            raise AuthenticationError(
                "No se puede editar el rol de un usuario a administrador"
            )
    else:
        # No se puede editar el rol de un administrador
        if edited_user.role.name == "Administrador":
            raise AuthenticationError("No se puede editar el rol de un administrador")

    # Edita el usuario en la base de datos
    edited_user.id_number = id_number
    edited_user.username = username
    edited_user.names = names
    edited_user.surnames = surnames
    edited_user.role = new_role

    db.session.commit()

    # Añade el evento de edición
    events.add_event("Perfiles de Usuarios", f"Editar usuario '{username}'")


# ========== Eliminación de usuarios ==========
def delete_user(user_id: int):
    """
    Elimina un usuario de la base de datos.

    Lanza una excepción AuthenticationError si hubo algún error.
    """
    if not user_id:
        raise AuthenticationError("Todos los campos son obligatorios")

    # Busca el usuario en la base de datos
    stmt = db.select(User).where(User.id == user_id)
    result = db.session.execute(stmt).fetchone()
    if not result:
        raise AuthenticationError("El usuario indicado no existe")
    (deleted_user,) = result

    # No se puede eliminar un administrador
    if deleted_user.role.name == "Administrador":
        raise AuthenticationError("No se puede eliminar un administrador")

    # Elimina el usuario de la base de datos
    db.session.delete(deleted_user)

    db.session.commit()

    # Añade el evento de eliminación
    events.add_event(
        "Perfiles de Usuarios", f"Eliminar usuario '{deleted_user.username}'"
    )
