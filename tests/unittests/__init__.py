import unittest

import SAGTMA
from SAGTMA.models import Role, User, db
from SAGTMA.utils.profiles import hash_password


class BaseTestClass(unittest.TestCase):
    def setUp(self):
        # Puebla la base de datos para el conjunto de tests, si es necesario
        # Crea la aplicación y un cliente para las pruebas
        self.app = SAGTMA.test_app()
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

        db.drop_all()
        db.create_all()
        self.populate_db()

    def populate_db(self):
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
            "V-11457851",
            "admin",
            "Juanito",
            "Alimaña",
            hash_password("Admin123."),
            roles[1],
        )
        db.session.add(admin_user)

        db.session.commit()

    def tearDown(self):
        # Sale el contexto de la aplicación
        self.ctx.pop()
