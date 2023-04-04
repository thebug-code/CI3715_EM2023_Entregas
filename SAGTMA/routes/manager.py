from flask import (
    Response,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from SAGTMA.utils import projects, events, project_details
from SAGTMA.utils.decorators import login_required, requires_roles

from SAGTMA.models import Project, ProjectDetail, Vehicle, Department, User, db


# ========== Gerente de Operaciones ==========
@current_app.route("/project-portfolio/", methods=["GET", "POST"])
@requires_roles("Gerente de Operaciones")
def portfolio() -> Response:
    """Muestra la lista de proyectos anadidos en el sistema"""
    if request.method == "POST":
        # Obtiene los datos del formulario
        descrip = request.form.get("descrip-filter", "").lower().strip()

        # WHERE description LIKE '%descrip%'
        stmt = db.select(Project).where(Project.description.like(f"%{descrip}%"))

        # Añade el evento de búsqueda
        events.add_event("Portafolio de Proyectos", f"Buscar '{descrip}'")
    else:
        # Selecciona los proyectos de la base de datos
        stmt = db.select(Project)

    result = db.session.execute(stmt).fetchall()
    _projects = [r for r, in result]

    return render_template("manager/portfolio.html", projects=_projects)


@current_app.route("/project-portfolio/add/", methods=["POST"])
@requires_roles("Gerente de Operaciones")
def create_project() -> Response:
    """Crear y anade un proyecto en la base de datos."""
    # Obtiene los datos del formulario
    description = request.form.get("description", "")
    start_date = request.form.get("start-date", "")
    deadline = request.form.get("deadline", "")

    try:
        projects.create_project(description, start_date, deadline)
    except projects.ProjectError as e:
        flash(f"{e}")
        return redirect(url_for("portfolio"))

    # Se permanece en la página
    flash("Proyecto creado exitosamente")
    return redirect(url_for("portfolio"))


@current_app.route("/project-portfolio/<int:project_id>/edit/", methods=["POST"])
@requires_roles("Gerente de Operaciones")
def edit_project(project_id):
    """Modifica los datos de un proyecto en la base de datos"""
    # Obtiene los datos del formulario
    description = request.form.get("description", "")
    start_date = request.form.get("start-date", "")
    deadline = request.form.get("deadline", "")

    try:
        projects.edit_project(project_id, description, start_date, deadline)
    except projects.ProjectError as e:
        flash(f"{e}")

    # Se permanece en la pagina
    return redirect(url_for("portfolio"))


@current_app.route("/project-portfolio/<int:project_id>/delete/", methods=["POST"])
@requires_roles("Gerente de Operaciones")
def delete_project(project_id) -> Response:
    """Elimina un proyecto de la base de datos"""
    try:
        projects.delete_project(project_id)
    except projects.ProjectError as e:
        flash(f"{e}")
        return redirect(url_for("portfolio"))

    # Se permanece en la pagina
    flash("Proyecto eliminado exitosamente")
    return redirect(url_for("portfolio"))


@current_app.route("/project-portfolio/edit/<int:project_id>/status/", methods=["POST"])
@requires_roles("Gerente de Operaciones")
def change_project_status(project_id):
    """Activa o desactiva un proyecto de la base de datos"""
    try:
        projects.toggle_project_status(project_id)
    except projects.ProjectError as e:
        flash(f"{e}")
        return redirect(url_for("portfolio"))

    # Se permanece en la pagina
    flash("Status de proyecto actualizado exitosamente")
    return redirect(url_for("portfolio"))


# ========== Detalles del proyecto ==========
@current_app.route("/project-details/<int:project_id>/", methods=["GET", "POST"])
@requires_roles("Gerente de Operaciones")
def project_data(project_id) -> Response:
    """Muestra la lista de datos de proyectos anadidos en el sistema"""
    # Selecciona el proyecto con el id indicado y verifica que exista
    stmt = db.select(Project).where(Project.id == project_id)
    project_query = db.session.execute(stmt).first()
    if not project_query:
        flash("El proyecto indicado no existe")
        return redirect(url_for("portfolio"))
    # Obtiene el proyecto
    _project = project_query[0]

    # Selecciona los detalles del proyecto con el id indicado y une las tablas
    # necesarias para mostrar los datos
    stmt = (
        db.select(ProjectDetail)
        .where(ProjectDetail.project_id == project_id)
        .join(Vehicle)
        .join(User)
        .join(Department)
    )

    if request.method == "POST":
        # Obtiene los datos del formulario
        detail = request.form.get("data-filter", "").lower().strip()

        if detail:
            # WHERE (license_plate) LIKE '%detail%' OR
            #       (department) LIKE '%detail%' OR
            #       (manager) LIKE '%detail%' OR
            #       (problem) LIKE '%detail%' OR
            #       (solution) LIKE '%detail%' OR
            #       (observations) LIKE '%detail%'
            stmt = stmt.where(
                db.or_(
                    Vehicle.license_plate.like(f"%{detail}%"),
                    Department.description.like(f"%{detail}%"),
                    User.id_number.like(f"%{detail}%"),
                    Vehicle.problem.like(f"%{detail}%"),
                    ProjectDetail.solution.like(f"%{detail}%"),
                    ProjectDetail.observations.like(f"%{detail}%"),
                )
            )
        # Registra el evento en la base de datos
        events.add_event(
            "Detalles de Proyecto",
            f"Buscar '{detail}' del proyecto '{_project.description}'",
        )
    else:
        # Selecciona los datos del proyecto con el id indicado
        stmt = db.select(ProjectDetail).where(ProjectDetail.project_id == project_id)

    result = db.session.execute(stmt).fetchall()
    _project_details = [r for r, in result]

    return render_template(
        "manager/project_details.html",
        project_details=_project_details,
        project=_project,
    )


@current_app.route("/project-details/<int:project_id>/register/", methods=["POST"])
@requires_roles("Gerente de Operaciones")
def register_project_data(project_id) -> Response:
    """Registrar y anade un detalle de proyecto en la base de datos."""
    # Obtiene los datos del formulario
    vehicle = request.form.get("vehicle", "")
    department = request.form.get("department", "")
    manager = request.form.get("manager", "")
    solution = request.form.get("solution", "")
    cost = request.form.get("cost", "")
    observations = request.form.get("observations", "")

    try:
        project_details.register_project_detail(
            project_id, vehicle, department, manager, solution, cost, observations
        )
    except project_details.ProjectDetailError as e:
        flash(f"{e}")
        return redirect(url_for("project_data", project_id=project_id))

    # Se permanece en la página
    flash("Detalle de proyecto registrado exitosamente")
    return redirect(url_for("project_data", project_id=project_id))


@current_app.route("/project-details/<int:detail_id>/edit/", methods=["POST"])
@requires_roles("Gerente de Operaciones")
def edit_project_data(detail_id) -> Response:
    """Registrar y anade un detalle de proyecto en la base de datos."""
    # Obtiene los datos del formulario
    vehicle = request.form.get("vehicle", "")
    department = request.form.get("department", "")
    manager = request.form.get("manager", "")
    solution = request.form.get("solution", "")
    cost = request.form.get("cost", "")
    observations = request.form.get("observations", "")
    project_id = int(request.form.get("project-id"))

    try:
        project_details.edit_project_detail(
            detail_id, vehicle, department, manager, solution, cost, observations
        )
    except project_details.ProjectDetailError as e:
        flash(f"{e}")
        return redirect(url_for("project_data", project_id=project_id))

    # Se permanece en la página
    flash("Detalle de proyecto registrado exitosamente")
    return redirect(url_for("project_data", project_id=project_id))


@current_app.route("/project-details/<int:detail_id>/delete/", methods=["POST"])
@requires_roles("Gerente de Operaciones")
def delete_project_data(detail_id) -> Response:
    """Elimina un detalle de proyecto de la base de datos"""
    # Obtiene el id del proyecto
    project_id = int(request.form.get("project-id"))

    try:
        project_details.delete_project_detail(detail_id)
    except project_details.ProjectDetailError as e:
        flash(f"{e}")
        return redirect(url_for("project_data", project_id=project_id))

    # Se permanece en la pagina
    flash("Detalle de proyecto eliminado exitosamente")
    return redirect(url_for("project_data", project_id=project_id))
