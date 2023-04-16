from tests.unittests import BaseTestClass

from SAGTMA.models import (
    User,
    Role,
    db,
    Project,
    Client,
    Vehicle,
    Department,
    ProjectDetail,  # Dejar los que hacen falta
)
from SAGTMA.utils.auth import hash_password
import SAGTMA.utils.project_plans as pp


class ProjectPlansTests(BaseTestClass):
    def test_valid_working_hours(self):
        """Testea la validación de horas de trabajo válidas"""

        def _test(input_value: str, expected_value):
            self.assertEqual(pp.validate_works_hours(input_value), expected_value)

        # Caso borde
        _test("1")

        # Valor nominal
        _test("8")

    def test_invalid_working_hours(self):
        """Testea la validación de horas de trabajo inválidas"""

        def _test(input_value: str):
            with self.assertRaises(pp.ActionPlanError):
                pp.validate_works_hours(input_value)

        # Caso borde
        _test("0")

        # Entero negativo
        _test("-1")

        # No tiene formato de número
        _test("a")

        # No es entero
        _test("1.5")
