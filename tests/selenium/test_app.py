from tests.selenium import BaseTestClass


class TestWebApp(BaseTestClass):
    def test_selenium(self):
        """Testea que el driver de Selenium se crea correctamente"""
        assert self.driver is not None

        self.driver.get(f"{self.base_url}/")
        assert "SAGTMA" in self.driver.title
