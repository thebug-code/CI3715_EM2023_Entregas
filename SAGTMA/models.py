import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Role(db.Model):
    """Modelo de rol."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    users = db.relationship("User", backref="role")

    def __init__(self, name: str):
        self.name = name

    def __repr__(self) -> str:
        return f"Role<{self.name}>"


class User(db.Model):
    """Modelo de usuario."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable=False)
    id_number = db.Column(db.String(10), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    names = db.Column(db.String(50), nullable=False)
    surnames = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(80), nullable=False)

    # Relación 1:n entre usuarios y eventos
    events = db.relationship("Event", backref="user", cascade="all, delete-orphan")

    # Relación 1:n entre usuarios y detalles de proyectos (mosca con el
    # cascade)
    project_details = db.relationship(
        "ProjectDetail", backref="manager", cascade="all, delete-orphan"
    )

    # Relación 1:N entre usuarios y actividades (mosca con el cascade)
    activities = db.relationship(
        "Activity", backref="charge_person", cascade="all, delete-orphan"
    )

    def __init__(
        self,
        id_number: str,
        username: str,
        names: str,
        surnames: str,
        password: str,
        role: Role,
    ):
        self.id_number = id_number
        self.username = username
        self.names = names
        self.surnames = surnames
        self.password = password
        self.role = role

    def __repr__(self) -> str:
        return f"User<{self.username}: {self.names} {self.surnames}, {self.role.name}>"


class Project(db.Model):
    """Modelo de proyecto."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(100), unique=True, nullable=False)
    active = db.Column(db.Boolean, default=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    # Relación 1:n entre proyectos y detalles de proyectos
    project_details = db.relationship(
        "ProjectDetail", backref="project", cascade="all, delete-orphan"
    )

    def __init__(self, description: str, start_date, end_date):
        self.description = description
        self.start_date = start_date
        self.end_date = end_date

    def __repr__(self) -> str:
        return f'Project<{self.description}: {self.start_date} - {self.end_date}, {"Activo" if self.active else "Inactivo"}>'


class ProjectDetail(db.Model):
    """Modelo de detalles de proyectos."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicle.id"), nullable=False)
    department_id = db.Column(
        db.Integer, db.ForeignKey("department.id"), nullable=False
    )
    project_manager_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    solution = db.Column(db.String(100), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    observations = db.Column(db.String(100), nullable=False)

    def __init__(
        self,
        project_id: int,
        vehicle_id: int,
        department_id: int,
        project_manager_id: int,
        solution: str,
        cost: float,
        observations: str,
    ):
        self.project_id = project_id
        self.vehicle_id = vehicle_id
        self.department_id = department_id
        self.project_manager_id = project_manager_id
        self.solution = solution
        self.cost = cost
        self.observations = observations

    def __repr__(self) -> str:
        return f"ProjectDetail<{self.solution}: {self.cost} - {self.observations}>"


class Event(db.Model):
    """Modelo de evento."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    module = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    time = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now)

    def __init__(self, user: User, module: str, description: str):
        self.user = user
        self.module = module
        self.description = (
            description if len(description) <= 80 else f"{description[:77]}..."
        )

    def __repr__(self) -> str:
        return f"Event<{self.user.username}: {self.module} - {self.type}>"


class Client(db.Model):
    """Modelo de cliente."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_number = db.Column(db.String(10), unique=True, nullable=False)
    names = db.Column(db.String(50), nullable=False)
    surnames = db.Column(db.String(50), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(120), nullable=False)

    # Relación 1:n entre clientes y vehículos
    vehicles = db.relationship("Vehicle", backref="owner", cascade="all, delete-orphan")

    def __init__(
        self,
        id_number: str,
        names: str,
        surnames: str,
        birthdate,
        phone_number: str,
        email: str,
        address: str,
    ):
        self.id_number = id_number
        self.names = names
        self.surnames = surnames
        self.birthdate = birthdate
        self.phone_number = phone_number
        self.email = email
        self.address = address

    def __repr__(self) -> str:
        return f"Client<{self.id_number}: {self.names} {self.surnames}>"


class Vehicle(db.Model):
    """Modelo de vehículo."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=False)
    license_plate = db.Column(db.String(10), unique=True, nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    body_number = db.Column(db.String(20), nullable=False)
    engine_number = db.Column(db.String(20), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    problem = db.Column(db.String(120), nullable=False)

    # Relacion 1:N entre vehículos y detalles de proyectos (ojo con el cascade)
    project_details = db.relationship(
        "ProjectDetail", backref="vehicle", cascade="all, delete-orphan"
    )

    def __init__(
        self,
        license_plate: str,
        brand: str,
        model: str,
        year: int,
        body_number: str,
        engine_number: str,
        color: str,
        problem: str,
    ):
        self.license_plate = license_plate
        self.brand = brand
        self.model = model
        self.year = year
        self.body_number = body_number
        self.engine_number = engine_number
        self.color = color
        self.problem = problem

    def __repr__(self) -> str:
        return f"Vehicle<{self.license_plate}: {self.brand} {self.model}>"


class Department(db.Model):
    """Modelo de Departamento."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(100), unique=True, nullable=False)

    # Relacion 1:N entre departamentos y detalles de proyectos (mosca con el
    # cascade)
    project_details = db.relationship(
        "ProjectDetail", backref="department", cascade="all, delete-orphan"
    )

    def __init__(self, description: str):
        self.description = description

    def __repr__(self) -> str:
        return f"Department<{self.description}>"


class MeasureUnit(db.Model):
    """ Modelo de unidades de medidas. """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dimension = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)

    def __init__(self, dimension: float, unit: str):
        self.dimension = dimension
        self.unit = unit

    def __repr__(self) -> str:
        return f"MeasureUnit<{self.dimension} {self.unit}>"


class Activity(db.Model):
    """Modelo de actividad."""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    action_plan_id = db.Column(db.Integer, db.ForeignKey("action_plan.id"), nullable=False)
    charge_person_id = db.column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    work_hours = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Float, nullable=False)

    def __init__(
            self,
            description: str,
            start_date,
            deadline,
            work_hours: int,
            cost: float
    ):
        self.description = description
        self.start_date = start_date
        self.deadline = deadline
        self.hours_number = hours_number
        self.cost = cost

    def __repr__(self) -> str:
        return f"Activity<{self.description}: {self.start_date} - {self.deadline}>"


class ActionPlan(db.Model):
    """Modelo de plan de acción."""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    action = db.Column(db.String(100), nullable=False)
 
    # Relacion 1:N entre plan de acción y actividades
    activities = db.relationship(
        "Activity", backref="action_plan", cascade="all, delete-orphan"
    )

    def __init__(self, action: str):
        self.action = action
