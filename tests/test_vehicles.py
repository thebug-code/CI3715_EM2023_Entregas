from tests import BaseTestClass

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from SAGTMA.models import User, Role, Client, db
from SAGTMA.utils.profiles import hash_password
from datetime import date


class TestClients(BaseTestClass):
    def populate_db(self):
        super().populate_db()

        stmt = db.select(Role).where(Role.name == "Analista de Operaciones")
        (analyst,) = db.session.execute(stmt).fetchone()

        # Añade un usuario Gerente de Operaciones y un cliente
        analyst_user = User(
            "analyst", "Bad", "Bunny", hash_password("Analyst123."), analyst
        )

        new_client = Client(
            "V-11111111",
            "Chus",
            "Chriscris",
            date(2001, 1, 1),
            "+584445555555",
            "ChuS@usb.ve",
            "Por ahi en un lugar",
        )

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
        self.driver.get(f"{self.base_url}/clients-details/1/")
        self.driver.find_element(
            By.CSS_SELECTOR, ".input-group > .btn:nth-child(3)"
        ).click()
        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "#addModal .modal-header")
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

        self.driver.find_element(By.CSS_SELECTOR, "#addModal .btn-primary").click()
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
            "puede tener, no sé ni cómo pudiera describirlo pero aja.",
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
