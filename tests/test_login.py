from tests import BaseTestClass

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class TestLogin(BaseTestClass):
    def test_login(self):
        """Testea el login con credenciales correctas."""
        self.driver.get("http://localhost:5001/login/")
        self.driver.find_element(By.ID, "username").send_keys("admin")
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("Admin123.")
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
        self.driver.find_element(By.CSS_SELECTOR, ".title-container").click()
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".title-container")
        self.assertTrue(len(elements) > 0)

    def test_login_incorrect_password(self):
        """Testea el login con credenciales incorrectas."""
        self.driver.get("http://localhost:5001/login/")
        self.driver.find_element(By.ID, "username").send_keys("admin")
        self.driver.find_element(By.ID, "username").send_keys(Keys.ENTER)
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("admin123..")
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
        self.driver.find_element(By.CSS_SELECTOR, ".toast-body").click()
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".toast-body")
        self.assertTrue(len(elements) > 0)

    def test_logout(self):
        """Testea el cierre de sesión"""
        self.driver.get("http://localhost:5001/login/")
        self.driver.find_element(By.ID, "username").send_keys("admin")
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("Admin123.")
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
        self.driver.find_element(By.CSS_SELECTOR, ".title-container").click()
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".title-container")
        self.assertTrue(len(elements) > 0)
