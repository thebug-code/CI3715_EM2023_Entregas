import unittest

import SAGTMA
from SAGTMA.models import Role, User, Event, db
from SAGTMA.utils.profiles import hash_password


class BaseTestClass(unittest.TestCase):
    app = SAGTMA.test_app()

    def setUp(self):
        # Puebla la base de datos para el conjunto de tests, si es necesario
        # Crea la aplicación y un cliente para las pruebas
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

    def login_user(self, username: str, password: str):
        """Inicia sesión con un usuario"""
        return self.client.post(
            "/login/",
            data={"username": username, "password": password},
            follow_redirects=True,
        )

    def _login_manager(self):
        return self.login_user("manager", "Manager123.")

    def _login_admin(self):
        return self.login_user("admin", "Admin123.")

    def _login_analyst(self):
        return self.login_user("analyst", "Analyst123.")

    def _test_logger_works(self):
        stmt = db.select(Event)
        self.assertIsNotNone(
            db.session.execute(stmt).first()
        )

    def tearDown(self):
        # Sale el contexto de la aplicación
        self.ctx.pop()
