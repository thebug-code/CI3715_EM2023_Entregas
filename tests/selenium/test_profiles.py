from random import randint

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from tests.selenium import BaseTestClass


class TestProfiles(BaseTestClass):
    def _login_admin(self):
        self.login_user("admin", "Admin123.")

    def _register_user(
        self,
        username: str,
        password: str,
        confirm_password: str,
        names: str,
        surnames: str,
    ):
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary:nth-child(4)").click()
        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "#add-user-modal .modal-header")
            )
        )
        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "confirm-password").click()
        self.driver.find_element(By.ID, "confirm-password").send_keys(confirm_password)
        self.driver.find_element(By.ID, "names").click()
        self.driver.find_element(By.ID, "names").send_keys(names)
        self.driver.find_element(By.ID, "surnames").click()
        self.driver.find_element(By.ID, "surnames").send_keys(surnames)
        self.driver.find_element(By.ID, "id-number").send_keys(
            f"V-{randint(1000000, 99999999)}"
        )
        self.driver.find_element(
            By.CSS_SELECTOR, ".modal-footer:nth-child(8) > .btn-primary"
        ).click()
        self.driver.find_element(By.CSS_SELECTOR, ".toast-body").click()
        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, ".toast-body")
            )
        )

    def test_register_invalid_password(self):
        """Testea registros de usuarios con contraseñas inválidas.

        Testea los casos de contraseñas con las siguientes características:
         - Menos de 6 caracteres.
         - Más de 20 caracteres.
         - Sin número.
         - Sin mayúsculas.
         - Sin minúsculas.
         - Sin caracteres especiales.
        """

        def _test_register_invalid_password(password: str, message: str):
            self._register_user("test1", password, password, "Alicia", "Maravilla")

            self.assertEqual(
                self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text, message
            )

            self.assertNotIn(
                "test1",
                self.driver.find_element(By.CSS_SELECTOR, ".table").text,
            )

        self._login_admin()

        # Menos de 6 caracteres
        _test_register_invalid_password(
            "Al1", "La contraseña debe tener entre 6 y 20 caracteres."
        )

        # Más de 20 caracteres
        _test_register_invalid_password(
            "AliceTheBest123_4567.", "La contraseña debe tener entre 6 y 20 caracteres."
        )

        # Sin número
        _test_register_invalid_password(
            "Alice.", "La contraseña debe contener al menos un número."
        )

        # Sin mayúsculas
        _test_register_invalid_password(
            "alice123.",
            "La contraseña debe contener al menos una mayúscula y una minúscula",
        )

        # Sin minúsculas
        _test_register_invalid_password(
            "ALICE123.",
            "La contraseña debe contener al menos una mayúscula y una minúscula",
        )

        # Sin caracteres especiales
        _test_register_invalid_password(
            "Alice123", "La contraseña debe contener al menos un caracter especial."
        )

    def test_register_valid_password(self):
        """Testea la creación de usuarios con la contraseñas válidas."""

        def _test_register_valid_password(id: int, password_to_test: str):
            self._register_user(
                f"test{id}",
                password_to_test,
                password_to_test,
                f"Alicia{id}",
                f"Maravilla{id}",
            )

            self.assertEqual(
                self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
                "Usuario registrado exitosamente",
            )
            self.assertIn(
                f"test{id}", self.driver.find_element(By.CSS_SELECTOR, ".table").text
            )

        self._login_admin()

        # Contraseña válida de 6 caracteres
        _test_register_valid_password(1, "Alice1.")

        # Contraseña válida de 20 caracteres
        _test_register_valid_password(2, "AliceTheBest123_456.")

    def test_register_invalid_user(self):
        """Testea la creación de usuarios con nombre de usuario inválidos

        Un nombre de usuario es válido si:
        -Tiene al menos 3 caracteres y a lo sumo 20 caracteres
        -No tiene caracteres especiales distintos de '_' (guión bajo)
        -No comienza con un caracter numérico
        """

        def _test_register_invalid_user(username: str, message: str):
            self._register_user(username, "Pass123.", "Pass123.", "Ca", "Rlos")

            self.assertEqual(
                self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
                message,
            )
            self.assertNotIn(
                "ca", self.driver.find_element(By.CSS_SELECTOR, ".table").text
            )

        self._login_admin()

        # Usuario con menos de 3 caracteres
        _test_register_invalid_user(
            "ca", "El nombre de usuario debe tener entre 3 y 20 caracteres."
        )

        # Usuario con más de 20 caracteres
        _test_register_invalid_user(
            "John_Doe_The_Best_Username",
            "El nombre de usuario debe tener entre 3 y 20 caracteres.",
        )

        # Usuario con caracteres especiales
        _test_register_invalid_user(
            "wal.", "El nombre de usuario no puede contener caracteres especiales."
        )

        # Usuario que comienza con número
        _test_register_invalid_user(
            "1test", "El nombre de usuario no puede comenzar con un número."
        )

    def test_register_mismatched_password(self):
        """Testea la creación de usuarios cuando la contraseña y su
        verificacion no coinciden"""

        self._login_admin()

        self._register_user("test1", "Alice123.", "Alice123", "Alicia", "Maravilla")

        self.assertEqual(
            self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
            "Las contraseñas ingresadas no coinciden",
        )
        self.assertNotIn(
            "test1", self.driver.find_element(By.CSS_SELECTOR, ".table").text
        )

    def test_register_duplicated_username(self):
        """Testea la creación de usuarios con nombre de usuario ya registrado"""
        self._login_admin()

        self._register_user("test1", "Pass123.", "Pass123.", "UsuarioPrueba", "Uno")
        self._register_user("test1", "Pass123.", "Pass123.", "UsuarioPrueba", "Uno")
        self.assertEqual(
            self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
            "El nombre de usuario ya existe",
        )
