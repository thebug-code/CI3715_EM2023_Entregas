from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from SAGTMA.models import (
    Role,
    User,
    Project,
    Client,
    Vehicle,
    ProjectDetail,
    Department,
    db,
)
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
        self.login_user("manager", "Manager123.")
        self.driver.get(f"{self.base_url}/project-details/0/")

    def _login_analyst(self):
        self.login_user("analyst", "Analyst123.")

    def _login_admin(self):
        self.login_user("admin", "Admin123.")

    def _add_project_data(self, solution: str, cost: str, observations: str):
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

    def _edit_project_data(self, solution: str, cost: str, observations: str):
        self.driver.find_element(
            By.CSS_SELECTOR, "#edit0"
        ).click()
        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "#edit-project-detail-modal .modal-header")
            )
        )

        self.driver.find_element(By.ID, "edit-solution").clear()
        self.driver.find_element(By.ID, "edit-solution").send_keys(solution)
        self.driver.find_element(By.ID, "edit-cost").clear()
        self.driver.find_element(By.ID, "edit-cost").send_keys(cost)
        self.driver.find_element(By.ID, "edit-observations").clear()
        self.driver.find_element(By.ID, "edit-observations").send_keys(observations)

        self.driver.find_element(
            By.CSS_SELECTOR, "#edit-project-detail-form .btn-primary"
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

    def test_register_project_data_solution_invalid(self):
        """Testea la adición de datos de proyecto con solución inválida."""

        def _test(solution: str, message: str):
            self._add_project_data(solution, "0.1", "N/A")
            self.assertEqual(
                self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
                message,
            )

            self.assertNotIn(
                solution, self.driver.find_element(By.CSS_SELECTOR, ".table").text
            )

        self._login_manager()

        # Solución de longitud 2
        _test("ZZ", "La solución debe tener entre 3 y 100 caracteres")

        # Solución de longitud 101
        _test(
            "Prueba Uno" * 10 + "2", "La solución debe tener entre 3 y 100 caracteres"
        )

        # Solución con caracteres inválidos
        _test(
            "Prueba con caracteres inválidos: !@#$%^&*()_+",
            "La solución solo puede contener caracteres alfanuméricos, guiones y espacios",
        )

    def test_register_project_data_observation_invalid(self):
        """Testea la adición de datos de proyecto con observación inválida."""

        def _test(observations: str, message: str):
            self._add_project_data("Prueba", "0.1", observations)
            self.assertEqual(
                self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
                message,
            )

            self.assertNotIn(
                observations, self.driver.find_element(By.CSS_SELECTOR, ".table").text
            )

        self._login_manager()

        # Observación de longitud 2
        _test("ZZ", "Las observaciones deben tener entre 3 y 100 caracteres")

        # Observación de longitud 101
        _test(
            "Prueba Uno" * 10 + "2",
            "Las observaciones deben tener entre 3 y 100 caracteres",
        )

        # Observación con caracteres inválidos
        _test(
            "Prueba con caracteres inválidos: !@#$%^&*()_+",
            "Las observaciones solo pueden contener caracteres alfanuméricos, guiones y espacios",
        )

    def test_edit_project_data_valid(self):
        """Testea la edición de datos de proyecto de forma válida."""

        self._login_manager()

        self._edit_project_data("Prueba", "2", "N/A")
        
        self.assertEqual(
            self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
            "Detalle de proyecto editado exitosamente",
        )
        
        self.assertIn(
            "Prueba", self.driver.find_element(By.CSS_SELECTOR, ".table").text
        )

    def test_edit_project_data_invalid(self):
        """Testea la edición de datos de proyecto de forma inválida."""

        def _test(solution: str, cost: str, observations: str, message: str):
            self._edit_project_data(solution, cost, observations)
            self.assertEqual(
                self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
                message,
            )

            self.assertNotIn(
                solution, self.driver.find_element(By.CSS_SELECTOR, ".table").text
            )

        self._login_manager()

        # Solucion muy larga
        _test("a"*101, "1", "N/A", "La solución debe tener entre 3 y 100 caracteres")

        # Observacion muy larga
        _test("ZZZ", "1", "a"*101, "Las observaciones deben tener entre 3 y 100 caracteres")

        # Costo negativo
        _test("ZZZ", "-1", "N/A", "El costo debe ser mayor o igual a 0")

    def test_delete_project_data(self):
        """Testea la eliminación de datos de proyecto."""
        self._login_manager()

        self.driver.find_element(By.CSS_SELECTOR, "#delete0 > .table-button").click()

        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "#delete-project-detail-modal .modal-header")
            )
        )

        # Cancela la eliminación
        self.driver.find_element(
            By.CSS_SELECTOR, ".modal-footer:nth-child(3) > .btn"
        ).click()

        self.assertIn(
            "N/A",
            self.driver.find_element(By.CSS_SELECTOR, ".table").text,
        )

        self.driver.find_element(By.CSS_SELECTOR, "#delete0 > .table-button").click()

        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "#delete-project-detail-modal .modal-header")
            )
        )

        self.driver.find_element(By.CSS_SELECTOR, ".btn-danger").click()

        # Assert that the client was deleted
        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, ".toast-body")
            )
        )

        self.assertEqual(
            self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
            "Detalle de proyecto eliminado exitosamente",
        )

        # Assert that the client is not in the table
        self.assertEqual(
            "No se encontraron datos del proyecto",
            self.driver.find_element(By.CSS_SELECTOR, ".alert").text,
        )

    def test_delete_client_project_associated(self):
        """Testea la eliminación de un cliente que tiene un proyecto asociado."""
        self._login_manager()

        self.driver.find_element(By.CSS_SELECTOR, "#delete1 > .table-button").click()

        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "#delete-project-detail-modal .modal-header")
            )
        )

        self.driver.find_element(By.CSS_SELECTOR, ".btn-danger").click()

        # Assert that the client was deleted
        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, ".toast-body")
            )
        )

        self.assertEqual(
            self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
            "El detalle de proyecto no puede ser eliminado porque está asociado a un cliente",
        )

        self.assertIn(
            "Prueba",
            self.driver.find_element(By.CSS_SELECTOR, ".table").text,
        )