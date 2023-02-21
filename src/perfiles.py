from flask import Flask, render_template, request, url_for, redirect, flash, session, abort
from app import app, db
from src.models import User, Role
from src.decorators import login_required, requires_access_level

@app.route("/perfiles/")
@login_required
def perfiles():
    return render_template("perfiles.html", userlist=User.query.all(), roles=Role.query.all())

@app.route('/user/delete/<int:user_id>', methods=['POST'])
@login_required
@requires_access_level("Administrator")
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted')
    return redirect(url_for('perfiles'))

@app.route('/user/update/<int:user_id>', methods=['POST'])
@login_required
@requires_access_level("Administrator")
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.rol = Role.query.filter_by(name=request.form['user_rol']).first().id
    db.session.commit()
    flash('User update')
    return redirect(url_for('perfiles'))
