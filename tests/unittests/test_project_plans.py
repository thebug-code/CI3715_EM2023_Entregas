from tests.unittests import BaseTestClass

from SAGTMA.models import (
    User,
    Role,
    db,
    Project,
    Client,
    Vehicle,
    Department,
    ProjectDetail,
    ActionPlan,
    Activity,
    HumanTalent,
    MaterialSupply,
    MeasureUnit,
)
from SAGTMA.utils.auth import hash_password
import SAGTMA.utils.project_plans as pp
from datetime import date


class ProjectPlansTests(BaseTestClass):
    def populate_db(self):
        super().populate_db()

        # Añade un usuario Gerente de Operaciones
        stmt = db.select(Role).where(Role.name == "Gerente de Operaciones")
        (manager,) = db.session.execute(stmt).fetchone()

        manager_user = User(
            "V-1000000",
            "manager",
            "Bad",
            "Bunny",
            hash_password("Manager123."),
            manager,
        )

        # Añade un proyecto
        project = Project(f"Proyecto Automotriz 1", date(2021, 4, 1), date(2023, 4, 1))
        project.id = 0

        # Añade un cliente y un vehículo
        client = Client(
            "V-11122345",
            "Cliente",
            "De Prueba",
            date(1974, 3, 16),
            "+584254635122",
            "testclient@locatel.com.ve",
            "Wock to Poland",
        )
        client.id = 0

        car = Vehicle(
            "ABC-123",
            "Toyota",
            "Corolla",
            2018,
            "A123456789",
            "987654321B",
            "Negro",
            "Clutch no funciona",
        )
        car.id = 0
        client.vehicles.append(car)

        # Añade un departamento
        dept = Department("Mecánica")
        dept.id = 0

        # Añade un detalle de proyecto
        detail = ProjectDetail(0, 0, 0, 1, "Prueba", 0.1, "N/A")
        detail.id = 0

        # Añade una unidad de medida
        unit = MeasureUnit(6, "Centímetros")
        unit.id = 0

        # Añade un plan de acción
        action = ActionPlan("Lavado", 0)
        action.id = 0

        # Añade una actividad, talento humano y material a esa acción
        activity = Activity(
            0, 0, "Preparar el material", date(2021, 4, 1), date(2023, 4, 1), 8, 80
        )
        activity.id = 0

        ht = HumanTalent(0, 8, 1, 7)
        ht.id = 0

        ms = MaterialSupply(0, 0, "Materiales", "Lija", 1, 32)
        ms.id = 0

        db.session.add_all(
            [
                manager_user,
                project,
                client,
                dept,
                detail,
                unit,
                action,
                activity,
                ht,
                ms,
            ]
        )

        db.session.commit()

    def _post_register_activity(self, data):
        """Envía una petición POST para registrar una actividad."""
        return self.client.post(
            f"/action-plans/{data['id']}/register/", data=data, follow_redirects=True
        )

    def _post_edit_activity(self, data):
        """Envía una petición POST para editar una actividad."""
        return self.client.post(
            f"/action-plans/{data['id']}/edit/", data=data, follow_redirects=True
        )

    def test_valid_working_hours(self):
        """Testea la validación de horas de trabajo válidas"""

        def _test(input_value: str, expected_value):
            self.assertEqual(pp.validate_works_hours(input_value), expected_value)

        # Caso borde
        _test("1", 1)

        # Valor nominal
        _test("8", 8)

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

    def test_register_activity_valid(self):
        """Testea el registro de una actividad válida"""
        self._login_manager()

        # Datos de actividad válidos
        self._post_register_activity(
            {
                "id": 0,
                "activity": "Prueba",
                "start-date": "2022-04-01",
                "deadline": "2022-04-01",
                "work-hours": "8",
                "charge-person": "2",
                "amount-person-hl": "1",
                "cost-hl": "1",
                "category-ms": "Materiales",
                "description-ms": "Jabón",
                "amount-ms": "1",
                "measure-unit-ms": "0",
                "cost-ms": "1",
                "new-action": "Lavado",
            }
        )

        stmt = db.select(Activity).where(Activity.description == "Prueba")
        self.assertIsNotNone(db.session.execute(stmt).first())

    def test_register_activity_invalid(self):
        """Testea el registro de una actividad inválida"""
        self._login_manager()

        def _test(field: str, value: str):
            data = {
                "id": 0,
                "activity": "Prueba",
                "start-date": "2024-04-01",
                "deadline": "2025-04-01",
                "work-hours": "8",
                "charge-person": "2",
                "amount-person-hl": "1",
                "cost-hl": "1",
                "category-ms": "Materiales",
                "description-ms": "Jabón",
                "amount-ms": "1",
                "measure-unit-ms": "0",
                "cost-ms": "1",
                "new-action": "Lavado",
            }

            data[field] = value
            self._post_register_activity(data)

            stmt = db.select(Activity).where(Activity.description == "Prueba")
            self.assertIsNone(db.session.execute(stmt).first())

        # Datos de actividad inválidos

        # Fecha fuera del rango del proyecto padre
        _test("start-date", "2020-04-01")

        # Id inexistente
        _test("id", "99")

        # Campos naturales negativos
        _test("work-hours", "-1")
        _test("work-hours", "-1")
        _test("charge-person", "-1")
        _test("amount-person-hl", "-1")
        _test("cost-hl", "-1")
        _test("amount-ms", "-1")
        _test("measure-unit-ms", "-1")
        _test("cost-ms", "-1")

    def test_edit_activity_valid(self):
        """Testea la edición de una actividad válida"""
        self._login_manager()

        # Datos de actividad válidos
        self._post_edit_activity(
            {
                "id": 0,
                "action": "Higiene",
                "activity": "Lavao",
                "start-date": "2022-04-01",
                "deadline": "2022-04-01",
                "work-hours": "8",
                "charge-person": "2",
                "amount-person-hl": "1",
                "cost-hl": "1",
                "category-ms": "Materiales",
                "description-ms": "Jabón",
                "amount-ms": "1",
                "measure-unit-ms": "0",
                "cost-ms": "1",
                "activity-id": "0",
                "project-detail-id": "0",
                "human-talent-id": "0",
                "material-supply-id": "0",
            }
        )

        stmt = db.select(Activity).where(Activity.description == "Lavao")
        self.assertIsNotNone(db.session.execute(stmt).first())

    def test_edit_activity_invalid(self):
        """Testea la edición de una actividad inválida"""
        self._login_manager()

        def _test(field: str, value: str):
            data = {
                "id": 0,
                "action": "Higiene",
                "activity": "Lavao",
                "start-date": "2022-04-01",
                "deadline": "2022-04-01",
                "work-hours": "8",
                "charge-person": "2",
                "amount-person-hl": "1",
                "cost-hl": "1",
                "category-ms": "Materiales",
                "description-ms": "Jabón",
                "amount-ms": "1",
                "measure-unit-ms": "0",
                "cost-ms": "1",
                "activity-id": "0",
                "project-detail-id": "0",
                "human-talent-id": "0",
                "material-supply-id": "0",
            }

            data[field] = value
            self._post_edit_activity(data)

            stmt = db.select(Activity).where(
                Activity.description == "Preparar el material"
            )
            self.assertIsNotNone(db.session.execute(stmt).first())

        # Datos de actividad inválidos
        # Fecha fuera del rango del proyecto padre
        _test("start-date", "2020-04-01")

        # Id inexistente
        _test("id", "99")

        # Campos naturales negativos
        _test("work-hours", "-1")
        _test("work-hours", "-1")
        _test("charge-person", "-1")
        _test("amount-person-hl", "-1")
        _test("cost-hl", "-1")
        _test("amount-ms", "-1")
        _test("measure-unit-ms", "-1")
        _test("cost-ms", "-1")

    def test_delete_activity_valid(self):
        """Testea la eliminación de una actividad válida"""
        self._login_manager()

        # Se elimina una actividad válida
        self.client.post(
            "/action-plans/0/delete/",
            data={"project-detail-id": "0", "delete-activity-id": "0"},
            follow_redirects=True,
        )

        stmt = db.select(Activity).where(Activity.id == 0)
        self.assertIsNone(db.session.execute(stmt).first())

    def test_delete_activity_invalid(self):
        """Testea la eliminación de una actividad inválida"""
        self._login_manager()

        # Se elimina una actividad inexistente
        self.client.post(
            "/action-plans/1/delete/",
            data={"project-detail-id": "0", "delete-activity-id": "0"},
            follow_redirects=True,
        )

        stmt = db.select(Activity).where(Activity.id == 0)
        self.assertIsNotNone(db.session.execute(stmt).first())
