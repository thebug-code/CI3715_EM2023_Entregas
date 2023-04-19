from flask import current_app, request, json

from SAGTMA.utils.decorators import login_required, requires_roles

from SAGTMA.models import (
    User,
    Project,
    Client,
    Vehicle,
    Department,
    Role,
    ProjectDetail,
    MeasureUnit,
    ActionPlan,
    Activity,
    MaterialSupply,
    HumanTalent,
    db,
)


@current_app.route("/api/v1/users")
@requires_roles("Administrador")
def api_users():
    # SELECT * FROM user
    stmt = db.select(User)

    # Obtiene los parámetros de la request para filtrar por id
    # y filtra de ser necesario
    user_id = request.args.get("id")
    if user_id:
        stmt = stmt.where(User.id == user_id)

    # Consulta los usuarios requeridos
    result = db.session.execute(stmt).fetchall()
    users = [
        {
            "id": user.id,
            "id_number": user.id_number,
            "username": user.username,
            "names": user.names,
            "surnames": user.surnames,
            "role_id": user.role.id,
        }
        for user, in result
    ]

    # Consulta los roles
    stmt = db.select(Role).where(Role.id != 1)
    result = db.session.execute(stmt).fetchall()
    roles = [{"id": r.id, "name": r.name} for r, in result]

    return {"users": users, "roles": roles}


@current_app.route("/api/v1/projects")
@requires_roles("Gerente de Operaciones")
def api_projects():
    stmt = db.select(Project)

    # Obtiene los parámetros de la request para filtrar por id
    # y filtra de ser necesario
    project_id = request.args.get("id")
    if project_id:
        stmt = stmt.where(Project.id == project_id)

    # Consulta los proyectos requeridos
    result = db.session.execute(stmt).fetchall()
    projects = [
        {
            "id": project.id,
            "description": project.description,
            "start_date": project.start_date.strftime("%Y-%m-%d"),
            "deadline": project.end_date.strftime("%Y-%m-%d"),
        }
        for project, in result
    ]

    return projects


@current_app.route("/api/v1/clients")
@requires_roles("Analista de Operaciones")
def api_clients():
    stmt = db.select(Client)

    # Obtiene los parámetros de la request para filtrar por id
    # y filtra de ser necesario
    client_id = request.args.get("id")
    if client_id:
        stmt = stmt.where(Client.id == client_id)

    # Consulta los clientes requeridos
    result = db.session.execute(stmt).fetchall()
    clients = [
        {
            "id": client.id,
            "id_number": client.id_number,
            "names": client.names,
            "surnames": client.surnames,
            "birthdate": client.birthdate.strftime("%Y-%m-%d"),
            "phone_number": client.phone_number,
            "email": client.email,
            "address": client.address,
        }
        for client, in result
    ]

    return clients


@current_app.route("/api/v1/vehicles")
@requires_roles("Analista de Operaciones")
def api_vehicles():
    stmt = db.select(Vehicle)

    # Obtiene los parámetros de la request para filtrar por id
    # y filtra de ser necesario
    vehicle_id = request.args.get("id")
    if vehicle_id:
        stmt = stmt.where(Vehicle.id == vehicle_id)

    # Consulta los clientes requeridos
    result = db.session.execute(stmt).fetchall()
    vehicles = [
        {
            "license_plate": vehicle.license_plate,
            "brand": vehicle.brand,
            "model": vehicle.model,
            "year": vehicle.year,
            "body_number": vehicle.body_number,
            "engine_number": vehicle.engine_number,
            "color": vehicle.color,
            "problem": vehicle.problem,
        }
        for vehicle, in result
    ]

    return vehicles


@current_app.route("/api/v1/departments")
@requires_roles("Administrador")
def api_departments():
    stmt = db.select(Department)

    # Obtiene los parámetros de la request para filtrar por id
    # y filtra de ser necesario
    dept_id = request.args.get("id")
    if dept_id:
        stmt = stmt.where(Department.id == dept_id)

    # Consulta los departamentos requeridos
    result = db.session.execute(stmt).fetchall()
    depts = [
        {
            "id": dept.id,
            "description": dept.description,
        }
        for dept, in result
    ]

    return depts


@current_app.route("/api/v1/project-details-dropdown-data")
@requires_roles("Gerente de Operaciones")
def get_project_details_dropdown_data():
    # SELECT * FROM user
    stmt = db.select(User)
    result = db.session.execute(stmt).fetchall()
    users = [
        {"id": u.id, "names": u.names, "surnames": u.surnames, "id_number": u.id_number}
        for u, in result
    ]

    # SELECT * FROM department
    stmt = db.select(Department)
    result = db.session.execute(stmt).fetchall()
    departments = [{"id": d.id, "description": d.description} for d, in result]

    # SELECT * FROM vehicle
    stmt = db.select(Vehicle)
    result = db.session.execute(stmt).fetchall()
    vehicles = [
        {
            "id": v.id,
            "license_plate": v.license_plate,
            "brand": v.brand,
            "id_number": v.owner.id_number,
            "names": v.owner.names,
            "surnames": v.owner.surnames,
            "problem": v.problem,
        }
        for v, in result
    ]

    data = {"users": users, "departments": departments, "vehicles": vehicles}

    return data


