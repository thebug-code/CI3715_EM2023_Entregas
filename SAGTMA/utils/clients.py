from datetime import date

from SAGTMA.models import Client, db
from SAGTMA.utils import events
from datetime import date


# ========== Excepciones ==========
class ClientError(ValueError):
    pass


class AlreadyExistingClientError(ClientError):
    pass


class MissingFieldError(ClientError):
    pass


class ClientNotFoundError(ClientError):
    pass


# ========== Validaciones ==========

# ========== Registro ==========
def register_client(
    id_number: str, 
    names: str, 
    surnames: str, 
    birthdate: str,
    phone_number: str, 
    email: str, 
    address: str
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

    if not all(
        [id_number, names, surnames, birthdate, phone_number, email, address]
    ):
        raise MissingFieldError("Todos los campos son obligatorios")

    # ---------------------------------
    # FALTA VERIFICAR TODOS LOS PARAMETROS
    # ---------------------------------

    # Verifica si ya existe un cliente con el mismo id_number
    stmt = db.select(Client).where(Client.id_number == id_number)
    if db.session.execute(stmt).first():
        raise AlreadyExistingClientError("El cliente ya existe")

    # Convert birthdate a tipo Date usando la libreria datetime
    y, m, d = birthdate.split("-")
    birthdate_t = date(int(y), int(m), int(d))

    # Crea el cliente en la base de datos
    new_client = Client(
                    id_number, names, surnames, birthdate_t, phone_number, email, address
                )

    db.session.add(new_client)

    # Registra el evento en la base de datos
    events.add_client(new_client.id_number)


# ========== Edicion de datos ==========
def modify_client(
    client_id: int,
    id_number: str, 
    names: str, 
    surnames: str, 
    birthdate: str,
    phone_number: str, 
    email: str, 
    address: str
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
    if not all(
        [id_number, names, surnames, birthdate, phone_number, email, address]
    ):
        raise MissingFieldError("Todos los campos son obligatorios")

    # ---------------------------------
    # FALTA VERIFICAR TODOS LOS PARAMETROS
    # ---------------------------------

    # Verifica si ya existe un cliente con el mismo id_number
    stmt = (
        db.select(Client)
        .where(Client.id_number == id_number)
        .where(Client.id != client_id)
    )
    if db.session.execute(stmt).first():
        raise AlreadyExistingClientError("El cliente ya existe")

    # Busca el cliente con el id indicado y verifica si existe
    stmt = db.select(Client).where(Client.id == client_id)
    client_query = db.session.execute(stmt).first()
    if not client_query:
        raise ClientNotFoundError("El cliente indicado no existe")

    # Convert birthdate a tipo Date usando la libreria datetime
    y, m, d = birthdate.split("-")
    birthdate_t = date(int(y), int(m), int(d))

    # Actualiza los datos del cliente
    client_query[0].id_number = id_number
    client_query[0].names = names.strip()
    client_query[0].surnames = surnames.strip()
    client_query[0].birthdate = birthdate_t
    client_query[0].phone_number = phone_number
    client_query[0].email = email.strip()
    client_query[0].address = address.strip()

    # Registra el evento en la base de datos
    events.add_modify_client(id_number)


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
        raise ClientNotFoundError("El cliente indicado no existe")

    # Elimina el cliente de la base de datos
    db.session.delete(result[0])

    # Registra el evento en la base de datos
    events.add_delete_client(result[0].id_number)
