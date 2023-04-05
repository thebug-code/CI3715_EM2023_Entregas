import re

from SAGTMA.models import Project, ProjectDetail, Vehicle, Department, User, db
from SAGTMA.utils import events


class ProjectDetailError(ValueError):
    pass


# ========== Validaciones ==========
def validate_cost(cost: str) -> float:
    """
    Lanza una excepción si el monto no es válido.

    Un monto es válida si:
      -Es un número entero positivo
    """
    try:
        cost = float(cost)
    except ValueError:
        raise ProjectDetailError("El monto debe ser un número")

    if cost < 0:
        raise ProjectDetailError("El monto debe ser un número positivo")

    return cost


def validate_input_text(input_text: str, flag: bool):
    """
    Lanza una excepción si el texto no es válido.

    Un texto es válido si:
        -Tiene al menos 3 caracteres y a lo sumo 100 caracteres
        -No tiene caracteres especiales distintos de '-_.,;:¡!/ '
    """
    if len(input_text) < 3 or len(input_text) > 100:
        if flag:
            raise ProjectDetailError("La solucion debe tener entre 3 y 100 caracteres")
        else:
            raise ProjectDetailError(
                "Las observaciones deben tener entre 3 y 100 caracteres"
            )

    regex = r"^[\w\s\-a-zA-Z0-9_.¡!,/;:]*$"
    if not re.match(regex, input_text):
        if flag:
            raise ProjectDetailError(
                "La solucion solo puede contener caracteres alfanuméricos, guiones y espacios"
            )
        else:
            raise ProjectDetailError(
                "Las observaciones solo pueden contener caracteres alfanuméricos, guiones y espacios"
            )


# ========== Registro de detalle de proyecto ==========
def register_project_detail(
    project_id: int,
    vehicle: str,
    department: str,
    manager: str,
    solution: str,
    cost: str,
    observations: str,
):
    """
    Registra un nuevo detalle de proyecto en la base de datos.

    Lanza una excepción si:
        -El proyecto no existe
        -El monto no es válido
        -La solución no es válida
        -Las observaciones no son válidas
        -El vehículo no existe
        -El departamento no existe
        -El gerente no existe
    """
    # Elimina espacios al comienzo y final del input del form
    vehicle = vehicle.strip()
    department = department.strip()
    manager = manager.strip()
    solution = solution.strip()
    observations = observations.strip()

    # Verifica que todos los campos estén completos
    if not all([vehicle, department, manager, solution, cost, observations]):
        raise ProjectDetailError("Todos los campos son obligatorios")

    # Verifica que el proyecto exista
    smt = db.select(Project).where(Project.id == project_id)
    project_query = db.session.execute(smt).first()
    if not project_query:
        raise ProjectDetailError("El proyecto no existe")
    project = project_query[0]

    # Verifica que el id del vehículo es un número entero positivo
    if not vehicle.isdigit():
        raise ProjectDetailError(
            "El id del vehículo debe ser un número entero positivo"
        )
    vehicle_id = int(vehicle)

    # Verifica que el vehículo exista
    smt = db.select(Vehicle).where(Vehicle.id == vehicle_id)
    if not db.session.execute(smt).first():
        raise ProjectDetailError("El vehículo no existe")

    # Verifica que el id del departamento es un número entero positivo
    if not department.isdigit():
        raise ProjectDetailError(
            "El id del departamento debe ser un número entero positivo"
        )
    department_id = int(department)

    # Verifica que el departamento exista
    smt = db.select(Department).where(Department.id == department_id)
    if not db.session.execute(smt).first():
        raise ProjectDetailError("El departamento no existe")

    # Verifica que el id del gerente es un número entero positivo
    if not manager.isdigit():
        raise ProjectDetailError("El id del gerente debe ser un número entero positivo")
    manager_id = int(manager)

    # Verifica que el gerente exista
    smt = db.select(User).where(User.id == manager_id)
    if not db.session.execute(smt).first():
        raise ProjectDetailError("El gerente no existe")

    # Chequea si los campos de texto son válidos
    cost = validate_cost(cost)
    validate_input_text(solution, True)
    validate_input_text(observations, False)

    # Crea el nuevo detalle de proyecto
    detail = ProjectDetail(
        project_id,
        vehicle_id,
        department_id,
        manager_id,
        solution,
        cost,
        observations,
    )
    
    # Agrega el detalle de proyecto a la base de datos
    db.session.add(detail)

    # Registra el evento en la base de datos
    events.add_event(
        "Datos de proyectos",
        f"Agregar detalle al proyecto '{project.description}'"
    )


