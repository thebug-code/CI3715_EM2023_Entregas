from flask import Response, abort, current_app, render_template

from SAGTMA.utils.decorators import requires_roles


@current_app.route('/project-portfolio',methods=['GET', 'POST'])
@requires_roles('Gerente de Operaciones')
def portfolio() -> Response:
    return render_template('manager/portfolio.html')

@current_app.route('/create-project',methods=['GET', 'POST'])
@requires_roles('Gerente de Operaciones')
def create_project() -> Response:
    abort(404)
