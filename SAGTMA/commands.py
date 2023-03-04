from random import randint
from datetime import date

from flask import current_app

from SAGTMA.models import Project, Role, User, Client, Event, db
from SAGTMA.utils import profiles


@current_app.cli.command("init-db")
def init_db_command():
    """Inicializa la base de datos y prepuebla la misma. Antes de poblarla
    borra los datos que tenía previamente.
    """
    db.drop_all()
    db.create_all()

    populate_db()


def populate_db():
    """Prepuebla la base de datos."""
    # Crea los roles
    user = Role("Usuario (Dummy)")
    admin = Role("Administrador")
    manager = Role("Gerente de Operaciones")
    analyst = Role("Analista de Operaciones")
    mechanics_supervisor = Role("Supervisor del Área de Mecánica General")
    painting_supervisor = Role("Supervisor del Área de Latonería y Pintura")
    mechanics_specialist = Role("Especialista en Mecánica")
    electronics_specialist = Role("Especialista en Electrónica")
    electricity_specialist = Role("Especialista en Electricidad")

    roles = [
        user,
        admin,
        analyst,
        manager,
        mechanics_supervisor,
        painting_supervisor,
        mechanics_specialist,
        electronics_specialist,
        electricity_specialist,
    ]

    db.session.add_all(roles)

    # Añade un usuario administrador
    admin_user = User(
        "admin", "Juanito", "Alimaña", profiles.hash_password("Admin123."), admin
    )
    db.session.add(admin_user)

    # Añade usuarios dummy de distintos roles
    names = ["Juan", "Pedro", "Pablo", "Luis", "Carlos", "Jorge", "Miguel"]
    surnames = ["Pérez", "González", "Gómez", "Rodríguez", "López", "Martínez"]
    roles_slice = roles[2:]
    for i in range(10):
        user = User(
            f"user{i}",
            names[i % len(names)],
            surnames[i % len(surnames)],
            profiles.hash_password("User123."),
            roles_slice[i % len(roles_slice)],
        )

        db.session.add(user)

    # Añade proyectos dummy
    for i in range(1, 11):
        project = Project(
            f"Proyecto Automotriz {i}", date(2021, 4, 1), date(2023, 4, 1)
        )

        db.session.add(project)

    # Itera sobre los usuarios y los proyectos para asignarles proyectos
    stmt = db.select(User)
    for (user,) in db.session.execute(stmt):
        # Toma una cantidad aleatoria de proyectos al azar y los asigna al usuario
        stmt = db.select(Project).order_by(db.func.random()).limit(randint(0, 5))
        for (project,) in db.session.execute(stmt):
            user.projects.append(project)

    # Añade un cliente dummy
    client = Client(
        "V-82482795",
        "Carlos",
        "Marx",
        date(1974, 1, 16),
        "+584254635142",
        "carlmarx@usb.ve",
        "La Castellana, Caracas, Al lado del portón rojo",
    )

    db.session.add(client)

    # Crea eventos de prueba
    stmt = db.select(User)
    for (user,) in db.session.execute(stmt):
        new_event = Event(
            user, "Perfiles de Usuarios", f"Agregar usuario '{user.username}'"
        )
        db.session.add(new_event)

    db.session.commit()
