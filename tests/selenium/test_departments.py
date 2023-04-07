from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from tests.selenium import BaseTestClass
from SAGTMA.models import Department, db


class TestDepartments(BaseTestClass):
    def populate_db(self):
        super().populate_db()

        # Añade un departamento
        dept = Department("Eléctrica")
        dept.id = 0

        db.session.add(dept)
        db.session.commit()

    def _login_admin(self):
        self.login_user("admin", "Admin123.")
        self.driver.get(f"{self.base_url}/workshop-departments/")

    def _register_dept(self, dept: str):
        self.driver.find_element(
            By.CSS_SELECTOR, ".input-group > .btn:nth-child(3)"
        ).click()
        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "#add-dept-modal .modal-header")
            )
        )

        self.driver.find_element(By.ID, "description").send_keys(dept)

        self.driver.find_element(
            By.CSS_SELECTOR, "#add-dept-modal .btn-primary"
        ).click()
        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, ".toast-body")
            )
        )

    def _edit_dept(self, dept: str):
        self.driver.find_element(By.CSS_SELECTOR, "#edit0").click()
        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "#edit-dept-modal .modal-header")
            )
        )

        self.driver.find_element(By.ID, "edit-description").clear()
        self.driver.find_element(By.ID, "edit-description").send_keys(dept)

        self.driver.find_element(
            By.CSS_SELECTOR, "#edit-dept-modal .btn-primary"
        ).click()
        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, ".toast-body")
            )
        )

    def test_register_dept_valid(self):
        """Testea la creación de departamentos con descripción válida."""
        self._login_admin()

        self._register_dept("Electrónica")

        self.assertEqual(
            self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
            "Departamento añadido exitosamente",
        )

        self.assertEqual(
            self.driver.find_element(By.CSS_SELECTOR, ".table > tbody > tr").text,
            "0 Eléctrica",
        )

    def test_register_dept_invalid(self):
        """Testea la creación de departamentos con descripción inválida."""
        self._login_admin()

        def _test(dept: str, msg: str):
            self._register_dept(dept)

            self.assertEqual(
                self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
                msg,
            )

            self.assertNotIn(
                dept,
                self.driver.find_element(By.CSS_SELECTOR, ".table > tbody").text,
            )

        # Testea descripciones cortas y largas
        _test(
            "Hoala",
            "La descripción del departamento debe tener entre 6 y 100 caracteres.",
        )
        _test(
            "A" * 101,
            "La descripción del departamento debe tener entre 6 y 100 caracteres.",
        )

        # Testea descripcion con caracteres inválidos
        _test(
            "Electrónic@",
            "La descripción del departamento no puede contener caracteres especiales.",
        )

    def test_register_duplicate_dept(self):
        """Testea la creación de departamentos con descripción duplicada."""
        self._login_admin()

        self._register_dept("Eléctrica")

        self.assertEqual(
            self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
            "Ya existe un departamento con la misma descripción",
        )

        self.assertEqual(
            self.driver.find_element(By.CSS_SELECTOR, ".table > tbody > tr").text,
            "0 Eléctrica",
        )

    def test_edit_dept_valid(self):
        """Testea la edición de departamentos con descripción válida."""
        self._login_admin()

        self._edit_dept("Electrónica")

        self.assertEqual(
            self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
            "Departamento modificado exitosamente",
        )

        self.assertEqual(
            self.driver.find_element(By.CSS_SELECTOR, ".table > tbody > tr").text,
            "0 Electrónica",
        )

    def test_edit_dept_invalid(self):
        """Testea la edición de departamentos con descripción inválida."""
        self._login_admin()

        def _test(dept: str, msg: str):
            self._edit_dept(dept)

            self.assertEqual(
                self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
                msg,
            )

            self.assertNotIn(
                dept,
                self.driver.find_element(By.CSS_SELECTOR, ".table > tbody").text,
            )

        # Testea descripciones cortas y largas
        _test(
            "Hoala",
            "La descripción del departamento debe tener entre 6 y 100 caracteres.",
        )
        _test(
            "A" * 101,
            "La descripción del departamento debe tener entre 6 y 100 caracteres.",
        )

        # Testea descripcion con caracteres inválidos
        _test(
            "Electrónic@",
            "La descripción del departamento no puede contener caracteres especiales.",
        )

    def test_delete_dept(self):
        """Testea la eliminación de departamentos."""
        self._login_admin()

        self.driver.find_element(By.CSS_SELECTOR, "#delete0 > .table-button").click()

        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "#delete-dept-modal .modal-header")
            )
        )

        # Cancela la eliminación
        self.driver.find_element(
            By.CSS_SELECTOR, ".modal-footer:nth-child(3) > .btn"
        ).click()

        self.assertIn(
            "Eléctrica",
            self.driver.find_element(By.CSS_SELECTOR, ".table").text,
        )

        self.driver.find_element(By.CSS_SELECTOR, "#delete0 > .table-button").click()

        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "#delete-dept-modal .modal-header")
            )
        )

        self.driver.find_element(By.CSS_SELECTOR, ".btn-danger").click()

        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, ".toast-body")
            )
        )

        self.assertEqual(
            self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
            "Departamento eliminado exitosamente",
        )

        self.assertEqual(
            "No se encontraron departamentos",
            self.driver.find_element(By.CSS_SELECTOR, ".alert").text,
        )
