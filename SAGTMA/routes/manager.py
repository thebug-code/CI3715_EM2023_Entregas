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

from SAGTMA.models import Project, Project_Detail, db


# ========== Gerente de Operaciones ==========
@current_app.route("/project-portfolio/", methods=["GET", "POST"])
@requires_roles("Gerente de Operaciones")
def portfolio() -> Response:
    """Muestra la lista de proyectos anadidos en el sistema"""
    if request.method == "POST":
        # Obtiene los datos del formulario
        descrip = request.form.get("descrip-filter", '').lower().strip()
        
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
@login_required
@requires_roles("Gerente de Operaciones")
def create_project() -> Response:
    """Crear y anade un proyecto en la base de datos."""
    # Obtiene los datos del formulario
    description = request.form.get("description", '')
    start_date = request.form.get("start-date", '')
    deadline = request.form.get("deadline", '')

    try:
        projects.create_project(description, start_date, deadline)
    except projects.ProjectError as e:
        flash(f"{e}")
        return redirect(url_for("portfolio"))

    # Se permanece en la página
    flash("Proyecto creado exitosamente")
    return redirect(url_for("portfolio"))


@current_app.route("/project-portfolio/<int:project_id>/edit/", methods=["POST"])
@login_required
@requires_roles("Gerente de Operaciones")
def edit_project(project_id):
    """Modifica los datos de un proyecto en la base de datos"""
    # Obtiene los datos del formulario
    description = request.form.get("description", '')
    start_date = request.form.get("start-date", '')
    deadline = request.form.get("deadline", '')

    try:
        projects.edit_project(project_id, description, start_date, deadline)
    except projects.ProjectError as e:
        flash(f"{e}")

    # Se permanece en la pagina
    return redirect(url_for("portfolio"))


@current_app.route("/project-portfolio/<int:project_id>/delete/", methods=["POST"])
@login_required
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
@login_required
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

    if request.method == "POST":
        pass
       # Obtiene los datos del formulario
       #descrip = request.form.get("data-filter")

       #stmt = db.select(Project).where(Project.description.like(f"%{descrip}%"))

       # Añade el evento de búsqueda
       #events.add_event("Portafolio de Proyectos", f"Buscar '{descrip}'")
    else:
       # Selecciona los datos del proyecto en la base de datos
        stmt = (
            db.select(Project_Detail)
            .where(Project_Detail.project_id == project_id)
        )
    
    result = db.session.execute(stmt).fetchall()
    _project_details = [r for r, in result]
    
    return render_template("manager/project_details.html",\
        project_details=_project_details, project=_project)


@current_app.route("/project-details/<int:project_id>/register/", methods=["POST"])
@login_required
@requires_roles("Gerente de Operaciones")
def register_project_data(project_id) -> Response:
    """Registrar y anade un detalle de proyecto en la base de datos."""
    # Obtiene los datos del formulario
    vehicle = request.form.get("vehicle", '') 
    department = request.form.get("department", '')
    manager = request.form.get("manager", '')
    solution = request.form.get("solution", '')
    amount = request.form.get("amount", '')
    observations = request.form.get("observations", '')
    
    try:
        project_details.register_project_detail(
            project_id, 
            vehicle,
            department,
            manager,
            solution,
            amount, 
            observations
        )
    except project_details.ProjectDetailError as e:
        flash(f"{e}")
        return redirect(url_for("project_data", project_id=project_id))

    # Se permanece en la página
    flash("Detalle de proyecto registrado exitosamente")
    return redirect(url_for("project_data", project_id=project_id))
