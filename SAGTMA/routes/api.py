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
    db,
)


@current_app.route("/api/v1/users")
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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


@current_app.route("/api/v1/project-details-dropdown-data", methods=["GET"])
@login_required
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


@current_app.route("/api/v1/project-details", methods=["GET"])
@login_required
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
            "amount": pd.amount,
            "observations": pd.observations,
        }
        for pd, in result
    ]

    # Obtiene los datos del dropdown
    data = get_project_details_dropdown_data()

    return {"project_details": project_details, "dropdown_data": data}