# ========== Edición de detalle de proyecto ==========
def edit_project_detail(
    detail_id: int,
    vehicle: str,
    department: str,
    manager: str,
    solution: str,
    cost: str,
    observations: str,
):
    """
    Edita un detalle de proyecto en la base de datos.

    Lanza una excepción si:
        -El detalle de proyecto no existe
        -El monto no es válido
        -La solución no es válida
        -Las observaciones no son válidas
        -El vehículo no existe
        -El departamento no existe
        -El gerente no existe
    """
    # Elimina espacios al comienzo y final del input del form
    vehicle = vehicle.strip()
    department = department.strip()
    manager = manager.strip()
    solution = solution.strip()
    observations = observations.strip()

    # Verifica que todos los campos estén completos
    if not all([vehicle, department, manager, solution, cost, observations]):
        raise ProjectDetailError("Todos los campos son obligatorios")

    # Verifica que el detalle de proyecto exista
    smt = db.select(ProjectDetail).where(ProjectDetail.id == detail_id)
    detail_query = db.session.execute(smt).first()
    if not detail_query:
        raise ProjectDetailError("El detalle de proyecto no existe")
    edited_detail = detail_query[0]

    # Verifica que el id del vehículo es un número entero positivo
    if not vehicle.isdigit():
        raise ProjectDetailError(
            "El id del vehículo debe ser un número entero positivo"
        )
    vehicle_id = int(vehicle)

    # Verifica que el vehículo exista
    smt = db.select(Vehicle).where(Vehicle.id == vehicle_id)
    if not db.session.execute(smt).first():
        raise ProjectDetailError("El vehículo no existe")

    # Verifica que el id del departamento es un número entero positivo
    if not department.isdigit():
        raise ProjectDetailError(
            "El id del departamento debe ser un número entero positivo"
        )
    department_id = int(department)

    # Verifica que el departamento exista
    smt = db.select(Department).where(Department.id == department_id)
    if not db.session.execute(smt).first():
        raise ProjectDetailError("El departamento no existe")

    # Verifica que el id del gerente es un número entero positivo
    if not manager.isdigit():
        raise ProjectDetailError("El id del gerente debe ser un número entero positivo")
    manager_id = int(manager)

    # Verifica que el gerente exista
    smt = db.select(User).where(User.id == manager_id)
    if not db.session.execute(smt).first():
        raise ProjectDetailError("El gerente no existe")

    # Chequea si los campos de texto son válidos
    cost = validate_cost(cost)
    validate_input_text(solution, True)
    validate_input_text(observations, False)

    # Edita el detalle de proyecto
    edited_detail.vehicle_id = vehicle_id
    edited_detail.department_id = department_id
    edited_detail.manager_id = manager_id
    edited_detail.solution = solution
    edited_detail.cost = cost
    edited_detail.observations = observations

    # Registra el evento en la base de datos
    events.add_event(
        "Datos de proyectos",
        f"Editar detalle {edited_detail.id} del proyecto {edited_detail.project.description}"
    )


# ========== Eliminación de detalle de proyecto ==========
def delete_project_detail(detail_id: int):
    """
    Elimina un detalle de proyecto de la base de datos.

    Lanza una excepción si:
        -El detalle de proyecto no existe
    """
    # Selecciona el detalle de proyecto con el id indicado y virifica que exista
    smt = db.select(ProjectDetail).where(ProjectDetail.id == detail_id)
    detail_query = db.session.execute(smt).first()
    if not detail_query:
        raise ProjectDetailError("El detalle de proyecto no existe")
    detail = detail_query[0]

    # Elimina el detalle de proyecto de la base de datos
    db.session.delete(detail)

    # Registra el evento en la base de datos
    events.add_event(
        "Datos de proyectos",
        f"Eliminar detalle {detail.id} del proyecto {detail.project.description}"
    )
