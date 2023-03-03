from flask import current_app, render_template


@current_app.errorhandler(403)
def forbidden(e):
    return render_template("errors/403.html"), 403


@current_app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html"), 404


@current_app.errorhandler(405)
def method_not_allowed(e):
    return render_template("errors/405.html"), 405


@current_app.errorhandler(500)
def internal_server_error(e):
    return render_template("errors/500.html"), 500
