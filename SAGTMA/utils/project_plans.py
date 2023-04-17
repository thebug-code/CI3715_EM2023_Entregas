from datetime import date

from SAGTMA.models import (
    ActionPlan,
    Activity,
    ProjectDetail,
    User,
    MeasureUnit,
    MaterialSupply,
    HumanTalent,
    db,
)
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
        raise ActionPlanError(
            "La cantidad de horas de trabajo debe ser un número entero positivo."
        )

    work_hours = int(work_hours)
    if work_hours <= 0:
        raise ActionPlanError(
            "La cantidad de horas de trabajo debe ser un número entero positivo."
        )
    return work_hours


# ========= Registro de Actividades de Planes de Acción =========
def register_activity_action_plan(
    project_detail_id: int,
    action: str,
    activity: str,
    start_date: str,
    deadline: str,
    work_hours: str,
    charge_person_id: str,
    amount_person_hl: str,
    cost_hl: str,
    category_ms: str,
    description_ms: str,
    amount_ms: str,
    measure_unit_ms_id: int,
    cost_ms: str,
):
    """
    Registra una actividad y su plan de acción asociado.

    Lanza una excepción si:
        - El proyecto no existe
        - La actividad no es valida
        - La fecha de inicio no es valida
        - La fecha de finalización no es valida
        - La cantidad de horas de trabajo no es valida
        - La persona encargada no existe
        - El costo no es valido
        - El tipo de acción no es valido
        - La cantidad de personas en talento humano no es valida
        - El costo de talento humano no es valido
        - La categoría de materiales y suministros no es valida
        - La descripción de materiales y suministros no es valida
        - La cantidad de materiales y suministros no es valida
        - La unidad de medida de materiales y suministros no es valida
        - El costo de materiales y suministros no es valido
    """
    # Elimina espacios al comienzo y final del input del form
    action = action.strip()
    activity = activity.strip()
    start_date = start_date.strip()
    deadline = deadline.strip()
    work_hours = work_hours.strip()
    charge_person_id = charge_person_id.strip()
    amount_person_hl = amount_person_hl.strip()
    cost_hl = cost_hl.strip()
    category_ms = category_ms.strip()
    description_ms = description_ms.strip()
    amount_ms = amount_ms.strip()
    cost_ms = cost_ms.strip()

    # Verifica que todos los campos estén completos
    if not all(
        [
            action,
            activity,
            start_date,
            deadline,
            work_hours,
            charge_person_id,
            amount_person_hl,
            cost_hl,
            category_ms,
            description_ms,
            amount_ms,
            cost_ms,
        ]
    ):
        raise ActionPlanError("Todos los campos son obligatorios.")

    # Verificar que el detalle de proyecto exista
    smt = db.select(ProjectDetail).where(ProjectDetail.id == project_detail_id)
    if not db.session.execute(smt).first():
        raise ActionPlanError("El detalle de proyecto no existe.")

    # Verifica que la persona encargada exista
    smt = db.select(User).where(User.id == charge_person_id)
    if not db.session.execute(smt).first():
        raise ActionPlanError("La persona encargada no existe.")

    # Verifica que la actividad sea válida
    validate_input_text(activity, "Actividad", ActionPlanError)

    # Verifica que la cantidad de personas en talento humano sea válida
    if not amount_person_hl.isdigit():
        raise ActionPlanError(
            "La cantidad de personas en talento humano debe ser un número entero positivo."
        )
    if int(amount_person_hl) < 0:
        raise ActionPlanError(
            "La cantidad de personas en talento humano debe ser mayor o igual a 0."
        )
    amount_person_hl = int(amount_person_hl)

    # Verifica que el costo de talento humano sea válido
    try:
        cost_hl = float(cost_hl)
    except ValueError:
        raise ActionPlanError("El costo de talento humano debe ser mayor o igual a 0.")
    if cost_hl < 0:
        raise ActionPlanError("El costo de talento humano debe ser mayor o igual a 0.")

    # Verifica que la categoría de materiales y suministros sea válida
    validate_input_text(
        category_ms, "Categoría de Materiales y Suministros", ActionPlanError
    )

    # Verifica que la descripción de materiales y suministro
    validate_input_text(
        description_ms, "Descripción de Materiales y Suministros", ActionPlanError
    )

    # Verifica que la cantidad de materiales y suministros sea válida
    if not amount_ms.isdigit():
        raise ActionPlanError(
            "La cantidad de materiales y suministros debe ser un número entero positivo."
        )
    if int(amount_ms) < 0:
        raise ActionPlanError(
            "La cantidad de materiales y suministros debe ser mayor o igual a 0."
        )
    amount_ms = int(amount_ms)

    # Verifica que la unidad de medida de materiales y suministros sea válida
    if not measure_unit_ms_id.isdigit():
        raise ActionPlanError(
            "La unidad de medida de materiales y suministros no es válida."
        )
    measure_unit_ms_id = int(measure_unit_ms_id)

    # Verifica que la unidad de medida de materiales y suministros exista
    smt = db.select(MeasureUnit).where(MeasureUnit.id == measure_unit_ms_id)
    if not db.session.execute(smt).first():
        raise ActionPlanError(
            "La unidad de medida de materiales y suministros no existe."
        )

    # Verifica que el costo de materiales y suministros sea válido
    try:
        cost_ms = float(cost_ms)
    except ValueError:
        raise ActionPlanError(
            "El costo de materiales y suministros debe ser mayor o igual a 0."
        )
    if cost_ms < 0:
        raise ActionPlanError(
            "El costo de materiales y suministros debe ser mayor o igual a 0."
        )

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

    # Calcula el monto total de talento humano
    total_hl = work_hours * cost_hl

    # Calcula el monto total de materiales y suministros
    total_ms = amount_ms * cost_ms

    # Calcula el monto total del plan de acción
    total = total_hl + total_ms

    # Verifica el tipo de acción
    action_id = int(action) if action.isdigit() else None

    # Crea o selecciona un plan de acción de acuerdo al tipo de acción
    activity_id = None
    if action_id:
        # Seleciona el plan de acción con el id indicado y verifica que exista
        smt = db.select(ActionPlan).where(ActionPlan.id == action_id)
        action_plan_query = db.session.execute(smt).first()
        if not action_plan_query:
            raise ActionPlanError("El plan de acción no existe.")
        action_plan = action_plan_query[0]

        # Verifica que no haya una actividad con la misma descripción
        smt = (
            db.select(Activity)
            .where(Activity.action_plan_id == action_id)
            .where(Activity.description == activity)
        )
        if db.session.execute(smt).first():
            raise ActionPlanError("Ya existe una actividad con la misma descripción.")

        # Crea una actividad
        activity = Activity(
            action_id,
            charge_person_id,
            activity,
            start_date_t,
            deadline_t,
            work_hours,
            total,
        )
        db.session.add(activity)

        # Registra el evento en la base de datos
        events.add_event(
            "Planes de Acción",
            f"Agregar actividad '{activity.description}' al plan de acción '{action_plan.action}'",
        )

        activity_id = activity.id

    else:
        # Verifica que la acción sea válida
        validate_input_text(action, "Acción", ActionPlanError)

        # Verifica que no haya un plan de acción con la misma descripción
        smt = (
            db.select(ActionPlan)
            .where(ActionPlan.project_detail_id == project_detail_id)
            .where(ActionPlan.action == action)
        )

        # Crea un plan de acción
        action_plan = ActionPlan(action, project_detail_id)

        db.session.add(action_plan)
        db.session.commit()

        action_id = action_plan.id

        # Crea una actividad
        activity = Activity(
            action_plan.id,
            charge_person_id,
            activity,
            start_date_t,
            deadline_t,
            work_hours,
            total,
        )
        db.session.add(activity)

        # Registra los eventos en la base de datos
        events.add_event("Planes de Acción", f"Agregar plan de acción '{action}'")

        events.add_event(
            "Planes de Acción",
            f"Agregar actividad '{activity.description}' al plan de acción '{action}'",
        )

        activity_id = activity.id

    # Crea un registro de talento humano
    human_talent = HumanTalent(
        activity_id,
        work_hours,
        amount_person_hl,
        total_hl,
    )

    # Crear un registro de materiales y suministros
    materials_supplies = MaterialSupply(
        activity_id,
        measure_unit_ms_id,
        category_ms,
        description_ms,
        amount_ms,
        total_ms,
    )

    # Agrega los registros a la base de datos
    db.session.add(human_talent)
    db.session.add(materials_supplies)

    # Registra los eventos en la base de datos
    events.add_event(
        "Talentos Humanos",
        f"Agregar talento humano a la actividad '{activity.description}'",
    )

    events.add_event(
        "Materiales y Suministros",
        f"Agregar material y suministro '{materials_supplies.description}' a la actividad '{activity.description}'",
    )

    # Actualiza el monto del dato del proyecto
    update_project_total(human_talent.activity.action_plan.project_detail)


