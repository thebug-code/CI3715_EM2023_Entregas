from tests.unittests import BaseTestClass

import SAGTMA.utils.validations as validations


class TestClients(BaseTestClass):
    def test_validate_id_number_valid(self):
        """Testea la validación de cédulas válidas."""

        def _test_validate_id_number_valid(id: str, actual_id: str):
            self.assertEqual(validations.validate_id(id, Exception), actual_id)

        # Prueba varios formatos de números de cédula válidos
        _test_validate_id_number_valid("j-1234567", "J-1234567")
        _test_validate_id_number_valid("V-1.234.567", "V-1234567")
        _test_validate_id_number_valid("e-1 234 567", "E-1234567")
        _test_validate_id_number_valid("G-1 234 567", "G-1234567")
        _test_validate_id_number_valid("C-1 234.5.6 7", "C-1234567")

    def test_validate_id_number_invalid(self):
        """Testea la validación de cédulas inválidas."""

        def _test_validate_id_number_invalid(id: str):
            with self.assertRaises(Exception):
                validations.validate_id_number(id, Exception)

        # Sin guión
        _test_validate_id_number_invalid("V2346789")

        # Sin letra
        _test_validate_id_number_invalid("2346789")

        # Menor a 7 dígitos
        _test_validate_id_number_invalid("V-234678")

        # Mayor a 8 dígitos
        _test_validate_id_number_invalid("V-123456789")

        # Más de un guión
        _test_validate_id_number_invalid("V--123456789")

        # Más de dos letras al comienzo
        _test_validate_id_number_invalid("VV-123456789")

        # Letra al final
        _test_validate_id_number_invalid("V-123456789a")

    def test_validate_name_valid(self):
        "Testea la validación de nombres válidos"

        def _test_validate_name_valid(name):
            self.assertIsNone(validations.validate_name(name, Exception))

        # Nombres de 2 y 50 caracteres
        _test_validate_name_valid("Ja")
        _test_validate_name_valid("Nombre Generico De Cincuenta Caracteres Claroquesi")

        # Valor nominal
        _test_validate_name_valid("Nombre Normál 1ro")

    def test_validate_name_invalid(self):
        "Testea la validación de nombres inválidos"

        def _test_validate_name_invalid(name: str):
            with self.assertRaises(Exception):
                validations.validate_name(name)

        # Nombres de 1 y 51 caracteres
        _test_validate_name_invalid("K")
        _test_validate_name_invalid(
            "Nombre Generico De Cincuenta1 Caracteres Claroquesi"
        )

        # Nombre con caracteres especiales
        _test_validate_name_invalid("Nombre@Raro ^ Qué")