@current_app.route("/api/v1/project-details")
@requires_roles("Gerente de Operaciones")
def api_project_details():
    # SELECT * FROM project_detail
    stmt = db.select(ProjectDetail)

    # Obtiene los parámetros de la request para filtrar por id
    # y filtra de ser necesario
    project_detail_id = request.args.get("id")
    if project_detail_id:
        stmt = stmt.where(ProjectDetail.id == project_detail_id)

    # Consulta los detalles de proyecto requeridos
    result = db.session.execute(stmt).fetchall()
    project_details = [
        {
            "id": pd.id,
            "project_id": pd.project.id,
            "manager_id": pd.manager.id,
            "department_id": pd.department.id,
            "vehicle_id": pd.vehicle.id,
            "solution": pd.solution,
            "cost": pd.cost,
            "observations": pd.observations,
        }
        for pd, in result
    ]

    # Obtiene los datos del dropdown
    data = get_project_details_dropdown_data()

    return {"project_details": project_details, "dropdown_data": data}


@current_app.route("/api/v1/measurement-units/")
@requires_roles("Gerente de Operaciones", "Administrador")
def api_measure_units():
    stmt = db.select(MeasureUnit)

    # Obtiene los parámetros de la request para filtrar por id
    # y filtra de ser necesario
    measure_unit_id = request.args.get("measurement-unit-id")
    if measure_unit_id:
        stmt = stmt.where(MeasureUnit.id == measure_unit_id)

    # Consulta las unidades de medida requeridas
    result = db.session.execute(stmt).fetchall()
    measure_units = [
        {
            "id": uom.id,
            "dimension": uom.dimension,
            "unit": uom.unit,
        }
        for uom, in result
    ]

    return measure_units


@current_app.route("/api/v1/action-plans-dropdown-data")
@requires_roles("Gerente de Operaciones")
def get_action_plans_dropdown_data():
    # SELECT * FROM USER
    stmt = db.select(User)
    result = db.session.execute(stmt).fetchall()

    users = [{"id": u.id, "names": u.names, "surnames": u.surnames} for u, in result]

    # Obtiene los parámetros de la request para filtrar por id
    # y filtra de ser necesario
    project_detail_id = request.args.get("id")

    stmt = db.select(ActionPlan)
    if project_detail_id:
        stmt = stmt.where(ActionPlan.project_detail_id == project_detail_id)

    # Consulta los planes de acción requeridos
    result = db.session.execute(stmt).fetchall()
    actions = [{"id": a.id, "description": a.action} for a, in result]

    # Obtiene las unidades de medida
    measure_units = api_measure_units()

    return {"users": users, "actions": actions, "measureUnits": measure_units}


@current_app.route("/api/v1/action-plans")
@requires_roles("Gerente de Operaciones")
def api_action_plans():
    # SELECT * FROM ActionPlan JOIN Activity ON ActionPlan.id = Activity.action_plan_id
    stmt = db.select(ActionPlan, Activity).join(
        Activity, ActionPlan.id == Activity.action_plan_id
    )

    # Obtiene los parámetros de la request para filtrar por id
    # y filtra de ser necesario
    action_plan_id = request.args.get("action_id")
    activity_id = request.args.get("activity_id")
    material_id = request.args.get("material_supply_id")
    human_talent_id = request.args.get("human_talent_id")

    filters = []

    if action_plan_id:
        filters.append(ActionPlan.id == action_plan_id)

    if activity_id:
        filters.append(Activity.id == activity_id)

    if material_id:
        filters.append(MaterialSupply.id == material_id)

    if human_talent_id:
        filters.append(HumanTalent.id == human_talent_id)

    # Agrega las condiciones de filtrado a stmt
    if filters:
        stmt = (
            db.session.query(ActionPlan, Activity, HumanTalent, MaterialSupply)
            .join(Activity, ActionPlan.id == Activity.action_plan_id)
            .join(HumanTalent, Activity.id == HumanTalent.activity_id)
            .join(MaterialSupply, Activity.id == MaterialSupply.activity_id)
            .filter(*filters)
        )

    # Consulta los planes de acción y actividades requeridas
    results = db.session.execute(stmt).fetchall()

    # Construye la lista de diccionarios con los resultados
    action_plans = {}
    for r in results:
        ap = r[0]
        act = r[1]
        if ap.id not in action_plans:
            # Si es la primera vez que se encuentra este ActionPlan,
            # se crea un nuevo diccionario para almacenar sus datos
            action_plans[ap.id] = {"id": ap.id, "action": ap.action, "activities": []}
        # Se agrega la actividad correspondiente al diccionario del ActionPlan
        action_plans[ap.id]["activities"].append(
            {
                "id": act.id,
                "description": act.description,
                "start_date": act.start_date.strftime("%Y-%m-%d"),
                "deadline": act.deadline.strftime("%Y-%m-%d"),
                "charge_person_id": act.charge_person_id,
                "work_hours": act.work_hours,
                "cost": act.cost,
                "human_talents": [
                    {
                        "id": ht.id,
                        "amount_persons": ht.amount,
                        "cost_hl": ht.cost / act.work_hours,
                    }
                    for ht in act.human_talents
                ],
                "material_supplies": [
                    {
                        "id": ms.id,
                        "category": ms.category,
                        "description": ms.description,
                        "amount": ms.amount,
                        "unit_id": ms.measure_unit_id,
                        "cost": ms.cost / ms.amount,
                    }
                    for ms in act.materials
                ],
            }
        )

    # Obtiene los datos del dropdown para hallar los nombres de los usuarios
    data = get_action_plans_dropdown_data()

    return {
        "actionPlans": action_plans,
        "users": data["users"],
        "measureUnits": data["measureUnits"],
    }