from tests.unittests import BaseTestClass

from SAGTMA.models import User, Role, Client, Vehicle, db
from SAGTMA.utils.profiles import hash_password
from SAGTMA.utils import vehicles
import datetime


class TestVehicles(BaseTestClass):
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

    def test_register_vehicle_valid(self):
        """Testea la creación de vehículos válidos."""
        self._login_analyst()

        self.client.post(
            "/client-details/0/register/",
            data={
                "license-plate": "ABC-ACB",
                "brand": "Toyota",
                "model": "Model S",
                "year": "1975",
                "body-number": "ACV8148DAS",
                "engine-number": "ASCEV15CW",
                "color": "Ocre",
                "problem": "No le sirve la pintura",
            },
            follow_redirects=True,
        )

        stmt = db.select(Vehicle).where(Vehicle.license_plate == "ABC-ACB")
        self.assertIsNotNone(db.session.execute(stmt).first())

    def test_validate_license_plate_invalid(self):
        """Testea la validacion de placas con placas inválidas."""

        def _test_validate_license_plate_invalid(license_plate: str):
            with self.assertRaises(vehicles.VehicleError):
                vehicles.validate_license_plate(license_plate)

        # Placa muy corta
        _test_validate_license_plate_invalid("NR16")

        # Placa muy larga
        _test_validate_license_plate_invalid("NR2160DAAC1")

        # Placa con dos guiones o espacios juntos
        _test_validate_license_plate_invalid("NR--16D")
        _test_validate_license_plate_invalid("NR  16D")

        # Placa comienza con guión
        _test_validate_license_plate_invalid("-NR116D")

    def test_validate_license_plate_valid(self):
        """Testea la validacion de placas con placas válidas."""

        def _test_validate_license_plate_valid(license_plate: str):
            self.assertIsNone(vehicles.validate_license_plate(license_plate))

        # Placa de 5 caracteres
        _test_validate_license_plate_valid("NR16Q")

        # Placa de 10 caracteres
        _test_validate_license_plate_valid("NR2160DAAC")

        # Placa con guión o espacio
        _test_validate_license_plate_valid("N-R-16D")
        _test_validate_license_plate_valid("NR 16 D")

    def test_validate_year_invalid(self):
        """Testea la validación de años con años inválidos."""

        def _test_validate_year_invalid(year: str):
            with self.assertRaises(vehicles.VehicleError):
                vehicles.validate_year(year)

        # Año anterior a 1900
        _test_validate_year_invalid(1899)

        # Año posterior al actual + 1
        actual_year = datetime.datetime.now().year
        _test_validate_year_invalid(int(actual_year + 2))

    def test_validate_year_valid(self):
        """Testea la validacion de años con años válidos."""

        def _test_validate_year_valid(year: str):
            self.assertEqual(vehicles.validate_year(year), int(year))

        # Años al límite
        actual_year = datetime.datetime.now().year
        _test_validate_year_valid(1900)
        _test_validate_year_valid(int(actual_year))

        # Valor nominal
        _test_validate_year_valid(2012)

    def test_validate_serial_invalid(self):
        """Testea la validación de seriales con seriales inválidos."""

        def _test_validate_serial_invalid(serial: str):
            with self.assertRaises(vehicles.VehicleError):
                vehicles.validate_serial_number(serial)

        # Serial muy corto
        _test_validate_serial_invalid("AB12")

        # Serial muy largo
        _test_validate_serial_invalid("ABCDEFG0-1234567-8F-A")

        # Serial con caracteres inválidos
        _test_validate_serial_invalid("ABCDEFG0126@7")

        # Serial con dos guiones consecutivos
        _test_validate_serial_invalid("A--B12")

        # Serial comienza o termina con guión
        _test_validate_serial_invalid("-AB12")
        _test_validate_serial_invalid("AB12-")

    def test_validate_serial_valid(self):
        """Testea la validacion de seriales con seriales válidos."""

        def _test_validate_serial_valid(serial: str):
            self.assertIsNone(vehicles.validate_serial_number(serial))

        # Serial del mínimo y máximo de caracters
        _test_validate_serial_valid("ABC12")
        _test_validate_serial_valid("ABC123456789DEFGHJKL")

        # Con caracteres especiales
        _test_validate_serial_valid("A-B-C-123-456")

        # Valor nominal
        _test_validate_serial_valid("MES056-EDF484ZQF")

    def test_validate_color_invalid(self):
        """Testea la validación de colores con colores inválidos."""

        def _test_validate_color_invalid(color: str):
            with self.assertRaises(vehicles.VehicleError):
                vehicles.validate_color(color)

        # Color muy corto
        _test_validate_color_invalid("U")

        # Color muy largo
        _test_validate_color_invalid("Negro mate con toques")

        # Color con caracteres inválidos
        _test_validate_color_invalid("@Asure")

    def test_validate_color_valid(self):
        """Testea la validacion de colores con color válido."""

        def _test_validate_color_valid(color: str):
            self.assertIsNone(vehicles.validate_color(color))

        # Color de número mínimo y máximo de caracteres
        _test_validate_color_valid("AO")
        _test_validate_color_valid("Rosado Camarón Claro")

        # Con número
        _test_validate_color_valid("Pantone 5760")

        # Valor nominal
        _test_validate_color_valid("Negro fluorescente")

    def test_vehicle_already_exists(self):
        """Testea la creación de vehículos que ya existen."""
        self._login_analyst()

        self.client.post(
            "/client-details/0/register/",
            data={
                "license-plate": "ABC-123",
                "brand": "Otro",
                "model": "Carro Cualquiera",
                "year": "2010",
                "body-number": "ACQQ148DAS",
                "engine-number": "ASQQV15CW",
                "color": "Azul",
                "problem": "Otra cosa",
            },
            follow_redirects=True,
        )

        stmt = db.select(Vehicle)
        self.assertEqual(len(db.session.execute(stmt).fetchall()), 1)

    def test_delete_vehicle(self):
        """Testea la eliminación de vehículos."""

        self._login_analyst()

        self.client.post(
            "/client-details/1/delete/",
            data={"client-id": "0"},
            follow_redirects=True,
        )

        stmt = db.select(Vehicle)
        self.assertIsNone(db.session.execute(stmt).fetchone())

    def test_edit_vehicle_valid(self):
        """Testea la edición válida de vehículos."""

        self._login_analyst()

        self.client.post(
            "/client-details/1/edit/",
            data={
                "client-id": "0",
                "license-plate": "ABC-123",
                "brand": "Otro",
                "model": "Carro Cualquiera",
                "year": "2010",
                "body-number": "ACQQ148DAS",
                "engine-number": "ASQQV15CW",
                "color": "Azul",
                "problem": "Otra cosa",
            },
            follow_redirects=True,
        )

        stmt = db.select(Vehicle).where(Vehicle.license_plate == "ABC-123")
        self.assertEqual(db.session.execute(stmt).fetchone()[0].brand, "Otro")
        self.assertEqual(len(db.session.execute(stmt).fetchall()), 1)
