from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

import SAGTMA.utils.measurement_units as mu
from SAGTMA.models import MeasureUnit, db
from tests.selenium import BaseTestClass


class MeasurementUnitsTests(BaseTestClass):
    def populate_db(self):
        super().populate_db()

        # Añade una unidad de medida
        unit = MeasureUnit(6, "Centímetros")
        unit.id = 0

        db.session.add(unit)
        db.session.commit()

    def _login_admin(self):
        self.login_user("admin", "Admin123.")
        self.driver.get(f"{self.base_url}/measurement-units/")

    def _register_unit(self, dimension: str, unit: str):
        self.driver.find_element(
            By.CSS_SELECTOR, ".input-group > .btn:nth-child(3)"
        ).click()

        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "#add-measure-unit-modal .modal-header")
            )
        )

        self.driver.find_element(By.ID, "add-dimension").send_keys(dimension)
        self.driver.find_element(By.ID, "add-unit").send_keys(unit)

        self.driver.find_element(
            By.CSS_SELECTOR, "#add-measure-unit-modal .btn-primary"
        ).click()

        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, ".toast-body")
            )
        )

    def _edit_unit(self, dimension: str, unit: str):
        self.driver.find_element(By.CSS_SELECTOR, "#edit0").click()

        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "#edit-measure-unit-modal .modal-header")
            )
        )

        self.driver.find_element(By.ID, "edit-dimension").clear()
        self.driver.find_element(By.ID, "edit-dimension").send_keys(dimension)
        self.driver.find_element(By.ID, "edit-unit").clear()
        self.driver.find_element(By.ID, "edit-unit").send_keys(unit)

        self.driver.find_element(
            By.CSS_SELECTOR, "#edit-measure-unit-modal .btn-primary"
        ).click()

        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, ".toast-body")
            )
        )

    def test_register_unit_valid(self):
        """Testea el registro de una unidad de medida válida"""
        self._login_admin()

        # Datos de unidad válidos
        def _test(dimension: str, unit: str):
            self._register_unit(dimension, unit)

            self.assertEqual(
                self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
                "Unidad de medida añadida exitosamente",
            )
            self.assertIn(unit, self.driver.page_source)

        _test("10", "Centímetros")
        _test("0.01", "Kilómetros")
        _test("999", "Unidades Astronómicas")
        _test("10", "s")

    def test_register_unit_invalid(self):
        """Testea el registro de una unidad de medida inválida"""

        def _test(dimension: str, unit: str, error_message: str):
            self._register_unit(dimension, unit)

            self.assertEqual(
                self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
                error_message,
            )
            self.assertNotIn(unit, self.driver.page_source)

        self._login_admin()

        # Datos de unidad inválidos
        _test("0", "Centimetros", "La dimensión debe ser un número positivo.")
        _test("10", "cm2", "La unidad solo puede contener caracteres alfabéticos.")

    def test_edit_unit_valid(self):
        """Testea la edición de una unidad de medida válida"""

        def _test(dimension: str, unit: str):
            self._edit_unit(dimension, unit)

            self.assertEqual(
                self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
                "Unidad de medida modificada exitosamente",
            )
            self.assertIn(unit, self.driver.page_source)

        self._login_admin()

        # Datos de unidad válidos
        _test("10", "Centímetros")
        _test("0.01", "Kilómetros")
        _test("999", "Unidades Astronómicas")
        _test("10", "s")

    def test_edit_unit_invalid(self):
        """Testea la edición de una unidad de medida inválida"""

        def _test(dimension: str, unit: str, error_message: str):
            self._edit_unit(dimension, unit)

            self.assertEqual(
                self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
                error_message,
            )
            self.assertNotIn(unit, self.driver.page_source)
            self.assertIn("6.0", self.driver.page_source)
            self.assertIn("Centímetros", self.driver.page_source)

        self._login_admin()

        # Datos de unidad inválidos
        _test("0", "Centimetros", "La dimensión debe ser un número positivo.")
        _test("10", "cm2", "La unidad solo puede contener caracteres alfabéticos.")

    def test_delete_unit(self):
        """Testea la eliminación de una unidad de medida de forma válida."""
        self._login_admin()

        self.driver.find_element(By.CSS_SELECTOR, "#delete0 > .table-button").click()

        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "#delete-measure-unit-modal .modal-header")
            )
        )

        # Cancela la eliminación
        self.driver.find_element(
            By.CSS_SELECTOR, ".modal-content > .modal-footer > .btn"
        ).click()

        self.assertIn(
            "Centímetros",
            self.driver.find_element(By.CSS_SELECTOR, ".table").text,
        )

        self.driver.find_element(By.CSS_SELECTOR, "#delete0 > .table-button").click()

        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "#delete-measure-unit-modal .modal-header")
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
            "Unidad de medida eliminada exitosamente",
        )

        self.assertEqual(
            "No se encontraron unidades de medida",
            self.driver.find_element(By.CSS_SELECTOR, ".alert").text,
        )
