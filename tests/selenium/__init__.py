import unittest
from os import environ

from selenium.webdriver.common.by import By
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

    def login_user(self, username: str, password: str):
        self.driver.get(f"{self.base_url}/login/")

        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()

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
        # Cierra el driver de Selenium
        self.driver.close()
        self.driver.quit()
        self.ctx.pop()
