from flask import (Response, current_app, flash, redirect, render_template,
                   request, url_for, json)

from SAGTMA.utils import project, events
from SAGTMA.utils.decorators import login_required, requires_roles

from SAGTMA.models import Project, db

@current_app.route('/project-portfolio/',methods=['GET', 'POST'])
@requires_roles('Gerente de Operaciones')
def portfolio() -> Response:
    '''Muestra la lista de proyectos anadidos en el sistema'''
        
    # SE ASUME QUE ES METDO GET, FALTA BARRA DE BUSQUEDA
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

@current_app.route('/modify-project/<int:project_id>', methods=['POST'])
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
