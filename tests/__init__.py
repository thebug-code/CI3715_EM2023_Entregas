import unittest
from selenium import webdriver
from os import environ

from SAGTMA import create_app


class BaseTestClass(unittest.TestCase):
    def setUp(self):
        # Crea la aplicación y un cliente para las pruebas
        self.app = create_app(
            test_config={
                "TESTING": True,
                "DEBUG": True,
                "APP_ENV": "testing",
                "DATABASE_NAME": "SAGTMA_test",
                "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            }
        )
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

        # Puebla la base de datos para el conjunto de tests, si es necesario
        if hasattr(self, "populate_db"):
            self.populate_db()
        
        # Inicializa el driver de Selenium, usa el webdriver especificado por
        # la variable de entorno WEBDRIVER
        webdriver_name = environ.get("WEBDRIVER")

        # Añade la opción de headless dependiendo del driver
        if webdriver_name == "Firefox":
            from selenium.webdriver.firefox.options import Options

            options = Options()
            options.add_argument("headless")
        elif webdriver_name == "Chrome":
            from selenium.webdriver.chrome.options import Options

            options = Options()
            options.add_argument("headless")
        elif webdriver_name == "Edge":
            from selenium.webdriver.edge.options import Options
            options = Options()
            options.add_argument("headless")
        else:
            raise ValueError("Unsupported webdriver, must be one of: Firefox, Chrome, Edge")

        self.driver = getattr(webdriver, webdriver_name)(options=options)

    def tearDown(self):
        # Elimina todas las tablas de la base de datos
        from SAGTMA.models import db

        db.drop_all()

        # Elimina el contexto de la aplicación
        self.ctx.pop()

        # Cierra el driver de Selenium
        self.driver.close()
        self.driver.quit()
