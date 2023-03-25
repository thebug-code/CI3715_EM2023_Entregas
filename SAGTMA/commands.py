from random import randint, choice
from datetime import date

from flask import current_app

from SAGTMA.models import Project, Role, User, Client, Vehicle, db
from SAGTMA.utils import profiles


@current_app.cli.command("init-db")
def init_db_command():
    """
    Inicializa la base de datos y prepuebla la misma. Antes de poblarla
    borra los datos que tenía previamente.
    """
    db.drop_all()
    db.create_all()

    populate_db()


def populate_db():
    """Prepuebla la base de datos."""
    # Crea los roles
    role_names = [
        "Usuario (Dummy)",
        "Administrador",
        "Gerente de Operaciones",
        "Analista de Operaciones",
        "Gerente de Mecánica General",
        "Especialista en Mecánica",
        "Gerente de Estructura",
        "Especialista en Estructura",
        "Gerente de Revestimiento",
        "Especialista en Revestimiento",
        "Gerente de Electrónica",
        "Especialista en Electrónica",
        "Gerente de Electricidad",
        "Especialista en Electricidad",
        "Gerente de Proyectos",
    ]

    roles = [Role(name) for name in role_names]
    db.session.add_all(roles)

    # Añade un usuario administrador
    admin_user = User(
        "V-20786789",
        "admin",
        "Juanito",
        "Alimaña",
        profiles.hash_password("Admin123."),
        roles[1]
    )
    db.session.add(admin_user)

    # Añade usuarios dummy de distintos roles
    names = ["Juan", "Pedro", "Pablo", "Luis", "Carlos", "Jorge", "Miguel"]
    surnames = ["Pérez", "González", "Gómez", "Rodríguez", "López", "Martínez"]
    prefixes = ['V', 'E', 'J', 'G', 'C']
    id_numbers = ( 
        [f"{choice(prefixes)}-{randint(10000000, 99999999)}" for _ in range(10)]
    )
    roles_slice = roles[2:]
    for i in range(10):
        user = User(
            id_numbers[i],
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

    # Añade un cliente dummy con dos vehículos
    client = Client(
        "V-82482795",
        "Carlos",
        "Marx",
        date(1974, 1, 16),
        "+584254635142",
        "carlmarx@usb.ve",
        "La Castellana, Caracas, Al lado del portón rojo",
    )

    car1 = Vehicle(
        "ABC-123",
        "Tesla",
        "Model S",
        2022,
        "123456789",
        "987654321",
        "Rojo",
        "El carro no arranca",
    )
    car2 = Vehicle(
        "BAR-12Y",
        "Toyota",
        "Festiva",
        1998,
        "XTYVFUYYJNNVVG98KJ",
        "XT78FUYYJNNVVG98KJ",
        "Negro",
        "El carro vuela",
    )

    client.vehicles.append(car1)
    client.vehicles.append(car2)

    db.session.add(client)
    db.session.commit()