# ========== Eliminar Actividades de Planes de Acción ==========
def delete_activity_action_plan(action_plan_id: int, activity_id: int):
    """
    Elimina una actividad de un plan de acción.

    Lanza una excepción si:
        - El plan de acción no existe
        - La actividad no existe
    """
    # Selecciona el plan de acción y verifica que exista
    smt = db.select(ActionPlan).where(ActionPlan.id == action_plan_id)
    action_plan_query = db.session.execute(smt).first()
    if not action_plan_query:
        raise ActionPlanError("El plan de acción no existe.")
    action_plan = action_plan_query[0]

    # Selecciona la actividad y verifica que exista
    smt = db.select(Activity).where(Activity.id == activity_id)
    activity_query = db.session.execute(smt).first()
    if not activity_query:
        raise ActionPlanError("La actividad no existe.")
    deleted_activity = activity_query[0]

    # Elimina la actividad
    db.session.delete(deleted_activity)

    # Registra el evento en la base de datos
    events.add_event(
        "Planes de acción",
        f"Eliminar actividad '{deleted_activity.description}' del plan de acción '{action_plan.action}'",
    )

    # Actualiza el monto del dato del proyecto
    update_project_total(deleted_activity.action_plan.project_detail)


# ========== Editar Actividades de Planes de Acción ==========
def edit_activity_action_plan(
    action_plan_id: int,
    activity_id: int,
    material_supply_id: int,
    human_talent_id: int,
    action: str,
    activity: str,
    start_date: str,
    deadline: str,
    work_hours: str,
    charge_person_id: int,
    amount_person_hl: str,
    cost_hl: str,
    category_ms: str,
    description_ms: str,
    amount_ms: str,
    measure_unit_ms_id: int,
    cost_ms: str,
):
    """
    Edita una actividad de un plan de acción.

    Lanza una excepción si:
        - El plan de acción no existe
        - La actividad no es valida
        - La fecha de inicio no es valida
        - La fecha de finalización no es valida
        - La cantidad de horas de trabajo no es valida
        - La persona encargada no existe
        - El costo no es valido
        - La cantidad de personas de talento humano no es valida
        - El costo de talento humano no es valido
        - La categoría de materiales y suministros no es valida
        - La descripción de materiales y suministros no es valida
        - La cantidad de materiales y suministros no es valida
        - La unidad de medida de materiales y suministros no es valida
        - El costo de materiales y suministros no es valido
    """
    # Elimina espacios al comienzo y final del input del form
    action = action.strip()
    activity = activity.strip()
    start_date = start_date.strip()
    deadline = deadline.strip()
    work_hours = work_hours.strip()
    amount_person_hl = amount_person_hl.strip()
    cost_hl = cost_hl.strip()
    category_ms = category_ms.strip()
    description_ms = description_ms.strip()
    amount_ms = amount_ms.strip()
    cost_ms = cost_ms.strip()

    # Verifica que todos los campos estén completos
    if not all(
        [
            action,
            activity,
            start_date,
            deadline,
            work_hours,
            charge_person_id,
            amount_person_hl,
            cost_hl,
            category_ms,
            description_ms,
            amount_ms,
            cost_ms,
        ]
    ):
        raise ActionPlanError("Todos los campos son obligatorios.")

    # Selecciona el plan de acción y verifica que exista
    smt = db.select(ActionPlan).where(ActionPlan.id == action_plan_id)
    action_plan_query = db.session.execute(smt).first()
    if not action_plan_query:
        raise ActionPlanError("El plan de acción no existe.")
    edited_action_plan = action_plan_query[0]

    # Verifica que la persona encargada exista
    smt = db.select(User).where(User.id == charge_person_id)
    if not db.session.execute(smt).first():
        raise ActionPlanError("La persona encargada no existe.")

    # Verifica que la actividad sea válida
    validate_input_text(activity, "Actividad", ActionPlanError)

    # Selecciona la actividad y verifica que exista
    smt = db.select(Activity).where(Activity.id == activity_id)
    activity_query = db.session.execute(smt).first()
    if not activity_query:
        raise ActionPlanError("La actividad no existe.")
    edited_activity = activity_query[0]

    # Selecciona el talento humano y verifica que exista
    smt = db.select(HumanTalent).where(HumanTalent.id == human_talent_id)
    human_talent_query = db.session.execute(smt).first()
    if not human_talent_query:
        raise ActionPlanError("El talento humano no existe.")
    edited_human_talent = human_talent_query[0]

    # Verifica que la cantidad de personas de talento humano sea válida
    if not amount_person_hl.isdigit():
        raise ActionPlanError(
            "La cantidad de personas de talento humano debe ser un número entero."
        )
    amount_person_hl = int(amount_person_hl)

    # Verifica que el costo de talento humano sea válido
    try:
        cost_hl = float(cost_hl)
    except ValueError:
        raise ActionPlanError("El costo de talento humano debe ser mayor o igual a 0.")
    if cost_hl < 0:
        raise ActionPlanError("El costo de talento humano debe ser mayor o igual a 0.")

    # Selecciona el material y suministro y verifica que exista
    smt = db.select(MaterialSupply).where(MaterialSupply.id == material_supply_id)
    material_supply_query = db.session.execute(smt).first()
    if not material_supply_query:
        raise ActionPlanError("El material y suministro no existe.")
    edited_material_supply = material_supply_query[0]

    # Verifica que la categoría de materiales y suministros sea válida
    validate_input_text(
        category_ms, "Categoría de materiales y suministros", ActionPlanError
    )

    # Verifica que la descripción de materiales y suministros sea válida
    validate_input_text(
        description_ms, "Descripción de materiales y suministros", ActionPlanError
    )

    # Verifica que la cantidad de materiales y suministros sea válida
    if not amount_ms.isdigit():
        raise ActionPlanError(
            "La cantidad de materiales y suministros debe ser un número entero."
        )
    amount_ms = int(amount_ms)

    # Verifica que el costo de materiales y suministros sea válido
    try:
        cost_ms = float(cost_ms)
    except ValueError:
        raise ActionPlanError(
            "El costo de materiales y suministros debe ser mayor o igual a 0."
        )

    # Verifica que la unidad de medida exista
    smt = db.select(MeasureUnit).where(MeasureUnit.id == measure_unit_ms_id)
    if not db.session.execute(smt).first():
        raise ActionPlanError("La unidad de medida no existe.")

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

    # Calcula el costo total de talento humano
    total_hl = cost_hl * work_hours

    # Calcula el costo total de materiales y suministros
    total_ms = amount_ms * cost_ms

    # Calcula el costo total de la actividad
    total_activity = total_hl + total_ms

    # Edita el plan de acción
    edited_action_plan.action = action
    edited_activity.description = activity
    edited_activity.start_date = start_date_t
    edited_activity.deadline = deadline_t
    edited_activity.work_hours = work_hours
    edited_activity.charge_person_id = charge_person_id
    edited_activity.cost = total_activity

    # Edita el talento humano
    edited_human_talent.amount = amount_person_hl
    edited_human_talent.cost = total_hl

    # Edita el material y suministro
    edited_material_supply.category = category_ms
    edited_material_supply.description = description_ms
    edited_material_supply.amount = amount_ms
    edited_material_supply.cost = total_ms

    # Registra los eventos en la base de datos
    events.add_event(
        "Planes de acción",
        f"Editar plan de acción '{edited_activity.action_plan.action}'",
    )

    events.add_event(
        "Talentos Humanos",
        f"Editar talento humano '{edited_human_talent.activity.description}' del plan de acción '{edited_activity.action_plan.action}'",
    )

    events.add_event(
        "Materiales y Suministros",
        f"Editar material y suministro '{edited_material_supply.activity.description}' del plan de acción '{edited_activity.action_plan.action}'",
    )

    # Actualiza el monto del dato del proyecto
    update_project_total(edited_human_talent.activity.action_plan.project_detail)


# ========== Utilidades ==========
def update_project_total(project_detail):
    """Actualiza en la base de datos el monto total de los planes de acción
    asociados al dato del proyecto.

    Args:
        project_detail (ProjectDetail): Dato del proyecto.
    """
    total = 0
    for action_plan in project_detail.action_plans:
        for activity in action_plan.activities:
            total += activity.cost
    project_detail.cost = total
    db.session.commit()
