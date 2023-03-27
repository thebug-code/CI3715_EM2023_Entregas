from flask import (
    Response,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from SAGTMA.utils import projects, events
from SAGTMA.utils.decorators import login_required, requires_roles

from SAGTMA.models import Project, db


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


# ========== Gerente de Proyectos ==========
# @current_app.route("/project-portfolio/<int:project_id>", methods=["GET", "POST"])
# @requires_roles("Gerente de Proyectos")
# def portfolio() -> Response:
#    """Muestra la lista de proyectos anadidos en el sistema"""
#    if request.method == "POST":
#        # Obtiene los datos del formulario
#        descrip = request.form.get("descrip-filter")
#
#        stmt = db.select(Project).where(Project.description.like(f"%{descrip}%"))
#
#        # Añade el evento de búsqueda
#        events.add_event("Portafolio de Proyectos", f"Buscar '{descrip}'")
#    else:
#        # Selecciona los proyectos de la base de datos
#        stmt = db.select(Project)
#
#    result = db.session.execute(stmt).fetchall()
#    _projects = [r for r, in result]
#
#    return render_template("manager/portfolio.html", projects=_projects)
