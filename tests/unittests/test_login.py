from tests.unittests import BaseTestClass
from SAGTMA.utils.auth import check_password, hash_password


class TestLogin(BaseTestClass):
    def test_login(self):
        """Testea el login con credenciales correctas."""
        res = self.client.post(
            "/login/",
            data={"username": "admin", "password": "Admin123."},
            follow_redirects=True,
        )

        self.assertNotIn(b"Iniciar Sesi", res.data)

    def test_login_incorrect_password(self):
        """Testea el login con credenciales incorrectas."""
        res = self.client.post(
            "/login/",
            data={"username": "admin", "password": "Admin123.."},
            follow_redirects=True,
        )

        self.assertIn(b"Iniciar Sesi", res.data)

    def test_logout(self):
        """Testea el cierre de sesión"""
        self.client.post(
            "/login/",
            data={"username": "admin", "password": "Admin123."},
            follow_redirects=True,
        )

        res = self.client.post(
            "/logout/",
            follow_redirects=True,
        )

        self.assertIn(b"Iniciar Sesi", res.data)

    def test_check_password_equal(self):
        self.assertTrue(check_password("Hola123.", hash_password("Hola123.")))

    def test_check_password_distinct(self):
        self.assertFalse(check_password("Hola123.", hash_password("Hola123")))
