from tests import BaseTestClass

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from SAGTMA.models import User, Role, db
from SAGTMA.utils.profiles import hash_password


class TestClients(BaseTestClass):
    def populate_db(self):
        super().populate_db()

        stmt = db.select(Role).where(Role.name == "Analista de Operaciones")
        (analyst,) = db.session.execute(stmt).fetchone()

        # Añade un usuario Gerente de Operaciones
        analyst_user = User(
            "analyst", "Bad", "Bunny", hash_password("Analyst123."), analyst
        )
        db.session.add(analyst_user)

        db.session.commit()

    def _login_analyst(self):
        self.driver.get("http://localhost:5001/login/")

        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "username").send_keys("analyst")
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("Analyst123.")
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()

    def _register_client(
        self,
        id_number: str,
        names: str,
        surnames: str,
        birthdate: str,
        phone: str,
        email: str,
        address: str,
    ):
        self.driver.find_element(
            By.CSS_SELECTOR, ".input-group > .btn:nth-child(3)"
        ).click()
        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "#addModal .modal-header")
            )
        )

        self.driver.find_element(By.ID, "id-number").click()
        self.driver.find_element(By.ID, "id-number").send_keys(id_number)
        self.driver.find_element(By.ID, "names").click()
        self.driver.find_element(By.ID, "names").send_keys(names)
        self.driver.find_element(By.ID, "surnames").click()
        self.driver.find_element(By.ID, "surnames").send_keys(surnames)
        self.driver.find_element(By.ID, "birthdate").click()
        self.driver.find_element(By.ID, "birthdate").send_keys(birthdate)
        self.driver.find_element(By.ID, "phone-number").click()
        self.driver.find_element(By.ID, "phone-number").send_keys(phone)
        self.driver.find_element(By.ID, "email").click()
        self.driver.find_element(By.ID, "email").send_keys(email)
        self.driver.find_element(By.ID, "address").click()
        self.driver.find_element(By.ID, "address").send_keys(address)

        self.driver.find_element(By.CSS_SELECTOR, "#addModal .btn-primary").click()
        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, ".toast-body")
            )
        )


    def test_register_client_valid(self):
        """Testea la creación de clientes válidos."""

        def _test_register_client_valid(
            id_number: str,
            names: str,
            surnames: str,
            birthdate: str,
            phone: str,
            email: str,
            address: str,
        ):
            self._register_client(
                id_number, names, surnames, birthdate, phone, email, address
            )
            self.assertEqual(
                self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
                "Cliente añadido exitosamente",
            )

            self.assertIn(
                email, self.driver.find_element(By.CSS_SELECTOR, ".table").text
            )

        self._login_analyst()

        # Cliente válido condiciones normales
        _test_register_client_valid(
            "V-12345678",
            "Alan",
            "Turing",
            "06/23/1912",
            "04123456789",
            "alanturing@usb.ve",
            "Chacaito",
        )
        
        # Cédula distinta
        _test_register_client_valid(
            "j-1234567",
            "Alan",
            "Turing",
            "06/23/1912",
            "04123456789",
            "alanturing@usb.ve",
            "Chacaito",
        )
        
        # Nombres y apellidos corto/largo
        _test_register_client_valid(
            "V-12345678",
            "Ka",
            "Bolivar Palacios y Blanco de la Santisima Trinid",
            "06/23/1912",
            "04123456789",
            "uncorreo@usb.ve",
            "Charallave",
        )

