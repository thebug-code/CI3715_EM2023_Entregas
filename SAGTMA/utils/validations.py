import re
from typing import Type
from datetime import date


def validate_id(id_number: str, exception_type: Type[BaseException]) -> str:
    """
    Lanza la excepción provista si una cédula no es válida.

    El formato del una cédula válida es:
     - Comienza con V, E, J, G, C, mayúscula o minúscula.
     - Seguido de un guión y 8 dígitos.
     - Puede contener espacios o puntos como separadores.

    Retorna la cédula transformada a un formato estándar:
     - Comienza con mayúscula.
    -  Seguido de un guión y 7 u 8 dígitos.
    """
    # Remueve espacios y puntos del número
    table = str.maketrans("", "", ". ")
    id_number = id_number.translate(table)

    # Transforma a mayúsculas
    id_number = id_number.upper()

    # Expresión regular para validar cédulas de identidad
    regex = r"[V|E|J|G|C]-\d{7,8}"
    if not re.fullmatch(regex, id_number):
        raise exception_type(
            "La cédula ingresada es inválida, debe tener el formato V-12345678"
        )

    return id_number


def validate_name(name: str, exception_type: Type[BaseException]):
    """
    Lanza una excepción si el nombre no es válido.

    Un nombre es válido si:
      -Tiene al menos 2 caracteres y a lo sumo 50 caracteres
      -No tiene caracteres especiales distintos de ' ' (espacio)
    """
    if len(name) < 2 or len(name) > 50:
        raise exception_type("El nombre debe tener entre 2 y 50 caracteres.")

    for char in name:
        if not char.isalnum() and char != " ":
            raise exception_type("El nombre no puede contener caracteres especiales.")


def validate_date(
    start_date: date, deadline: date, exception_type: Type[BaseException]
) -> str:
    """
    Lanza una excepción si la fecha de inicio de un proyecto es despues que su fecha de cierre
    """

    if start_date > deadline:
        raise exception_type(
            "La fecha de inicio no puede ser mayor que la fecha de cierre."
        )


def validate_input_text(
    input_text: str, campo: str, exception_type: Type[BaseException]
):
    """
    Lanza una excepción si el texto no es válido.

    Un texto es válido si:
        -Tiene al menos 3 caracteres y a lo sumo 100 caracteres
        -No tiene caracteres especiales distintos de '-_.,;:¡!/ '
    """
    if len(input_text) < 3 or len(input_text) > 100:
        raise exception_type(f"El campo {campo} debe tener entre 3 y 100 caracteres")

    regex = r"^[\w\s\-a-zA-Z0-9_.¡!,/;:]*$"
    if not re.match(regex, input_text):
        if flag:
            raise exception_type(
                f"El campo {campo} solo puede contener caracteres alfanuméricos, guiones y espacios"
            )
