import unittest
from selenium import webdriver
from os import environ


class BaseTestClass(unittest.TestCase):
    def setUp(self):
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
            raise ValueError(
                "Unsupported webdriver, must be one of: Firefox, Chrome, Edge"
            )

        self.driver = getattr(webdriver, webdriver_name)(options=options)
        self.base_url = "http://localhost:5001"

    def tearDown(self):
        # Cierra el driver de Selenium
        self.driver.close()
        self.driver.quit()
