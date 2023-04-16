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
import SAGTMA.utils.measurement_units as mu


class MeasurementUnitsTests(BaseTestClass):
    def test_validate_dimension_valid(self):
        """Testea la validación de dimensiones válidas."""

        def _test(dimension: str, expected: float):
            self.assertEqual(mu.validate_dimension(dimension), expected)

        # Testea dimensiones válidas
        _test("1", 1)
        _test("1.0", 1.0)
        _test("0.01", 0.01)

    def test_validate_dimension_invalid(self):
        """Testea la validación de dimensiones inválidas."""
        def _test(dimension: str):
            with self.assertRaises(mu.MeasureUnitError):
                mu.validate_dimension(dimension)
        
        # Testea dimensiones inválidas
        _test("0")
        _test("-1")
        _test("a")
        _test("1a")
        _test("-0.01")

    def test_validate_unit_valid(self):
        """Testea la validación de unidades válidas."""
        def _test(unit: str):
            self.assertIsNone(mu.validate_unit(unit))

        _test("cm")
        _test("Pulgadas")
        _test("Metros cuadrados")

    def test_validate_unit_invalid(self):
        """Testea la validación de unidades inválidas."""
        def _test(unit: str):
            with self.assertRaises(mu.MeasureUnitError):
                mu.validate_unit(unit)

        _test("")
        _test("cm2")
        _test("Pulgadas-cuadradas")