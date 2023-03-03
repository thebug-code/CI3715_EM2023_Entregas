from flask import (
    Response,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    json,
)

from SAGTMA.utils import projects, events
from SAGTMA.utils.decorators import login_required, requires_roles

from SAGTMA.models import Project, db


@current_app.route("/project-portfolio/", methods=["GET", "POST"])
@requires_roles("Gerente de Operaciones")
def portfolio() -> Response:
    """Muestra la lista de proyectos anadidos en el sistema"""
    if request.method == "POST":
        # Obtiene los datos del formulario
        descrip = request.form.get("descrip-filter")

        stmt = db.select(Project).where(Project.description.like(f"%{descrip}%"))

        # Añade el evento de búsqueda
        events.add_search_project(descrip)
    else:
        # Selecciona los proyectos de la base de datos
        stmt = db.select(Project)

    result = db.session.execute(stmt).fetchall()
    _projects = [r for r, in result]
    print(f"Proyectos: {_projects}")

    return render_template("manager/portfolio.html", projects=_projects)


@current_app.route("/project-portfolio/add/", methods=["POST"])
@login_required
@requires_roles("Gerente de Operaciones")
def create_project() -> Response:
    """Crear y anade un proyecto en la base de datos."""
    description = request.form["description"]
    start_date = request.form["start_date"]
    deadline = request.form["deadline"]

    try:
        projects.create_project(description, start_date, deadline)
    except projects.CreateProjectError as e:
        flash(f"{e}")
        return redirect(url_for("portfolio"))

    # Se permanece en la página
    flash("Proyecto creado exitosamente")
    return redirect(url_for("portfolio"))


@current_app.route("/project-portfolio/modify/<int:project_id>/", methods=["POST"])
@login_required
@requires_roles("Gerente de Operaciones")
def modify_project(project_id):
    """Modifica los datos de un proyecto en la base de datos"""
    description = request.form["description"]
    start_date = request.form["start_date"]
    deadline = request.form["deadline"]

    try:
        projects.modify_project(project_id, description, start_date, deadline)
    except projects.CreateProjectError as e:
        flash(f"{e}")

    # Se permanece en la pagina
    return redirect(url_for("portfolio"))


@current_app.route("/project-portfolio/delete/<int:project_id>/", methods=["POST"])
@login_required
@requires_roles("Gerente de Operaciones")
def delete_project(project_id) -> Response:
    """Elimina un proyecto de la base de datos"""
    # Busca el proyecto con el id indicado
    stmt = db.select(Project).where(Project.id == project_id)
    result = db.session.execute(stmt).first()
    if not result:
        flash("El proyecto indicado no existe")
        return redirect(url_for("portfolio"))

    # Elimina el proyecto de la base de datos
    db.session.delete(result[0])
    db.session.commit()

    # Registra el evento en la base de datos
    events.add_delete_project(result[0].description)

    flash("Proyecto eliminado exitosamente")

    # Se permanece en la pagina
    return redirect(url_for("portfolio"))


@current_app.route(
    "/project-portfolio/modify/<int:project_id>/status/", methods=["POST"]
)
@login_required
@requires_roles("Gerente de Operaciones")
def change_project_status(project_id):
    """Activa o desactiva un proyecto de la base de datos"""
    # Busca el proyecto con el id indicado
    stmt = db.select(Project).where(Project.id == project_id)
    result = db.session.execute(stmt).first()
    if not result:
        flash("El proyecto indicado no existe")
        return redirect(url_for("portfolio"))

    # Verifica si hay que habilitar o desactivar proyecto
    if "enable_project" in request.form:
        result[0].active = True
    else:
        result[0].active = False

    db.session.commit()
    flash("Status de proyecto actualizado exitosamente")

    # Se permanece en la pagina
    return redirect(url_for("portfolio"))


@current_app.route("/select", methods=["GET", "POST"])
@login_required
@requires_roles("Gerente de Operaciones")
def select():
    if request.method == "POST":
        project_id = request.form["project_id"]
        stmt = db.select(Project).where(Project.id == project_id)  # FALTA VERIFICAR
        rproject = db.session.execute(stmt).first()[0]

        project_list = [
            {
                "id": rproject.id,
                "description": rproject.description,
                "start_date": rproject.start_date.strftime("%Y-%m-%d"),
                "deadline": rproject.end_date.strftime("%Y-%m-%d"),
            }
        ]

        return json.dumps(project_list)
