from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from SAGTMA.models import Role, User, db
from SAGTMA.utils.auth import hash_password
from tests.selenium import BaseTestClass


class TestPortfolio(BaseTestClass):
    def populate_db(self):
        super().populate_db()

        stmt = db.select(Role).where(Role.name == "Gerente de Operaciones")
        (manager,) = db.session.execute(stmt).fetchone()

        # Añade un usuario Gerente de Operaciones
        admin_user = User(
            "V-48912114",
            "manager",
            "Heisenberg",
            "The Danger",
            hash_password("Manager123."),
            manager,
        )
        db.session.add(admin_user)

        db.session.commit()

    def _login_manager(self):
        self.driver.get(f"{self.base_url}/login/")

        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "username").send_keys("manager")
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("Manager123.")
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()

    def _register_project(self, description: str, start_date: str, deadline: str):
        self.driver.find_element(
            By.CSS_SELECTOR, ".btn-primary:nth-child(3) > .table-button"
        ).click()
        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "#add-project-modal .modal-header")
            )
        )

        self.driver.find_element(By.ID, "description").click()
        self.driver.find_element(By.ID, "description").send_keys(description)
        self.driver.find_element(By.ID, "start-date").click()
        self.driver.find_element(By.ID, "start-date").send_keys(start_date)
        self.driver.find_element(By.ID, "start-date").click()
        self.driver.find_element(By.ID, "deadline").click()
        self.driver.find_element(By.ID, "deadline").send_keys(deadline)

        self.driver.find_element(
            By.CSS_SELECTOR, "#add-project-modal .btn-primary"
        ).click()
        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, ".toast-body")
            )
        )

    def test_register_project_valid(self):
        """Testea la creación de proyecto válidos."""

        def _test_register_project_valid(description: str):
            self._register_project(description, "02/14/2023", "03/30/2023")
            self.assertEqual(
                self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
                "Proyecto creado exitosamente",
            )

            self.assertIn(
                description, self.driver.find_element(By.CSS_SELECTOR, ".table").text
            )

        self._login_manager()

        # Proyecto válido con descripción corta
        _test_register_project_valid("Proyec")

        # Proyecto válido con descripción larga
        _test_register_project_valid(
            "Esta es la descripción de proyecto automotriz válido más largo que"
            " puede darse según el sistema, si."
        )
