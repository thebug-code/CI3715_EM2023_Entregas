from SAGTMA import create_app
from tests import BaseTestClass


class TestWebApp(BaseTestClass):
    def test_app(self):
        """Testea que la aplicacion se crea correctamente y está en modo
        testing"""
        assert not create_app().testing
        assert create_app({"TESTING": True}).testing
        assert self.app is not None
        assert self.app.testing

    def test_selenium(self):
        """Testea que el driver de Selenium se crea correctamente"""
        assert self.driver is not None

        self.driver.get("http://localhost:5000/")
        assert "SAGTMA" in self.driver.title
