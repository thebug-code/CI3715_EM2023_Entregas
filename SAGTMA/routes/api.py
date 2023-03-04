from flask import current_app, request, json

from SAGTMA.utils.decorators import login_required, requires_roles

from SAGTMA.models import Project, db


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
