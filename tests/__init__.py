import unittest
from os import environ

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


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

        options.add_argument('-headless')
        self.driver = getattr(webdriver, webdriver_name)(options=options)
        self.base_url = "http://localhost:5001"

    def _login(self, username: str, password: str):
        '''Mét'''
        self.driver.get(f"{self.base_url}/")
        username_form = self.driver.find_element(By.ID, "username")
        password_form = self.driver.find_element(By.ID, "password")
        submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")

        username_form.send_keys(username)
        password_form.send_keys(password)
        submit_button.click()

    def _logout(self):
        self.driver.get(f"{self.base_url}/")
        logout_button = self.driver.find_element(By.XPATH, "//a[@class='nav-link link']")
        logout_button.click()

    def tearDown(self):
        # Cierra el driver de Selenium
        self.driver.close()
        self.driver.quit()
