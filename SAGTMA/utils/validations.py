import re
from typing import Type


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
