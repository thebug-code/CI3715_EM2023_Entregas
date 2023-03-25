from tests.unittests import BaseTestClass


class TestWebApp(BaseTestClass):
    def test_client(self):
        """Testea que el cliente de pruebas se crea correctamente"""
        assert self.client is not None

        response = self.client.get("/login/", content_type="html/text")

        # Comprueba que la respuesta es correcta y que el contenido se está obteniendo
        self.assertEqual(response.status_code, 200)
        assert b"SAGTMA" in response.data
