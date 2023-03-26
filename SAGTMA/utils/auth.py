from typing import Tuple

import bcrypt

from SAGTMA.models import User, db


class AuthenticationError(ValueError):
    pass


# ========== Validaciones ==========
def hash_password(password: str):
    """Crea un hash de la contraseña ingresada."""
    return bcrypt.hashpw(str.encode(password), bcrypt.gensalt())


def check_password(password, hash) -> bool:
    """Comprueba si la contraseña coincide con el hash de la base de datos"""
    return bcrypt.checkpw(str.encode(password), hash)


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
