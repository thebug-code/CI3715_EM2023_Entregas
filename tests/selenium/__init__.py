import unittest
from os import environ

from selenium import webdriver
import SAGTMA
from SAGTMA.models import Role, User, db
from SAGTMA.utils.auth import hash_password


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

        # Inicializa el driver de Selenium, usa el webdriver especificado por
        # la variable de entorno WEBDRIVER
        webdriver_name = environ.get("WEBDRIVER")
        headless = bool(environ.get("HEADLESS"))

        # Añade la opción de headless dependiendo del driver
        if webdriver_name == "Firefox":
            from selenium.webdriver.firefox.options import Options

            options = Options()
        elif webdriver_name == "Chrome":
            from selenium.webdriver.chrome.options import Options

            options = Options()
        elif webdriver_name == "Edge":
            from selenium.webdriver.edge.options import Options

            options = Options()
        else:
            raise ValueError(
                "Unsupported webdriver, must be one of: Firefox, Chrome, Edge"
            )

        if headless:
            options.add_argument("-headless")
        self.driver = getattr(webdriver, webdriver_name)(options=options)
        self.base_url = "http://localhost:5001"

    def populate_db(self):
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
            "V-48912714",
            "admin",
            "Juanito",
            "Alimaña",
            hash_password("Admin123."),
            admin,
        )
        db.session.add(admin_user)

        db.session.commit()

    def tearDown(self):
        # Cierra el driver de Selenium
        self.driver.close()
        self.driver.quit()
        self.ctx.pop()
