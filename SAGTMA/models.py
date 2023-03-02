import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Role(db.Model):
    '''Modelo de rol.'''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)
    users = db.relationship('User', backref='role')

    def __init__(self, name: str):
        self.name = name

    def __repr__(self) -> str:
        return f'Role<{self.name}>'

user_project = db.Table(
    'user_project',
    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id')),
    db.UniqueConstraint('user_id', 'project_id')
)

class User(db.Model):
    '''Modelo de usuario.'''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True)
    names = db.Column(db.String(50))
    surnames = db.Column(db.String(50))
    password = db.Column(db.String(80))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    # Relación n:n entre usuarios y proyectos
    projects = db.relationship(
        'Project',
        secondary=user_project,
        backref=db.backref('assigned_to')
    )

    # Relación 1:n entre usuarios y eventos
    events = db.relationship('Event', backref='user')

    def __init__( self, username: str, names: str, surnames: str, password: str, role: Role):
        self.username = username
        self.names = names
        self.surnames = surnames
        self.password = password
        self.role = role

    def __repr__(self) -> str:
        return f'User<{self.username}: {self.names} {self.surnames}, {self.role.name}>'

class Project(db.Model):
    '''Modelo de proyecto.'''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(200), unique=True)
    # Fecha de sql almacena la fecha 
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    def __init__(self, description: str, start_date, end_date):
        self.description = description
        self.start_date = start_date
        self.end_date = end_date

    def __repr__(self) -> str:
        return f'Project<{self.description}: {self.start_date} - {self.end_date}>'

class Event(db.Model):
    '''Modelo de evento.'''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    module = db.Column(db.String(80))
    description = db.Column(db.String(80))
    time = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now)

    def __init__(self, user: User, module: str, description: str):
        self.user = user
        self.module = module
        self.description = description\
            if len(description) <= 80\
            else f'{description[:77]}...'

    def __repr__(self) -> str:
        return f'Event<{self.user.username}: {self.module} - {self.type}>'
