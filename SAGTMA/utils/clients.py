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

# ========== Anadidura ==========
def modify_client(
    client_id: int,
    id_number: int, 
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
    # events.add_modify_client(id_number)

    db.session.commit()
