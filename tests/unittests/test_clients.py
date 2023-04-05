from tests.unittests import BaseTestClass

from SAGTMA.models import User, Role, Client, Vehicle, db
from SAGTMA.utils.profiles import hash_password
import SAGTMA.utils.clients as clients
import datetime


class TestClients(BaseTestClass):
    def populate_db(self):
        super().populate_db()

        stmt = db.select(Role).where(Role.name == "Analista de Operaciones")
        (analyst,) = db.session.execute(stmt).fetchone()

        # Añade un usuario Gerente de Operaciones
        analyst_user = User(
            "V-1000000",
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
            "2018",
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
        """Inicia sesión con un usuario Analista de Operaciones."""
        return self.login_user("analyst", "Analyst123.")

    def test_validate_phone_number_valid(self):
        """Testea la validación de números de teléfonos válidos."""

        def _test_validate_phone_number_valid(phone: str):
            self.assertEqual(clients.validate_phone_number(phone), "+584123456789")

        # Prueba varios formatos de números de teléfono válidos
        _test_validate_phone_number_valid("04123456789")
        _test_validate_phone_number_valid("412 (345) 67.89")
        _test_validate_phone_number_valid("58 412 345 6789")
        _test_validate_phone_number_valid("+58412-345.6789")
        _test_validate_phone_number_valid("0058.412(345)67-89")

    def test_validate_phone_number_invalid(self):
        """Testea la validación de números de teléfonos válidos."""

        def _test_validate_phone_number_invalid(phone: str):
            with self.assertRaises(clients.ClientError):
                clients.validate_phone_number(phone)

        # Con código de otro país
        _test_validate_phone_number_invalid("+14244444444")

        # Distinto de 10 dígitos
        _test_validate_phone_number_invalid("412 123.456")
        _test_validate_phone_number_invalid("412 123.4567.8")

    def test_validate_birthdate_valid(self):
        """Testea la creación de clientes con fecha de nacimiento válida."""

        def _test_validate_birthdate_valid(birthdate: str):
            self.assertIsNone(clients.validate_birthdate(birthdate))

        # 18 años
        eighteen_years = datetime.date.today() - datetime.timedelta(days=365 * 18 + 10)
        _test_validate_birthdate_valid(eighteen_years)

        # 25 años
        twenty_five_years = datetime.date.today() - datetime.timedelta(days=365 * 25)
        _test_validate_birthdate_valid(twenty_five_years)

        # 100 años
        one_hundred_years = datetime.date.today() - datetime.timedelta(days=365 * 100)
        _test_validate_birthdate_valid(one_hundred_years)

    def test_validate_birthdate_invalid(self):
        """Testea la creación de clientes con fecha de nacimiento inválida."""

        def _test_validate_birthdate_invalid(birthdate: str):
            with self.assertRaises(clients.ClientError):
                clients.validate_birthdate(birthdate)

        # Mayor a 100 años
        one_hundred_years_ago = datetime.date.today() - datetime.timedelta(
            days=365 * 102
        )
        _test_validate_birthdate_invalid(one_hundred_years_ago)

        # Menor a 18 años
        eighteen_years_ago = datetime.date.today() - datetime.timedelta(
            days=365 * 18 + 1
        )

        _test_validate_birthdate_invalid(eighteen_years_ago)

        # Hoy
        _test_validate_birthdate_invalid(datetime.date.today())

    def test_validate_email_valid(self):
        """Testea la validación de correos electrónicos válidos."""

        def _test_validate_email_valid(email: str):
            self.assertIsNone(clients.validate_email(email))

        # Dirección de correo electrónico válida
        _test_validate_email_valid("johndoe@example.com")

        # Dirección de correo electrónico válida con mayúsculas
        _test_validate_email_valid("JohnDoe@example.com")

    def test_validate_email_invalid(self):
        """Testea la validación de correos electrónicos inválidos."""

        def _test_validate_email_invalid(email: str):
            with self.assertRaises(clients.ClientError):
                clients.validate_email(email)

        # Faltan caracteres después del punto
        _test_validate_email_invalid("johndoe@example.")

        # Caracteres no permitidos en el dominio
        _test_validate_email_invalid("johndoe@exam_ple.com")

        # Dominio con sólo 1 letra
        _test_validate_email_invalid("johndoe@xorg.c")

        # Dirección de correo electrónico inválida - dominio con más de 7 letras
        _test_validate_email_invalid("johndoe@example.aguacate")

    def test_register_client_valid(self):
        """Testea la creación de clientes válidos."""
        self._login_analyst()

        self.client.post(
            "/client-details/register/",
            data={
                "id-number": "V-12457845",
                "names": "Test",
                "surnames": "Client",
                "birthdate": "2000-12-30",
                "phone-number": "+584124568789",
                "email": "aaaa@aaa.usb",
                "address": "Address AA123",
            },
            follow_redirects=True,
        )

        stmt = db.select(Client).where(Client.id_number == "V-12457845")
        self.assertIsNotNone(db.session.execute(stmt).first())

    def test_register_client_already_registered(self):
        """Testea la creación de clientes con cédula ya registrada."""
        self._login_analyst()

        stmt = db.select(Client).where(Client.id_number == "V-11122345")

        self.client.post(
            "/client-details/register/",
            data={
                "id-number": "V-11122345",
                "names": "Test",
                "surnames": "Client",
                "birthdate": "2000-12-30",
                "phone-number": "+584124568789",
                "email": "aaaa@aaa.usb",
                "address": "Address AA123",
            },
            follow_redirects=True,
        )

        self.assertEqual(len(db.session.execute(stmt).fetchall()), 1)

    def test_delete_client(self):
        """Testea la eliminación de clientes."""
        self._login_analyst()

        self.client.post("/client-details/delete/0/", follow_redirects=True)

        # Verifica que se elimino el cliente
        stmt = db.select(Client).where(Client.id_number == "V-11122345")
        self.assertIsNone(db.session.execute(stmt).first())

        # Verifica que se eliminó su vehiculos
        stmt = db.select(Vehicle).where(Vehicle.license_plate == "ABC-123")
        self.assertIsNone(db.session.execute(stmt).first())

    def test_edit_client_valid(self):
        """Testea la creación de clientes válidos."""
        self._login_analyst()

        self.client.post(
            "/client-details/edit/0/",
            data={
                "id-number": "V-12121212",
                "names": "Test",
                "surnames": "Client",
                "birthdate": "2000-12-30",
                "phone-number": "+584124568789",
                "email": "aaaa@aaa.usb",
                "address": "Address AA123",
            },
            follow_redirects=True,
        )

        # Verifica que el cliente anterior no existe
        stmt = db.select(Client).where(Client.id_number == "V-11122345")
        self.assertIsNone(db.session.execute(stmt).first())

        # Verifica que el cliente editado existe
        stmt = db.select(Client).where(Client.id_number == "V-12121212")
        self.assertIsNotNone(db.session.execute(stmt).first())
