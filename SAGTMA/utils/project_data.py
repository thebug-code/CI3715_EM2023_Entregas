from SAGTMA.models import Project, Project_Detail, db
from SAGTMA.utils import events


class ProjectDetailError(ValueError):
    pass


# ========== Validaciones ==========
def validate_amount(amount: str) -> int:
    """
    Lanza una excepción si el monto no es válida.

    Un monto es válida si:
      -Es un número entero positivo
    """
    if not amount.isdigit():
        raise ProjectDetailError("El monto debe ser un número entero positivo")
    amount = int(amount)

    if amount < 0:
        raise ProjectDetailError("El monto debe ser un número entero positivo")

    return amount


def validate_input_text(input_text: str, flag: bool):
    """
    Lanza una excepción si el texto no es válido.

    Un texto es válido si:
        -Tiene al menos 5 caracteres y a lo sumo 100 caracteres
        -No tiene caracteres especiales distintos de '-_.,;:¡! '
    """
    if len(input_text) < 5 or len(input_text) > 100:
        if flag:
            raise ProjectDetailError("La solucion debe tener entre 5 y 100 caracteres")
        else:
            raise ProjectDetailError("Las observaciones deben tener entre 5 y 100 caracteres")

    regex = r"^[\w\s\-a-zA-Z0-9_.¡!,;:]*$"
    if not re.match(regex, observations):
        if flag:
            raise ProjectDetailError("La solucion solo puede contener caracteres alfanuméricos, guiones y espacios")
        else:
            raise ProjectDetailError("Las observaciones solo pueden contener caracteres alfanuméricos, guiones y espacios")


# ========== Funciones ==========
def register_project_detail(
    project_id: int,
    vehicle: str,
    department: str,
    manager: str,
    solution: str,
    amount: str,
    observations: str
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
    if not all([vehicle, department, manager, solution, amount, observations]):
        raise ProjectDetailError("Todos los campos son obligatorios")

    # Verifica que el proyecto exista
    smt = db.select(Project).where(Project.id == project_id)
    project_query = db.session.execute(smt).first()
    if not project_query:
        raise ProjectDetailError("El proyecto no existe")
    project = project_query[0]


    # Verifica que el id del vehículo es un número entero positivo
    if not vehicle.isdigit():
        raise ProjectDetailError("El id del vehículo debe ser un número entero positivo")
    vehicle_id = int(vehicle)

    # Verifica que el vehículo exista
    smt = db.select(Vehicle).where(Vehicle.id == vehicle_id)
    if not db.session.execute(smt).first():
        raise ProjectDetailError("El vehículo no existe")

    # Verifica que el id del departamento es un número entero positivo
    if not department.isdigit():
        raise ProjectDetailError("El id del departamento debe ser un número entero positivo")
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
    smt = db.select(Manager).where(Manager.id == manager)
    if not db.session.execute(smt).first():
        raise ProjectDetailError("El gerente no existe")

    # Chequea si los campos de texto son válidos
    amount = validate_amount(amount)
    validate_input_text(solution, True)
    validate_input_text(observations, False)

    # Crea el nuevo detalle de proyecto
    project_detail = Project_Detail(
        project_id,
        vehicle_id,
        department_id,
        manager_id,
        solution,
        amount,
        observations,
    )

    # Registra el evento en la base de datos
    events.add_event(
            "Datos del proyecto", f"Agregar dato de proyecto para el proyecto {project.description}"
    )
