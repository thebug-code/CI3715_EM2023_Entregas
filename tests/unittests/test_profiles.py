from tests.unittests import BaseTestClass
from SAGTMA.utils import profiles
from SAGTMA.models import User, db


class TestProfiles(BaseTestClass):
    def _login_admin(self):
        """Inicia sesión con un usuario Administrador."""
        return self.login_user("admin", "Admin123.")

    def test_validate_password_invalid(self):
        """Testea registros de usuarios con contraseñas inválidas.

        Testea los casos de contraseñas con las siguientes características:
         - Menos de 6 caracteres.
         - Más de 20 caracteres.
         - Sin número.
         - Sin mayúsculas.
         - Sin minúsculas.
         - Sin caracteres especiales.
        """

        def _test_validate_password_invalid(password: str):
            with self.assertRaises(profiles.ProfileError):
                profiles.validate_password(password)

        # Menos de 6 caracteres
        _test_validate_password_invalid("Al1")

        # Más de 20 caracteres
        _test_validate_password_invalid("AliceTheBest123_4567.")

        # Sin número
        _test_validate_password_invalid("Alice.")

        # Sin mayúsculas
        _test_validate_password_invalid("alice123.")

        # Sin minúsculas
        _test_validate_password_invalid("ALICE123.")

        # Sin caracteres especiales
        _test_validate_password_invalid("Alice123")

    def test_validate_password_valid(self):
        """Testea la creación de usuarios con la contraseñas válidas."""

        def _test_validate_password_valid(password: str):
            self.assertIsNone(profiles.validate_password(password))

        # Contraseña válida de 6 caracteres
        _test_validate_password_valid("Alice1.")

        # Contraseña válida de 20 caracteres
        _test_validate_password_valid("AliceTheBest123_456.")

    def test_validate_username_invalid(self):
        """Testea la creación de usuarios con nombre de usuario inválidos

        Un nombre de usuario es válido si:
        -Tiene al menos 3 caracteres y a lo sumo 20 caracteres
        -No tiene caracteres especiales distintos de '_' (guión bajo)
        -No comienza con un caracter numérico
        """

        def _test_validate_username_invalid(username: str):
            with self.assertRaises(profiles.ProfileError):
                profiles.validate_username(username)

        # Usuario con menos de 3 caracteres
        _test_validate_username_invalid("ca")

        # Usuario con más de 20 caracteres
        _test_validate_username_invalid("John_Doe_The_Best_Username")

        # Usuario con caracteres especiales
        _test_validate_username_invalid("wal.")

        # Usuario que comienza con número
        _test_validate_username_invalid("1test")

    def test_validate_username_valid(self):
        """Testea la creación de usuarios con nombre de usuario válidos

        Un nombre de usuario es válido si:
        -Tiene al menos 3 caracteres y a lo sumo 20 caracteres
        -No tiene caracteres especiales distintos de '_' (guión bajo)
        -No comienza con un caracter numérico
        """
        # Usuario nominal
        self.assertIsNone(profiles.validate_username("admin_user123"))

    def test_register_user_mismatched_password(self):
        """Testea la creación de usuarios cuando la contraseña y su
        verificacion no coinciden"""
        self._login_admin()

        self.client.post(
            "/user-profiles/register/",
            data={
                "id-number": "V-12457845",
                "username": "test_user",
                "names": "Test",
                "surnames": "User",
                "password": "Test123.",
                "confirm-password": "Test123",
                "role": "2",
            },
            follow_redirects=True,
        )

        stmt = db.select(User).where(User.username == "test_user")
        self.assertIsNone(db.session.execute(stmt).first())

    def test_register_user_duplicated_username(self):
        """Testea la creación de usuarios con nombre de usuario ya registrado"""
        self._login_admin()

        self.client.post(
            "/user-profiles/register/",
            data={
                "id-number": "V-12457845",
                "username": "admin",
                "names": "Test",
                "surnames": "User",
                "password": "Test123.",
                "confirm-password": "Test123.",
                "role": "2",
            },
            follow_redirects=True,
        )

        stmt = db.select(User).where(User.username == "admin")
        self.assertEqual(len(db.session.execute(stmt).fetchall()), 1)

    def test_register_missing_fields(self):
        """Testea la creación de usuarios dejando todos los campos vacíos"""
        self._login_admin()

        self.client.post(
            "/user-profiles/register/",
            data={},
            follow_redirects=True,
        )

        stmt = db.select(User)
        self.assertEqual(len(db.session.execute(stmt).fetchall()), 1)

    def test_register_user_valid(self):
        self._login_admin()

        self.client.post(
            "/user-profiles/register/",
            data={
                "id-number": "V-12451845",
                "username": "admina",
                "names": "Test",
                "surnames": "User",
                "password": "Test123.",
                "confirm-password": "Test123.",
                "role": "3",
            },
            follow_redirects=True,
        )

        stmt = db.select(User)
        self.assertEqual(len(db.session.execute(stmt).fetchall()), 2)

    def test_delete_user(self):
        self._login_admin()

        self.client.post(
            "/user-profiles/register/",
            data={
                "id-number": "V-12451845",
                "username": "admina",
                "names": "Test",
                "surnames": "User",
                "password": "Test123.",
                "confirm-password": "Test123.",
                "role": "3",
            },
            follow_redirects=True,
        )

        self.client.post(
            "/user-profiles/2/delete/",
        )

        stmt = db.select(User)
        self.assertEqual(len(db.session.execute(stmt).fetchall()), 1)
