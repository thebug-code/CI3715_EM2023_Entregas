import re
from datetime import date

from SAGTMA.models import ActionPlan, Activity, ProjectDetail, User, db
from SAGTMA.utils import events
from SAGTMA.utils.validations import validate_date, validate_input_text


class ActionPlanError(ValueError):
    pass


# ========= Validaciones =========
def validate_works_hours(work_hours: str) -> int:
    """
    Lanza una excepción si la cantidad de horas de trabajo no es valida.

    Una cantidad de horas de trabajo es válida si:
        - Es un número entero positivo
    """
    if not work_hours.isdigit():
        raise ActionPlanError("La cantidad de horas de trabajo debe ser un número entero positivo.")
    return int(work_hours)


# ========= Registro de planes de acción =========
def register_action_plan(
    project_detail_id: int,
    action: str,
    activity: str,
    start_date: str,
    deadline: str,
    work_hours: str,
    charge_person_id: int,
    cost: str
):
    """
    Registra un plan de acción en la base de datos.

    Lanza una excepción si:
        - El proyecto no existe
        - La actividad no es valida
        - La fecha de inicio no es valida
        - La fecha de finalización no es valida
        - La cantidad de horas de trabajo no es valida
        - La persona encargada no existe
        - El costo no es valido
        - El tipo de acción no es valido
    """
    # Elimina espacios al comienzo y final del input del form
    action = action.strip()
    activity = activity.strip()
    start_date = start_date.strip()
    deadline = deadline.strip()
    work_hours = work_hours.strip()
    cost = cost.strip()

    # Verifica que todos los campos estén completos
    if not all(
        [action, activity, start_date, deadline, work_hours, charge_person_id, cost]
    ):
        raise ActionPlanError("Todos los campos son obligatorios.")
    
    # Selecciona el detalle de proyecto y verifica que exista
    smt = db.select(ProjectDetail).where(ProjectDetail.id == project_detail_id)
    project_detail_query = db.session.execute(smt).first()
    if not project_detail_query:
        raise ActionPlanError("El detalle de proyecto no existe.")
    project_detail = project_detail_query[0]

    # Verifica que la persona encargada exista
    smt = db.select(User).where(User.id == charge_person_id)
    if not db.session.execute(smt).first():
        raise ActionPlanError("La persona encargada no existe.")

    # Verifica que la actividad sea válida
    validate_input_text(activity, "Actividad", ActionPlanError)

    # Convert start_date a tipo Date usando la libreria datetime
    y, m, d = start_date.split("-")
    y, m, d = int(y), int(m), int(d)
    start_date_t = date(y, m, d)

    # Convert deadline a tipo Date usando la libreria datetime
    y, m, d = deadline.split("-")
    y, m, d = int(y), int(m), int(d)
    deadline_t = date(y, m, d)

    # Verifica que las fechas sean válidas
    validate_date(start_date_t, deadline_t, ActionPlanError)

    # Verifica que la cantidad de horas de trabajo sea válida
    work_hours = validate_works_hours(work_hours)

    # Calcula el costo total (falta)
    
    # Verifica el tipo de acción
    action_id = int(action) if action.isdigit() else None

    # Crea o selecciona un plan de acción de acuerdo al tipo de acción
    if action_id:
        # Seleciona el plan de acción con el id indicado y verifica que exista
        smt = db.select(ActionPlan).where(ActionPlan.id == action_id)
        action_plan_query = db.session.execute(smt).first()
        if not action_plan_query:
            raise ActionPlanError("El plan de acción no existe.")
        action_plan = action_plan_query[0]

        # Crea una actividad
        activity = Activity(
            action_id,
            charge_person_id,
            activity,
            start_date_t,
            deadline_t,
            work_hours,
            float(cost) # Después se calcula el costo total
        )
        db.session.add(activity)

        # Registra el evento en la base de datos
        events.add_event(
            "Planes de acción",
            f"Agregar actividad '{activity.description}' al plan de acción '{action_plan.action}'"
        )
        
    else:

        # Crea un plan de acción
        action_plan = ActionPlan(action, project_detail_id)

        db.session.add(action_plan)
        db.session.commit()

        # Crea una actividad
        activity = Activity(
            action_plan.id,
            charge_person_id,
            activity,
            start_date_t,
            deadline_t,
            work_hours,
            float(cost) # Después se calcula el costo total
        )

        db.session.add(activity)

        # Registra el evento en la base de datos
        events.add_event(
            "Planes de acción", f"Agregar plan de acción '{action}'"
        )
    





