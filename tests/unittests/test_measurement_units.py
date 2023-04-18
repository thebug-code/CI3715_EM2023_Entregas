from tests.unittests import BaseTestClass

from SAGTMA.models import (
    db,
    MeasureUnit,
)
import SAGTMA.utils.measurement_units as mu


class MeasurementUnitsTests(BaseTestClass):
    def populate_db(self):
        super().populate_db()

        # Añade una unidad de medida
        unit = MeasureUnit(6, "Centímetros")
        unit.id = 0

        db.session.add(unit)
        db.session.commit()

    def _post_register_unit(self, data: dict):
        """Envía una petición POST para registrar una unidad de medida."""
        return self.client.post(
            "/measurement-units/register/", data=data, follow_redirects=True
        )

    def _post_edit_unit(self, data: dict):
        """Envía una petición POST para editar una unidad de medida."""
        return self.client.post(
            f"/measurement-units/{data['id']}/edit/", data=data, follow_redirects=True
        )

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

    def test_register_unit_valid(self):
        """Testea el registro de una unidad de medida válida"""
        self._login_admin()

        # Datos de unidad válidos
        self._post_register_unit({"dimension": "1", "unit": "Pulgada"})

        stmt = db.select(MeasureUnit).where(MeasureUnit.unit == "Pulgada")
        self.assertIsNotNone(db.session.execute(stmt).first())

    def test_register_unit_invalid(self):
        """Testea el registro de una unidad de medida inválida"""
        self._login_admin()

        # Datos de unidad inválidos
        self._post_register_unit({"dimension": "0", "unit": "Pulgada"})

        stmt = db.select(MeasureUnit).where(MeasureUnit.unit == "Pulgada")
        self.assertIsNone(db.session.execute(stmt).first())

        self._post_register_unit({"dimension": "1", "unit": ""})

        stmt = db.select(MeasureUnit).where(MeasureUnit.unit == "")
        self.assertIsNone(db.session.execute(stmt).first())

    def test_edit_unit_valid(self):
        """Testea la edición de una unidad de medida válida"""
        self._login_admin()

        # Datos de unidad válidos
        self._post_edit_unit(data={"dimension": "10", "unit": "Metros", "id": 0})

        stmt = db.select(MeasureUnit).where(MeasureUnit.unit == "Metros")
        self.assertIsNotNone(db.session.execute(stmt).first())

        stmt = db.select(MeasureUnit).where(MeasureUnit.unit == "Centímetros")
        self.assertIsNone(db.session.execute(stmt).first())

    def test_edit_unit_invalid(self):
        """Testea la edición de una unidad de medida inválida"""
        self._login_admin()

        # Datos de unidad inválidos
        self._post_edit_unit(data={"dimension": "0", "unit": "m2", "id": 0})

        stmt = db.select(MeasureUnit).where(MeasureUnit.unit == "m2")
        self.assertIsNone(db.session.execute(stmt).first())

        self._post_edit_unit(data={"dimension": "1", "unit": "", "id": 0})

        stmt = db.select(MeasureUnit).where(MeasureUnit.unit == "")
        self.assertIsNone(db.session.execute(stmt).first())

        stmt = db.select(MeasureUnit).where(MeasureUnit.unit == "Centímetros")
        self.assertIsNotNone(db.session.execute(stmt).first())

    def test_delete_unit_valid(self):
        """Testea la eliminación de una unidad de medida de forma válida."""
        self._login_admin()

        # Elimina la unidad de medida
        self.client.post("/measurement-units/0/delete/", follow_redirects=True)

        stmt = db.select(MeasureUnit).where(MeasureUnit.id == 0)
        self.assertIsNone(db.session.execute(stmt).first())

    def test_delete_unit_invalid(self):
        """Testea la eliminación de una unidad de medida de forma inválida."""
        self._login_admin()

        # Elimina la unidad de medida
        self.client.post("/measurement-units/1/delete/", follow_redirects=True)

        stmt = db.select(MeasureUnit).where(MeasureUnit.id == 0)
        self.assertIsNotNone(db.session.execute(stmt).first())
