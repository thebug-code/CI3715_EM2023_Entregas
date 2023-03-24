import re
import datetime

from SAGTMA.models import Client, db
from SAGTMA.utils import events
from SAGTMA.utils.profiles import validate_names


class ClientError(ValueError):
    pass


# ========== Validaciones ==========
def validate_id(id_number: str) -> str:
    """
    Lanza una excepción si una cédula no es válida.

    El formato del una cédula válida es:
     - Comienza con V, E, J, G, C, mayúscula o minúscula.
     - Seguido de un guión y 8 dígitos.
     - Puede contener espacios o puntos como separadores.

    Retorna la cédula transformada a un formato estándar:
     - Comienza con V.
    -  Seguido de un guión y 8 dígitos.
    """
    # Remueve espacios y puntos del número
    table = str.maketrans("", "", ". ")
    id_number = id_number.translate(table)

    # Transforma a mayúsculas
    id_number = id_number.upper()

    # Expresión regular para validar cédulas de identidad
    regex = r"[V|E|J|G|C]-\d{7,8}"
    if not re.fullmatch(regex, id_number):
        raise ClientError(
            "La cédula ingresada es inválida, debe tener el formato V-12345678"
        )

    return id_number


def validate_phone_number(phone_number: str) -> str:
    """
    Lanza una excepción si el número telefónico no es válido.

    El formato del un número de teléfono válido es cualquiera de los siguientes:
     - Comienza con 58, +58, 0058, 0 no tener comienzo.
     - Seguido de 10 dígitos.
     - Puede contener paréntesis, espacios, puntos o guiones como separadores.

    Retorna el número de teléfono transformado a un formato estándar:
     - Comienza con +58.
     - Seguido de 10 dígitos.
     - No contiene separadores.
    """
    # Remueve espacios, guiones, paréntesis y puntos del número
    table = str.maketrans("", "", ".- ()[]")
    phone_number = phone_number.translate(table)

    # Expresión regular para validar número telefónicos
    regex = r"((\+|00)?58|0)?\d{10}"
    if not re.fullmatch(regex, phone_number):
        raise ClientError("El número de teléfono ingresado no tiene un formato válido")

    # Regulariza el número para guardarlo en la base de datos
    if phone_number.startswith("00"):
        phone_number = phone_number.replace("00", "+")
    elif phone_number.startswith("0"):
        phone_number = phone_number.replace("0", "+58")
    elif not phone_number.startswith("+58"):
        phone_number = f"+58{phone_number}"

    return phone_number


def validate_email(email: str):
    """Lanza una excepción si el correo electrónico no es válido"""
    # Expresión regular para validar correos electrónicos
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    if not re.fullmatch(regex, email):
        raise ClientError("El correo electrónico ingresado es inválido")


def validate_birthdate(birthdate: datetime.date):
    """
    Lanza una excepción si la fecha de nacimiento no es válida

    La edad mínima es 18 años.
    La edad máxima es 100 años.
    """
    today = datetime.date.today()
    age = (
        today.year
        - birthdate.year
        - ((today.month, today.day) < (birthdate.month, birthdate.day))
    )

    if age < 18:
        raise ClientError("La edad mínima para registrarse es 18 años")
    elif age > 100:
        raise ClientError("La edad máxima para registrarse es 100 años")


