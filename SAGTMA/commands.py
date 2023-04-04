from random import randint, choice
from datetime import date

from flask import current_app
from sqlalchemy import func

from SAGTMA.models import (
    Project,
    Role,
    User,
    Client,
    Vehicle,
    Department,
    ProjectDetail,
    db,
)
from SAGTMA.utils.auth import hash_password


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
        hash_password("Admin123."),
        roles[1],
    )
    db.session.add(admin_user)

    # Añade usuarios dummy de distintos roles
    names = ["Juan", "Pedro", "Pablo", "Luis", "Carlos", "Jorge", "Miguel"]
    surnames = ["Pérez", "González", "Gómez", "Rodríguez", "López", "Martínez"]
    prefixes = ["V", "E", "J", "G", "C"]
    id_numbers = [
        f"{choice(prefixes)}-{randint(10000000, 99999999)}" for _ in range(10)
    ]
    roles_slice = roles[2:]
    for i in range(10):
        user = User(
            id_numbers[i],
            f"user{i}",
            names[i % len(names)],
            surnames[i % len(surnames)],
            hash_password("User123."),
            roles_slice[i % len(roles_slice)],
        )

        db.session.add(user)

    # Añade proyectos dummy
    for i in range(1, 11):
        project = Project(
            f"Proyecto Automotriz {i}", date(2021, 4, 1), date(2023, 4, 1)
        )

        db.session.add(project)

    # Añade dos clientes dummy con dos vehículos
    client0 = Client(
        "V-82482795",
        "Carlos",
        "Marx",
        date(1974, 1, 16),
        "+584254635142",
        "carlmarx@usb.ve",
        "La Castellana, Caracas, Al lado del portón rojo",
    )

    client1 = Client(
        "V-82482799",
        "Fidel",
        "Castro",
        date(1970, 4, 16),
        "+584249745787",
        "fidelcastro@usb.ve",
        "La california, Caracas, Al lado del kiosko verde",
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

    client0.vehicles.append(car1)
    client1.vehicles.append(car2)

    db.session.add_all([client0, client1])

    # Anade departamentos
    dept_names = [
        "Mecánica",
        "Estructura",
        "Revestimiento",
        "Electricidad",
        "Electrónica",
    ]

    depts = [Department(dept) for dept in dept_names]
    db.session.add_all(depts)

    # Anade dos datos de proyectos

    # Selecciona dos proyectos aleatorios y le asignas un dato de proyecto
    projects = Project.query.order_by(func.random()).limit(2).all()
    projects[0].active = True
    projects[1].active = True

    # Selecciona el departamento de Estructura y le asigna un dato de proyecto
    smt = db.select(Department).where(Department.description == "Estructura")
    dept1 = db.session.execute(smt).first()[0]

    # Selecciona el departamento de Mecánica y le asigna un dato de proyecto
    smt = db.select(Department).where(Department.description == "Mecánica")
    dept2 = db.session.execute(smt).first()[0]

    # Selecciona dos usuarios aleatorios y les asigna un dato de proyecto
    users = User.query.order_by(func.random()).limit(2).all()

    detail0 = ProjectDetail(
        projects[0].id,
        car1.id,
        depts[0].id,
        users[0].id,
        "Cambiar el aceite",
        150,
        "Aceite sintético",
    )

    detail1 = ProjectDetail(
        projects[1].id,
        car2.id,
        depts[1].id,
        users[1].id,
        "Quitarle las alas",
        200,
        "Ninguna",
    )
    db.session.add_all([detail0, detail1])

    db.session.commit()
