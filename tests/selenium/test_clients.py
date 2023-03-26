from tests.selenium import BaseTestClass

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from SAGTMA.models import User, Role, Client, Vehicle, db
from SAGTMA.utils.auth import hash_password
import datetime


class TestClients(BaseTestClass):
    def populate_db(self):
        super().populate_db()

        stmt = db.select(Role).where(Role.name == "Analista de Operaciones")
        (analyst,) = db.session.execute(stmt).fetchone()

        # Añade un usuario Gerente de Operaciones
        analyst_user = User(
            "V-48112714",
            "analyst",
            "Bad",
            "Bunny",
            hash_password("Analyst123."),
            analyst,
        )

        # Añade un cliente y un vehículo
        client = Client(
            "V-11122345",
            "Cliente",
            "De Prueba",
            datetime.date(1974, 3, 16),
            "+584254635122",
            "testclient@locatel.com.ve",
            "Wock to Poland",
        )

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
        client.vehicles.append(car)
        client.id = 0

        db.session.add_all([analyst_user, client])
        db.session.commit()

    def _login_analyst(self):
        self.driver.get(f"{self.base_url}/login/")

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
                (By.CSS_SELECTOR, "#add-client-modal .modal-header")
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

        self.driver.find_element(
            By.CSS_SELECTOR, "#add-client-modal .btn-primary"
        ).click()
        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, ".toast-body")
            )
        )

    def _edit_client(
        self,
        id_number: str,
        names: str,
        surnames: str,
        birthdate: str,
        phone: str,
        email: str,
        address: str,
    ):
        self.driver.find_element(By.CSS_SELECTOR, "#edit0 > .table-button").click()
        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "#edit-client-modal .modal-header")
            )
        )

        self.driver.find_element(By.ID, "edit-id-number").click()
        self.driver.find_element(By.ID, "edit-id-number").clear()
        self.driver.find_element(By.ID, "edit-id-number").send_keys(id_number)
        self.driver.find_element(By.ID, "edit-names").click()
        self.driver.find_element(By.ID, "edit-names").clear()
        self.driver.find_element(By.ID, "edit-names").send_keys(names)
        self.driver.find_element(By.ID, "edit-surnames").click()
        self.driver.find_element(By.ID, "edit-surnames").clear()
        self.driver.find_element(By.ID, "edit-surnames").send_keys(surnames)
        self.driver.find_element(By.ID, "edit-birthdate").click()
        self.driver.find_element(By.ID, "edit-birthdate").clear()
        self.driver.find_element(By.ID, "edit-birthdate").send_keys(birthdate)
        self.driver.find_element(By.ID, "edit-phone-number").click()
        self.driver.find_element(By.ID, "edit-phone-number").clear()
        self.driver.find_element(By.ID, "edit-phone-number").send_keys(phone)
        self.driver.find_element(By.ID, "edit-email").click()
        self.driver.find_element(By.ID, "edit-email").clear()
        self.driver.find_element(By.ID, "edit-email").send_keys(email)
        self.driver.find_element(By.ID, "edit-address").click()
        self.driver.find_element(By.ID, "edit-address").clear()
        self.driver.find_element(By.ID, "edit-address").send_keys(address)

        self.driver.find_element(
            By.CSS_SELECTOR, "#edit-client-modal .btn-primary"
        ).click()
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
            "06/23/2000",
            "04123456789",
            "alanturing@usb.ve",
            "Chacaito",
        )

        # Cédula distinta
        _test_register_client_valid(
            "j-1234567",
            "Alan",
            "Turing",
            "06/23/2000",
            "04123456789",
            "alanturing@usb.ve",
            "Chacaito",
        )

        # Nombres y apellidos corto/largo
        _test_register_client_valid(
            "V-92345678",
            "Ka",
            "Bolivar Palacios y Blanco de la Santisima Trinid",
            "06/23/2000",
            "04123456789",
            "uncorreo@usb.ve",
            "Charallave",
        )

        # Fecha de nacimiento al límite
        eighteen_years_ago = datetime.date.today() - datetime.timedelta(days=19 * 365)
        one_hundred_years_ago = datetime.date.today() - datetime.timedelta(
            days=99 * 365
        )
        _test_register_client_valid(
            "V-1234678",
            "Chavez",
            "Maduro",
            eighteen_years_ago.strftime("%m/%d/%Y"),
            "0412 345. 6789",
            "chav@ez.co",
            "San Antonio de los Altos",
        )

        _test_register_client_valid(
            "V-1234178",
            "Raul",
            "Siete",
            one_hundred_years_ago.strftime("%m/%d/%Y"),
            "0412 345. 6789",
            "chav@ez.co",
            "San Antonio de los Altos",
        )

        # Otros formatos de teléfono
        _test_register_client_valid(
            "V-2234678",
            "Nombre",
            "Generico",
            "01/01/2000",
            "412 (345) 67.89",
            "chav@ez.co",
            "No Sé",
        )

        _test_register_client_valid(
            "V-3234678",
            "Jesus",
            "David",
            "01/01/2000",
            "58 412 345 6789",
            "jdavis@isb.co",
            "La Victoria",
        )

        _test_register_client_valid(
            "V-4234678",
            "Perez",
            "Rodriguez",
            "01/01/2000",
            "+58412-345.6789",
            "perez@rod.net",
            "Bajo un Puente",
        )

        _test_register_client_valid(
            "V-2346789",
            "Nombre",
            "Extraño",
            "01/01/2000",
            "0058.412(345)67-89",
            "nombre@gmail.com",
            "Sambil",
        )

    def test_register_client_invalid_id(self):
        """Testea la creación de clientes con cédula inválida."""

        def _test_register_client_invalid_id(id_number: str):
            self._register_client(
                id_number,
                "UsuarioPrueba",
                "Hola",
                "01/01/2001",
                "+584244444444",
                "aaa@aaa.aa",
                "Por ahí",
            )
            self.assertEqual(
                self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
                "La cédula ingresada es inválida, debe tener el formato V-12345678",
            )

        self._login_analyst()

        # Sin guión
        _test_register_client_invalid_id("V2346789")

        # Sin letra
        _test_register_client_invalid_id("2346789")

        # Menor a 7 dígitos
        _test_register_client_invalid_id("V-234678")

        # Mayor a 8 dígitos
        _test_register_client_invalid_id("V-123456789")

        # Más de un guión
        _test_register_client_invalid_id("V--123456789")

        # Más de dos letras al comienzo
        _test_register_client_invalid_id("VV-123456789")

        # Letra al final
        _test_register_client_invalid_id("V-123456789a")

    def test_register_client_invalid_birthdate(self):
        """Testea la creación de clientes con fecha de nacimiento inválido."""

        def _test_register_client_invalid_birthdate(birthdate: str, message: str):
            self._register_client(
                "V-12345678",
                "UsuarioPrueba",
                "Hola",
                birthdate,
                "+584244444444",
                "aaa@aaa.aa",
                "Por ahí",
            )
            self.assertEqual(
                self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
                message,
            )

        self._login_analyst()

        # Mayor a 100 años
        one_hundred_years_ago = datetime.date.today() - datetime.timedelta(
            days=365 * 102
        )
        _test_register_client_invalid_birthdate(
            one_hundred_years_ago.strftime("%m/%d/%Y"),
            "La edad máxima para registrarse es 100 años",
        )

        # Menor a 18 años
        eighteen_years_ago = datetime.date.today() - datetime.timedelta(
            days=365 * 18 + 1
        )

        _test_register_client_invalid_birthdate(
            eighteen_years_ago.strftime("%m/%d/%Y"),
            "La edad mínima para registrarse es 18 años",
        )

        # Hoy
        _test_register_client_invalid_birthdate(
            datetime.date.today().strftime("%m/%d/%Y"),
            "La edad mínima para registrarse es 18 años",
        )

    def test_register_client_invalid_phone(self):
        """Testea la creación de clientes con teléfono inválido."""

        def _test_register_client_invalid_phone(phone: str):
            self._register_client(
                "V-12345678",
                "UsuarioPrueba",
                "Hola",
                "01/01/2001",
                phone,
                "usb@usb.usb",
                "Universida Simo Boliva",
            )

            self.assertEqual(
                self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
                "El número de teléfono ingresado no tiene un formato válido",
            )

        self._login_analyst()

        # Con codigo de otro país
        _test_register_client_invalid_phone("+14244444444")

        # Distinto de 10 digitos
        _test_register_client_invalid_phone("412 123.456")
        _test_register_client_invalid_phone("412 123.4567.8")

    def test_register_client_already_registered(self):
        """Testea la creación de clientes con cédula ya registrada."""

        self._login_analyst()

        self._register_client(
            "V-11122345",
            "UsuarioPrueba",
            "Hola",
            "01/01/2001",
            "+584244444444",
            "hola@hol.aaa",
            "República Popular China",
        )

        self.assertEqual(
            self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
            "Ya existe un cliente con la misma cédula",
        )

    def test_delete_client(self):
        """Testea la eliminación de clientes."""

        self._login_analyst()

        self.driver.find_element(By.CSS_SELECTOR, "#delete0 > .table-button").click()

        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "#delete-client-modal .modal-header")
            )
        )

        # Cancela la eliminación
        self.driver.find_element(
            By.CSS_SELECTOR, ".modal-footer:nth-child(3) > .btn"
        ).click()

        self.assertIn(
            "testclient@locatel.com.ve",
            self.driver.find_element(By.CSS_SELECTOR, ".table").text,
        )

        self.driver.find_element(By.CSS_SELECTOR, "#delete0 > .table-button").click()

        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "#delete-client-modal .modal-header")
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
            "Cliente eliminado exitosamente",
        )

        # Assert that the client is not in the table
        self.assertEqual(
            "No se encontraron clientes",
            self.driver.find_element(By.CSS_SELECTOR, ".alert").text,
        )

    def test_edit_client_valid(self):
        """Testea la creación de clientes válidos."""

        def _test_edit_client_valid(
            id_number: str,
            names: str,
            surnames: str,
            birthdate: str,
            phone: str,
            email: str,
            address: str,
        ):
            self._edit_client(
                id_number, names, surnames, birthdate, phone, email, address
            )
            self.assertEqual(
                self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
                "Cliente modificado exitosamente",
            )

            self.assertIn(
                email, self.driver.find_element(By.CSS_SELECTOR, ".table").text
            )

        self._login_analyst()

        # Cliente válido condiciones normales
        _test_edit_client_valid(
            "V-12345678",
            "Alan",
            "Turing",
            "06/23/2000",
            "04123456789",
            "alanturing@usb.ve",
            "Chacaito",
        )

        # Cédula distinta
        _test_edit_client_valid(
            "j-1234567",
            "Alan",
            "Turing",
            "06/23/2000",
            "04123456789",
            "alanturing@usb.ve",
            "Chacaito",
        )

        # Nombres y apellidos corto/largo
        _test_edit_client_valid(
            "V-92345678",
            "Ka",
            "Bolivar Palacios y Blanco de la Santisima Trinid",
            "06/23/2000",
            "04123456789",
            "uncorreo@usb.ve",
            "Charallave",
        )

        # Fecha de nacimiento al límite
        eighteen_years_ago = datetime.date.today() - datetime.timedelta(days=19 * 365)
        one_hundred_years_ago = datetime.date.today() - datetime.timedelta(
            days=99 * 365
        )
        _test_edit_client_valid(
            "V-1234678",
            "Chavez",
            "Maduro",
            eighteen_years_ago.strftime("%m/%d/%Y"),
            "0412 345. 6789",
            "chav@ez.co",
            "San Antonio de los Altos",
        )

        _test_edit_client_valid(
            "V-1234178",
            "Raul",
            "Siete",
            one_hundred_years_ago.strftime("%m/%d/%Y"),
            "0412 345. 6789",
            "chav@ez.co",
            "San Antonio de los Altos",
        )

        # Otros formatos de teléfono
        _test_edit_client_valid(
            "V-2234678",
            "Nombre",
            "Generico",
            "01/01/2000",
            "412 (345) 67.89",
            "chav@ez.co",
            "No Sé",
        )

        _test_edit_client_valid(
            "V-3234678",
            "Jesus",
            "David",
            "01/01/2000",
            "58 412 345 6789",
            "jdavis@isb.co",
            "La Victoria",
        )

        _test_edit_client_valid(
            "V-4234678",
            "Perez",
            "Rodriguez",
            "01/01/2000",
            "+58412-345.6789",
            "perez@rod.net",
            "Bajo un Puente",
        )

        _test_edit_client_valid(
            "V-2346789",
            "Nombre",
            "Extraño",
            "01/01/2000",
            "0058.412(345)67-89",
            "nombre@gmail.com",
            "Sambil",
        )