# ========== Registro ==========
def register_client(
    id_number: str,
    names: str,
    surnames: str,
    birthdate: str,
    phone_number: str,
    email: str,
    address: str,
):
    """
    Crea y anade un cliente en la base de datos.

    Lanza una excepción ClientError si hubo algún error.
    """
    # Elimina espacios al comienzo y final del input del form
    names = names.strip()
    surnames = surnames.strip()
    phone_number = phone_number.strip()
    email = email.strip()
    address = address.strip()

    if not all([id_number, names, surnames, birthdate, phone_number, email, address]):
        raise ClientError("Todos los campos son obligatorios")

    # Chequea si los campos son válidos
    id_number = validate_id(id_number)
    validate_names(names)
    validate_names(surnames)
    phone_number = validate_phone_number(phone_number)
    validate_email(email)

    if len(address) > 120:
        raise ClientError(
            "La descripción del problema no puede tener más de 120 caracteres"
        )

    # Verifica si ya existe un cliente con el mismo id_number
    stmt = db.select(Client).where(Client.id_number == id_number)
    if db.session.execute(stmt).first():
        raise ClientError("Ya existe un cliente con la misma cédula")

    # Convert birthdate a tipo Date usando la libreria datetime
    y, m, d = birthdate.split("-")
    y, m, d = int(y), int(m), int(d)
    birthdate_t = datetime.date(y, m, d)

    # Chequea si la fecha de nacimiento es válida
    validate_birthdate(birthdate_t)

    # Crea el cliente en la base de datos
    new_client = Client(
        id_number, names, surnames, birthdate_t, phone_number, email, address
    )

    db.session.add(new_client)

    # Registra el evento en la base de datos
    events.add_event(
        "Detalles de los Clientes", f"Agregar cliente '{new_client.id_number}'"
    )


# ========== Edicion de datos ==========
def edit_client(
    client_id: int,
    id_number: str,
    names: str,
    surnames: str,
    birthdate: str,
    phone_number: str,
    email: str,
    address: str,
):
    """
    Modifica los datos de un cliente en la base de datos

    Lanza una excepción ClientError si hubo algún error.
    """
    # Elimina espacios al comienzo y final del input del form
    names = names.strip()
    surnames = surnames.strip()
    phone_number = phone_number.strip()
    email = email.strip()
    address = address.strip()

    # Verifica si todos los campos fueron ingresados
    if not all([id_number, names, surnames, birthdate, phone_number, email, address]):
        raise ClientError("Todos los campos son obligatorios")

    # Chequea si los campos son válidos
    id_number = validate_id(id_number)
    validate_names(names)
    validate_names(surnames)
    phone_number = validate_phone_number(phone_number)
    validate_email(email)

    if len(address) > 120:
        raise ClientError(
            "La descripción del problema no puede tener más de 120 caracteres"
        )

    # Verifica si ya existe un cliente con el mismo id_number
    stmt = (
        db.select(Client)
        .where(Client.id_number == id_number)
        .where(Client.id != client_id)
    )
    if db.session.execute(stmt).first():
        raise ClientError("Ya existe un cliente con la misma cédula")

    # Busca el cliente con el id indicado y verifica si existe
    stmt = db.select(Client).where(Client.id == client_id)
    client_query = db.session.execute(stmt).first()
    if not client_query:
        raise ClientError("El cliente indicado no existe")

    # Convert birthdate a tipo Date usando la libreria datetime
    y, m, d = birthdate.split("-")
    y, m, d = int(y), int(m), int(d)
    birthdate_t = datetime.date(y, m, d)

    validate_birthdate(birthdate_t)

    # Actualiza los datos del cliente
    client_query[0].id_number = id_number
    client_query[0].names = names.strip()
    client_query[0].surnames = surnames.strip()
    client_query[0].birthdate = birthdate_t
    client_query[0].phone_number = phone_number
    client_query[0].email = email.strip()
    client_query[0].address = address.strip()

    # Registra el evento en la base de datos
    events.add_event("Detalles de los Clientes", f"Modificar cliente '{id_number}'")


# ========== Eliminacion de clientes ==========
def delete_client(client_id: int):
    """
    Elimina un cliente de la base de datos

    Lanza una excepción ClientError si hubo algún error.
    """
    # Busca el cliente con el id indicado y verifica si existe
    stmt = db.select(Client).where(Client.id == client_id)
    result = db.session.execute(stmt).first()
    if not result:
        raise ClientError("El cliente indicado no existe")

    # Elimina el cliente de la base de datos
    db.session.delete(result[0])

    # Registra el evento en la base de datos
    events.add_event(
        "Detalles de los Clientes", f"Eliminar cliente '{result[0].id_number}'"
    )
