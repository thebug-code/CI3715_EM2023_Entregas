from SAGTMA.models import Role
from SAGTMA.utils import users
from tests import BaseTestClass


class TestAuth(BaseTestClass):
    def test_register_invalid_password(self):
        """Testea la creación de usuarios con la contraseñas inválidas.

        Una contraseña es válida si:
          -Tiene al menos 6 caracteres y a lo sumo 20 caracteres
          -Tiene al menos un número
          -Tiene al menos una mayúscula y una minúscula
          -Tiene al menos un caracter especial
        """

        def test_register_user(password_to_test: str):
            with self.assertRaises(users.InvalidPasswordError):
                users.register_user(
                    "Alice",
                    "Alice@example.com",
                    password_to_test,
                    password_to_test,
                    Role.USER,
                )

        # Menos de 6 caracteres
        test_register_user("Al1.")

        # Más de 20 caracteres
        test_register_user("AliceTheBest123_4567.")

        # Sin número
        test_register_user("Alice.")

        # Sin mayúsculas
        test_register_user("alice123.")

        # Sin minúsculas
        test_register_user("ALICE123.")

        # Sin caracteres especiales
        test_register_user("Alice123")

    def test_register_valid_password(self):
        """Testea la creación de usuarios con la contraseñas válidas."""

        def register_test_user(id: int, password_to_test: str):
            users.register_user(
                f"user_{id}",
                f"user_{id}@example.com",
                password_to_test,
                password_to_test,
                Role.USER,
            )

        # Creación de usuario con contraseña válida de 6 caracteres
        self.assertIsNone(register_test_user(1, "Alice1."))

        # Creación de usuario con contraseña válida de 20 caracteres
        self.assertIsNone(register_test_user(2, "AliceTheBest123....."))

    def test_register_no_empty_allowed(self):
        """Testea la creación de usuarios con campos vacíos."""
        with self.assertRaises(users.MissingFieldError):
            users.register_user(
                "", "Alice@example.com", "Alice123.", "Alice123.", Role.USER
            )

        with self.assertRaises(users.MissingFieldError):
            users.register_user("Alice", "", "Alice123.", "Alice123.", Role.USER)

        with self.assertRaises(users.MissingFieldError):
            users.register_user(
                "Alice", "Alice@example.com", "", "Alice123.", Role.USER
            )

        with self.assertRaises(users.MissingFieldError):
            users.register_user(
                "Alice", "Alice@example.com", "Alice123.", "", Role.USER
            )

    def test_register_invalid_user(self):
        """Testea la creación de usuarios con nombre de usuario inválidos

        Un nombre de usuario es válido si:
          -Tiene al menos 3 caracteres y a lo sumo 20 caracteres
          -No tiene caracteres especiales distintos de '_' (guión bajo)
          -No comienza con un caracter numérico
        """

        def test_register_user(username: str):
            with self.assertRaises(users.InvalidUsernameError):
                users.register_user(
                    username,
                    f"{username}@example.com",
                    "Hola123.",
                    "Hola123.",
                    Role.USER,
                )

        # Con menos de 3 caracteres
        test_register_user("ka")

        # Con más de 20 caracteres
        test_register_user("John_Doe_The_Best_Username")

        # Con caracteres especiales
        test_register_user("val.")

        # Empieza con un número
        test_register_user("1user")

    def test_register_mismatched_password(self):
        """Testea la creación de usuarios cuando la contraseña y su
        verificacion no coinciden
        """
        with self.assertRaises(users.PasswordMismatchError):
            users.register_user(
                "Alice", "Alice@example.com", "Alice123.", "Alice12.", Role.USER
            )

    def test_register_duplicated_username(self):
        """Testea la creación de usuarios con nombre de usuario o correo ya
        registrados
        """
        # Crea el usuario base
        users.register_user(
            "Alice", "Alice@example.com", "Alice123.", "Alice123.", Role.USER
        )

        with self.assertRaises(users.AlreadyExistingUserError):
            # Usuario ya registrado
            users.register_user(
                "Alice", "Alice_dup@example.com", "Alice123.", "Alice123.", Role.USER
            )

        with self.assertRaises(users.AlreadyExistingUserError):
            # Correo ya registrado
            users.register_user(
                "Alice_dup", "Alice@example.com", "Alice123.", "Alice123.", Role.USER
            )

    def test_register_invalid_email(self):
        """Se testea la creación de usuarios con correos inválidos"""

        def test_register_user(email: str):
            with self.assertRaises(users.InvalidEmailError):
                users.register_user(
                    "generic_user", email, "Hola123.", "Hola123.", Role.USER
                )

        test_register_user("Aliceexample.com")
        test_register_user("Alice@examplecom")
        test_register_user("Alice@example.a")
        test_register_user("Alice@example.")
        test_register_user(".@example.")
        test_register_user(".@example.com")

    def test_login_incorrect_password(self):
        """Testea el inicio de sesión con contraseña incorrecta"""
        users.register_user(
            "Alice", "Alice@example.com", "Alice123.", "Alice123.", Role.USER
        )

        with self.assertRaises(users.IncorrectPasswordError):
            users.log_user("Alice", "Alice12.")

    def test_login_correct_password(self):
        """Testea el inicio de sesión con contraseña correcta"""
        users.register_user(
            "Alice", "Alice@example.com", "Alice123.", "Alice123.", Role.USER
        )

        self.assertIsNotNone(users.log_user("Alice", "Alice123."))
