import os
from app import app, db
from src.models import User, Role
from werkzeug.security import generate_password_hash

def create_db(db_name):
    app.app_context().push()
    if not os.path.exists(db_name):
        db.create_all()

    Role.insert_roles()

    user = User(username='admin', first_name='foo', last_name='bar',\
        rol=1, pass_hash=generate_password_hash("A123", 'sha256'))
    db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    create_db("data.db")
