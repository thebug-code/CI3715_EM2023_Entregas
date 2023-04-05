from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from SAGTMA.models import Role, User, Project, Client, Vehicle, ProjectDetail, Department, db
from SAGTMA.utils.auth import hash_password
from tests.selenium import BaseTestClass
from datetime import date

class TestProjectDetails(BaseTestClass):
    def populate_db(self):
        super().populate_db()

        stmt = db.select(Role).where(Role.name == "Gerente de Operaciones")
        (manager,) = db.session.execute(stmt).fetchone()

        # Añade un usuario Gerente de Operaciones
        manager_user = User(
            "V-1000000",
            "manager",
            "Bad",
            "Bunny",
            hash_password("Manager123."),
            manager,
        )

        # Añade un proyecto
        project = Project(f"Proyecto Automotriz 1", date(2021, 4, 1), date(2023, 4, 1))
        project.id = 0

        # Añade un cliente y un vehículo
        client = Client(
            "V-11122345",
            "Cliente",
            "De Prueba",
            date(1974, 3, 16),
            "+584254635122",
            "testclient@locatel.com.ve",
            "Wock to Poland",
        )
        client.id = 0

        car = Vehicle(
            "ABC-123",
            "Toyota",
            "Corolla",
            2018,
            "A123456789",
            "987654321B",
            "Negro",
            "Clutch no funciona",
        )
        car.id = 0
        client.vehicles.append(car)

        # Añade un departamento
        dept = Department("Mecánica")
        dept.id = 0

        # Añade un detalle de proyecto
        detail = ProjectDetail(0, 0, 0, 1, "Prueba", 0.1, "N/A")
        detail.id = 0

        db.session.add_all([manager_user, project, client, dept, detail])
        db.session.commit()

    def _login_manager(self):
        self.driver.get(f"{self.base_url}/login/")

        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "username").send_keys("manager")
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("Manager123.")
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
        self.driver.get(f"{self.base_url}/project-details/0/")

    def _add_project_data(self, solution, cost, observations):
        self.driver.find_element(
            By.CSS_SELECTOR, ".btn-primary:nth-child(3) > .table-button"
        ).click()
        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "#add-project-detail-modal .modal-header")
            )
        )

        self.driver.find_element(By.ID, "add-solution").click()
        self.driver.find_element(By.ID, "add-solution").send_keys(solution)
        self.driver.find_element(By.ID, "add-cost").click()
        self.driver.find_element(By.ID, "add-cost").send_keys(cost)
        self.driver.find_element(By.ID, "add-observation").click()
        self.driver.find_element(By.ID, "add-observation").send_keys(observations)

        self.driver.find_element(
            By.CSS_SELECTOR, "#add-project-detail-form .btn-primary"
        ).click()
        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, ".toast-body")
            )
        )

    def test_register_project_data_valid(self):
        """Testea la adición de datos de proyecto válidos."""

        self._login_manager()

        self._add_project_data("Prueba", "0.1", "N/A")
        self.assertEqual(
            self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
            "Detalle de proyecto registrado exitosamente",
        )

        self.assertIn(
            "Prueba", self.driver.find_element(By.CSS_SELECTOR, ".table").text
        )
