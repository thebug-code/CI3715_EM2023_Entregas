from flask import (Response, current_app, flash, redirect, render_template,
                   request, url_for, json)

from SAGTMA.utils import project, events
from SAGTMA.utils.decorators import login_required, requires_roles

from SAGTMA.models import Project, db

@current_app.route('/project-portfolio/',methods=['GET', 'POST'])
@requires_roles('Gerente de Operaciones')
def portfolio() -> Response:
    '''Muestra la lista de proyectos anadidos en el sistema'''
    if request.method == 'POST':
        # Obtiene los datos del formulario
        descrip = request.form.get('descrip-filter')

        stmt = db.select(Project).where(Project.description.like(f'%{descrip}%'))

        # Añade el evento de búsqueda
        events.add_search_project(descrip)
    else:
        # Selecciona los proyectos de la base de datos
        stmt = db.select(Project)

    result = db.session.execute(stmt).fetchall()
    projects = [r for r, in result]

    return render_template('manager/portfolio.html', projects=projects)

@current_app.route('/create-project/',methods=['GET', 'POST'])
@login_required
@requires_roles('Gerente de Operaciones')
def create_project() -> Response:
    '''Crear y anade un proyecto en la base de datos.'''
    if request.method == "POST":
        description = request.form['description']
        start_date = request.form['start_date']
        deadline = request.form['deadline']
        
        try:
            project.create_project(description, start_date, deadline)
        except project.CreateProjectError as e:
            flash(f'{e}')
        
    # Se permanece en la página
    return redirect(url_for('portfolio'))

@current_app.route('/project-portfolio/modify/<int:project_id>', methods=['POST'])
@login_required
@requires_roles('Gerente de Operaciones')
def modify_project(project_id):
    '''Modifica los datos de un proyecto en la base de datos'''
    description = request.form['description']
    start_date = request.form['start_date']
    deadline = request.form['deadline']

    try:
        project.modify_project(project_id, description, start_date, deadline)
    except project.CreateProjectError as e:
        flash(f'{e}')

    # Se permanece en la pagina
    return redirect(url_for('portfolio'))

@current_app.route('/project-portfolio/delete/<int:project_id>', methods=['post'])
@login_required
@requires_roles('Gerente de Operaciones')
def delete_project(project_id) -> Response:
    '''Elimina un proyecto de la base de datos'''
    # Busca el proyecto con el id indicado
    stmt = db.select(Project).where(Project.id == project_id)
    result = db.session.execute(stmt).first()
    if not result:
        flash('El proyecto indicado no existe')
        return redirect(url_for('portfolio'))

    # Elimina el proyecto de la base de datos
    db.session.delete(result[0])
    db.session.commit()

    # Registra el evento en la base de datos
    events.add_modify_project(result[0].description)

    flash('Proyecto eliminado exitosamente')

    # Se permanece en la pagina
    return redirect(url_for('portfolio'))

@current_app.route('/select', methods=['GET', 'POST'])
@login_required
@requires_roles('Gerente de Operaciones')
def select():
    if request.method == 'POST':
        project_id = request.form['project_id']
        stmt = db.select(Project).where(Project.id == project_id) #FALTA VERIFICAR
        rproject = db.session.execute(stmt).first()[0]

        project_list = [{
            'id': rproject.id,
            'description': rproject.description,
            'start_date': rproject.start_date.strftime("%Y-%m-%d"),
            'deadline': rproject.end_date.strftime("%Y-%m-%d")
        }]

        return json.dumps(project_list)

from urllib.parse import unquote as urllib_unquote

@current_app.template_filter('unquote')
def unquote(url):
    safe = app.jinja_env.filters['safe']
    return safe(urllib_unquote(url))
