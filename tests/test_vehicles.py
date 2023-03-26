from tests import BaseTestClass

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from SAGTMA.models import User, Role, Client, Vehicle, db
from SAGTMA.utils.auth import hash_password
import datetime


class TestVehicles(BaseTestClass):
    def populate_db(self):
        super().populate_db()

        stmt = db.select(Role).where(Role.name == "Analista de Operaciones")
        (analyst,) = db.session.execute(stmt).fetchone()

        # Añade un usuario Gerente de Operaciones y un cliente
        analyst_user = User(
            "V-58912714",
            "analyst",
            "Bad",
            "Bunny",
            hash_password("Analyst123."),
            analyst,
        )

        new_client = Client(
            "V-11111111",
            "Chus",
            "Chriscris",
            datetime.date(2001, 1, 1),
            "+584445555555",
            "ChuS@usb.ve",
            "Por ahi en un lugar",
        )

        new_car = Vehicle(
            "AAA-111",
            "Toyota",
            "Corolla",
            2010,
            "123456789A",
            "A987654321",
            "Gris",
            "Caja dañada (como siempre)",
        )
        new_car.id = 0

        new_client.vehicles.append(new_car)

        db.session.add_all([analyst_user, new_client])

        db.session.commit()

    def _login_analyst(self):
        self.driver.get(f"{self.base_url}/login/")

        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "username").send_keys("analyst")
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("Analyst123.")
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
        self.driver.get(f"{self.base_url}/client-details/1/")

    def _register_vehicle(
        self,
        license_plate: str,
        brand: str,
        model: str,
        year: str,
        body_number: str,
        engine_number: str,
        problem: str,
    ):
        self.driver.find_element(
            By.CSS_SELECTOR, ".input-group > .btn:nth-child(3)"
        ).click()
        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "#add-vehicle-modal .modal-header")
            )
        )

        self.driver.find_element(By.ID, "license-plate").click()
        self.driver.find_element(By.ID, "license-plate").send_keys(license_plate)
        self.driver.find_element(By.ID, "brand").click()
        self.driver.find_element(By.ID, "brand").send_keys(brand)
        self.driver.find_element(By.ID, "model").click()
        self.driver.find_element(By.ID, "model").send_keys(model)
        self.driver.find_element(By.ID, "year").click()
        self.driver.find_element(By.ID, "year").send_keys(year)
        self.driver.find_element(By.ID, "body-number").click()
        self.driver.find_element(By.ID, "body-number").send_keys(body_number)
        self.driver.find_element(By.ID, "engine-number").click()
        self.driver.find_element(By.ID, "engine-number").send_keys(engine_number)
        self.driver.find_element(By.ID, "problem").click()
        self.driver.find_element(By.ID, "problem").send_keys(problem)

        self.driver.find_element(
            By.CSS_SELECTOR, "#add-vehicle-modal .btn-primary"
        ).click()
        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, ".toast-body")
            )
        )

    def _edit_vehicle(
        self,
        license_plate: str,
        brand: str,
        model: str,
        year: str,
        body_number: str,
        engine_number: str,
        problem: str,
    ):
        self.driver.find_element(By.CSS_SELECTOR, "#edit0 > .table-button").click()
        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "#edit-vehicle-modal .modal-header")
            )
        )

        self.driver.find_element(By.ID, "edit-license-plate").click()
        self.driver.find_element(By.ID, "edit-license-plate").clear()
        self.driver.find_element(By.ID, "edit-license-plate").send_keys(license_plate)
        self.driver.find_element(By.ID, "edit-brand").click()
        self.driver.find_element(By.ID, "edit-brand").clear()
        self.driver.find_element(By.ID, "edit-brand").send_keys(brand)
        self.driver.find_element(By.ID, "edit-model").click()
        self.driver.find_element(By.ID, "edit-model").clear()
        self.driver.find_element(By.ID, "edit-model").send_keys(model)
        self.driver.find_element(By.ID, "edit-year").click()
        self.driver.find_element(By.ID, "edit-year").clear()
        self.driver.find_element(By.ID, "edit-year").send_keys(year)
        self.driver.find_element(By.ID, "edit-body-number").click()
        self.driver.find_element(By.ID, "edit-body-number").clear()
        self.driver.find_element(By.ID, "edit-body-number").send_keys(body_number)
        self.driver.find_element(By.ID, "edit-engine-number").click()
        self.driver.find_element(By.ID, "edit-engine-number").clear()
        self.driver.find_element(By.ID, "edit-engine-number").send_keys(engine_number)
        self.driver.find_element(By.ID, "edit-problem").click()
        self.driver.find_element(By.ID, "edit-problem").clear()
        self.driver.find_element(By.ID, "edit-problem").send_keys(problem)

        self.driver.find_element(
            By.CSS_SELECTOR, "#edit-vehicle-modal .btn-primary"
        ).click()
        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, ".toast-body")
            )
        )

    def test_register_vehicle_valid(self):
        """Testea la creación de vehículos válidos."""

        def _test_register_vehicle_valid(
            license_plate: str,
            brand: str,
            model: str,
            year: str,
            body_number: str,
            engine_number: str,
            problem: str,
        ):
            self._register_vehicle(
                license_plate, brand, model, year, body_number, engine_number, problem
            )
            self.assertEqual(
                self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
                "Vehículo añadido exitosamente",
            )

            self.assertIn(
                license_plate, self.driver.find_element(By.CSS_SELECTOR, ".table").text
            )

        self._login_analyst()

        # Vehículo válido condiciones normales
        _test_register_vehicle_valid(
            "NRR-16D",
            "Chevrolet",
            "Aveo",
            "1978",
            "ABCDEFG01234567",
            "1234567ABCDEFG",
            "Se le dañó la caja!",
        )

        # Longitud de placa al borde
        _test_register_vehicle_valid(
            "NR216",
            "Chevrolet",
            "Aveo",
            "2023",
            "ABCDEFG01234567",
            "1234567ABCDEFG",
            "Se le dañó la caja!",
        )

        _test_register_vehicle_valid(
            "NR2160 DAA",
            "Chevrolet",
            "Aveo",
            "2023",
            "ABCDEFG01234567",
            "1234567ABCDEFG",
            "Se le dañó la caja!",
        )

        # Años al borde
        _test_register_vehicle_valid(
            "NR1-16D",
            "Chevrolet",
            "Aveo",
            "1900",
            "ABCDEFG01234567",
            "1234567ABCDEFG",
            "Se le dañó la caja!",
        )

        _test_register_vehicle_valid(
            "NR2-16D",
            "Chevrolet",
            "Aveo",
            "2023",
            "ABCDEFG01234567",
            "1234567ABCDEFG",
            "Se le dañó la caja!",
        )

        # Seriales corto y largo
        _test_register_vehicle_valid(
            "NR2-16A",
            "Chevrolet",
            "Aveo",
            "2023",
            "ABCDE",
            "1234567ABCDEFG123456",
            "Se le dañó la caja!",
        )

        # Problemas largo
        _test_register_vehicle_valid(
            "NR3-16D",
            "Chevrolet",
            "Aveo",
            "2023",
            "ABCDE",
            "1234567ABCDEFG123456",
            "El problema más largo que vas a poder imaginarte que un carro "
            "puede tener, no sé ni cómo pudiera describirlo pero aja...",
        )

    def test_register_vehicle_invalid_license_plate(self):
        """Testea la creación de vehículos con placas inválidas."""

        def _test_register_vehicle_invalid_license_plate(
            license_plate: str, message: str
        ):
            self._register_vehicle(
                license_plate,
                "Tesla",
                "Model S",
                "2023",
                "ABCDEF1234",
                "1234ABCDEF",
                "No sirve el cargador",
            )
            self.assertEqual(
                self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
                message,
            )

        self._login_analyst()

        # Placa muy corta
        _test_register_vehicle_invalid_license_plate(
            "NR16", "La placa debe tener entre 5 y 10 caracteres"
        )

        # Placa muy larga
        _test_register_vehicle_invalid_license_plate(
            "NR2160DAAC1", "La placa debe tener entre 5 y 10 caracteres"
        )

        # Placa con dos guiones o espacios juntos
        _test_register_vehicle_invalid_license_plate(
            "NR--16D", "La placa no puede contener espacios/guiones consecutivos"
        )

        _test_register_vehicle_invalid_license_plate(
            "NR  16D", "La placa no puede contener espacios/guiones consecutivos"
        )

        # Placa comienza con guión
        _test_register_vehicle_invalid_license_plate(
            "-NR116D", "La placa debe comenzar con un caracter alfanumérico"
        )

    def test_vehicle_year_invalid(self):
        """Testea la creación de vehículos con años inválidos."""

        def _test_vehicle_year_invalid(year: str):
            self._register_vehicle(
                "NRR-16D",
                "Chevrolet",
                "Aveo",
                year,
                "ABCDEFG01234567",
                "1234567ABCDEFG",
                "Se le dañó la caja!",
            )
            self.assertEqual(
                self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
                "El año debe ser un número entero entre 1900 y el año posterior al actual",
            )

        self._login_analyst()

        # Año anterior a 1900
        _test_vehicle_year_invalid("1899")

        # Año posterior al actual + 1
        actual_year = datetime.datetime.now().year
        _test_vehicle_year_invalid(str(actual_year + 2))

    def test_vehicle_serial_invalid(self):
        """Testea la creación de vehículos con seriales inválidos."""

        def _test_vehicle_serial_invalid(serial: str, message: str):
            self._register_vehicle(
                "NRR-16D",
                "Chevrolet",
                "Aveo",
                "1978",
                serial,
                "1234567ABCDEFG",
                "Se le dañó la caja!",
            )
            self.assertEqual(
                self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
                message,
            )

        self._login_analyst()

        # Serial muy corto
        _test_vehicle_serial_invalid(
            "AB12", "El número de serie debe tener entre 5 y 20 caracteres"
        )

        # Serial muy largo
        _test_vehicle_serial_invalid(
            "ABCDEFG0-1234567-8F-A",
            "El número de serie debe tener entre 5 y 20 caracteres",
        )

        # Serial con caracteres inválidos
        _test_vehicle_serial_invalid(
            "ABCDEFG0126@7",
            "El número de serie solo puede contener caracteres alfanuméricos y guiones",
        )

        # Serial con dos guiones consecutivos
        _test_vehicle_serial_invalid(
            "A--B12", "El número de serie no puede contener guiones consecutivos"
        )

        # Serial comienza o termina con guión
        _test_vehicle_serial_invalid(
            "-AB12", "El número de serie no puede comenzar ni terminar con un guión"
        )
        _test_vehicle_serial_invalid(
            "AB12-", "El número de serie no puede comenzar ni terminar con un guión"
        )

    def test_vehicle_problem_invalid(self):
        """Testea la creación de vehículos con problemas inválidos."""

        def _test_vehicle_problem_invalid(problem: str):
            self._register_vehicle(
                "NRR-16D",
                "Chevrolet",
                "Aveo",
                "1978",
                "ABCDEFG01234567",
                "1234567ABCDEFG",
                problem,
            )
            self.assertEqual(
                self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
                "La descripción del problema no puede tener más de 120 caracteres",
            )

        self._login_analyst()

        # Problema muy largo
        _test_vehicle_problem_invalid(
            "El problema más largo que vas a poder imaginarte que un carrot "
            "puede tener, no sé ni cómo pudiera describirlo pero aja..."
        )

    def test_vehicle_already_exists(self):
        """Testea la creación de vehículos que ya existen."""

        self._login_analyst()

        self._register_vehicle(
            "NRR-16D",
            "Chevrolet",
            "Aveo",
            "1978",
            "ABCDEFG01234567",
            "1234567ABCDEFG",
            "Se le dañó la caja!",
        )

        self._register_vehicle(
            "NRR-16D",
            "Chevrolet",
            "Aveo",
            "1978",
            "ABCDEFG01234567",
            "1234567ABCDEFG",
            "Se le dañó la caja!",
        )

        self.assertEqual(
            self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
            "El vehículo indicado ya existe",
        )

    def test_delete_vehicle(self):
        """Testea la eliminación de vehículos."""

        self._login_analyst()

        self._register_vehicle(
            "NRR-16D",
            "Chevrolet",
            "Aveo",
            "1978",
            "ABCDEFG01234567",
            "1234567ABCDEFG",
            "Se le dañó la caja!",
        )

    def test_delete_vehicle(self):
        """Testea la eliminación de vehículos."""

        self._login_analyst()

        self
        self.driver.find_element(By.CSS_SELECTOR, "#delete0 > .table-button").click()

        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "#delete-vehicle-modal .modal-header")
            )
        )

        # Cancela la eliminación
        self.driver.find_element(
            By.CSS_SELECTOR, ".modal-footer:nth-child(3) > .btn"
        ).click()

        self.assertIn(
            "AAA-111",
            self.driver.find_element(By.CSS_SELECTOR, ".table").text,
        )

        self.driver.find_element(By.CSS_SELECTOR, "#delete0 > .table-button").click()

        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "#delete-vehicle-modal .modal-header")
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
            "Vehículo eliminado exitosamente",
        )

        # Assert that the client is not in the table
        self.assertEqual(
            "No se encontraron vehículos",
            self.driver.find_element(By.CSS_SELECTOR, ".alert").text,
        )

    def test_edit_vehicle_valid(self):
        """Testea la creación de vehículos válidos."""

        def _test_edit_edit_valid(
            license_plate: str,
            brand: str,
            model: str,
            year: str,
            body_number: str,
            engine_number: str,
            problem: str,
        ):
            self._edit_vehicle(
                license_plate, brand, model, year, body_number, engine_number, problem
            )
            self.assertEqual(
                self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
                "Vehículo modificado exitosamente",
            )

            self.assertIn(
                license_plate, self.driver.find_element(By.CSS_SELECTOR, ".table").text
            )

        self._login_analyst()

        # Vehículo válido condiciones normales
        _test_edit_edit_valid(
            "NRR-16D",
            "Chevrolet",
            "Aveo",
            "1978",
            "ABCDEFG01234567",
            "1234567ABCDEFG",
            "Se le dañó la caja!",
        )

        # Longitud de placa al borde
        _test_edit_edit_valid(
            "NR216",
            "Chevrolet",
            "Aveo",
            "2023",
            "ABCDEFG01234567",
            "1234567ABCDEFG",
            "Se le dañó la caja!",
        )

        _test_edit_edit_valid(
            "NR2160 DAA",
            "Chevrolet",
            "Aveo",
            "2023",
            "ABCDEFG01234567",
            "1234567ABCDEFG",
            "Se le dañó la caja!",
        )

        # Años al borde
        _test_edit_edit_valid(
            "NR1-16D",
            "Chevrolet",
            "Aveo",
            "1900",
            "ABCDEFG01234567",
            "1234567ABCDEFG",
            "Se le dañó la caja!",
        )

        _test_edit_edit_valid(
            "NR2-16D",
            "Chevrolet",
            "Aveo",
            "2023",
            "ABCDEFG01234567",
            "1234567ABCDEFG",
            "Se le dañó la caja!",
        )

        # Seriales corto y largo
        _test_edit_edit_valid(
            "NR2-16A",
            "Chevrolet",
            "Aveo",
            "2023",
            "ABCDE",
            "1234567ABCDEFG123456",
            "Se le dañó la caja!",
        )

        # Problemas largo
        _test_edit_edit_valid(
            "NR3-16D",
            "Chevrolet",
            "Aveo",
            "2023",
            "ABCDE",
            "1234567ABCDEFG123456",
            "El problema más largo que vas a poder imaginarte que un carro "
            "puede tener, no sé ni cómo pudiera describirlo pero aja...",
        )
