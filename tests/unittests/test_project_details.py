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
)
from SAGTMA.utils.auth import hash_password
import SAGTMA.utils.project_details as pd
from datetime import date


class TestProjectDetails(BaseTestClass):
    def populate_db(self):
        super().populate_db()

        # Añade un usuario Analista
        stmt = db.select(Role).where(Role.name == "Analista de Operaciones")
        (analyst,) = db.session.execute(stmt).fetchone()

        analyst_user = User(
            "V-1001000",
            "analyst",
            "Bad3",
            "Bunny3",
            hash_password("Analyst123."),
            analyst,
        )

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

        db.session.add_all([analyst_user, manager_user, project, client, dept, detail])
        db.session.commit()

    def _login_manager(self):
        return self.login_user("manager", "Manager123.")

    def _login_analyst(self):
        return self.login_user("analyst", "Analyst123.")

    def _login_admin(self):
        return self.login_user("admin", "Admin123.")

    def test_add_project_data_valid(self):
        """Testea la adición de datos proyecto válidos."""
        self._login_manager()

        # Datos de proyecto válidos
        self.client.post(
            "/project-details/0/register/",
            data={
                "vehicle": "0",
                "department": "0",
                "manager": "1",
                "solution": "Arreglarlo p",
                "cost": "150",
                "observations": "Ninguna por ahora",
            },
            follow_redirects=True,
        )

        stmt = db.select(ProjectDetail).where(ProjectDetail.solution == "Arreglarlo p")
        self.assertIsNotNone(db.session.execute(stmt).first())

    def test_add_project_data_missing_fields_invalid(self):
        "Testea adición de datos de proyectos con los campos vacíos"

        self._login_manager()

        # Hace la request sin data
        self.client.post(
            "/project-details/0/register/",
            follow_redirects=True,
        )

        stmt = db.select(ProjectDetail)
        self.assertEqual(len(db.session.execute(stmt).fetchall()), 1)

        # Hace la request con solo solución
        self.client.post(
            "/project-details/0/register/",
            data={
                "solution": "Arreglarlo p",
            },
            follow_redirects=True,
        )

        stmt = db.select(ProjectDetail).where(ProjectDetail.solution == "Arreglarlo p")
        self.assertEqual(len(db.session.execute(stmt).fetchall()), 0)

    def test_validate_cost_invalid(self):
        "Testea la validacion de montos válidos"

        def _test_validate_cost_invalid(cost: str):
            with self.assertRaises(pd.ProjectDetailError):
                pd.validate_cost(cost)

        # Monto negativo
        _test_validate_cost_invalid("-.1")
        _test_validate_cost_invalid("-100")

        # Monto no numérico
        _test_validate_cost_invalid("abc")
        _test_validate_cost_invalid("1.1.1")
        _test_validate_cost_invalid("1,1")
        _test_validate_cost_invalid("--1")

    def test_validate_cost_valid(self):
        "Testea la validacion de montos inválidos"

        def _test_validate_cost_valid(cost: str):
            self.assertEqual(pd.validate_cost(cost), float(cost))

        # Montos válidos
        _test_validate_cost_valid("0")
        _test_validate_cost_valid("1")
        _test_validate_cost_valid("1.1")
        _test_validate_cost_valid("100")

    def test_validate_text_input_invalid(self):
        "Testea la validacion de inputs de texto inválidos"

        def _test_validate_text_input_invalid(text: str):
            with self.assertRaises(pd.ProjectDetailError):
                pd.validate_input_text(text)

        # Inputs vacíos
        _test_validate_text_input_invalid("")
        _test_validate_text_input_invalid(" ")
        _test_validate_text_input_invalid("  ")

        # Inputs con más de 100 caracteres
        _test_validate_text_input_invalid("a" * 101)

        # Inputs con caracteres inválidos
        _test_validate_text_input_invalid("a\n")

    def test_validate_text_input_valid(self):
        "Testea la validacion de inputs de texto válidos"

        def _test_validate_text_input_valid(text: str):
            self.assertIsNone(pd.validate_input_text(text))

        # Inputs válidos
        _test_validate_text_input_valid("N/A")
        _test_validate_text_input_valid("a" * 100)

    def test_edit_project_data_valid(self):
        """Testea la edición de datos proyecto válidos."""
        self._login_manager()

        # Edita el proyecto agregado en el setup
        self.client.post(
            "/project-details/0/edit/",
            data={
                "vehicle": "0",
                "department": "0",
                "manager": "1",
                "solution": "Dejarlo asi",
                "cost": "150",
                "observations": "Ninguna por ahora",
                "project-id": "0",
            },
            follow_redirects=True,
        )

        stmt = db.select(ProjectDetail).where(ProjectDetail.solution == "Prueba")
        self.assertIsNone(db.session.execute(stmt).first())

        stmt = db.select(ProjectDetail).where(ProjectDetail.solution == "Dejarlo asi")
        self.assertIsNotNone(db.session.execute(stmt).first())

    def test_edit_project_data_invalid(self):
        """Testea la edición de datos proyecto válidos."""
        self._login_manager()

        # Edita el proyecto con un dato inválido
        self.client.post(
            "/project-details/0/edit/",
            data={
                "vehicle": "0",
                "department": "0",
                "manager": "1",
                "solution": "Dejarlo asi",
                "cost": "-150",
                "observations": "Ninguna por ahora",
                "project-id": "0",
            },
            follow_redirects=True,
        )

        stmt = db.select(ProjectDetail).where(ProjectDetail.solution == "Prueba")
        self.assertIsNotNone(db.session.execute(stmt).first())

        stmt = db.select(ProjectDetail).where(ProjectDetail.solution == "Dejarlo asi")
        self.assertIsNone(db.session.execute(stmt).first())

    def test_delete_project_data(self):
        """Testea la eliminación de datos proyecto válidos."""
        self._login_manager()

        # Elimina un proyecto existente
        self.client.post(
            f"/project-details/0/delete/",
            data={
                "project-id": "0",
            },
            follow_redirects=True,
        )

        # Verifica que se eliminó el proyecto
        stmt = db.select(ProjectDetail).where(ProjectDetail.solution == "Prueba")
        self.assertIsNone(db.session.execute(stmt).first())

    def test_delete_client_project_associated(self):
        """Testea que no se pueda eliminar un cliente con proyectos asociados."""
        self._login_analyst()

        # Elimina un cliente con proyectos asociados
        self.client.post("/client-details/delete/0/", follow_redirects=True)

        # Verifica que no se eliminó el cliente
        stmt = db.select(Client).where(Client.names == "Cliente")
        self.assertIsNotNone(db.session.execute(stmt).first())

    def test_delete_vehicle_project_associated(self):
        """Testea que no se pueda eliminar un vehículo con proyectos asociados."""
        self._login_analyst()

        # Elimina un vehículo con proyectos asociados
        self.client.post(
            "/client-details/0/delete/",
            data={"client-id": "0"},
            follow_redirects=True,
        )

        # Verifica que no se eliminó el vehículo
        stmt = db.select(Vehicle).where(Vehicle.license_plate == "ABC-123")
        self.assertIsNotNone(db.session.execute(stmt).first())

    def test_delete_manager_project_associated(self):
        """Testea que no se pueda eliminar un usuario con proyectos asociados."""
        self._login_admin()

        # Añade un detalle de proyecto asociado a un gerente que no es admin
        detail = ProjectDetail(0, 0, 0, 2, "Prueba", 0.1, "N/A")
        detail.id = 1
        db.session.add(detail)
        db.session.commit()

        # Elimina un usuario con proyectos asociados
        self.client.post("/user-profiles/2/delete/")

        db.session.execute(db.select(User)).fetchall()

        # Verifica que no se eliminó el usuario
        stmt = db.select(User).where(User.username == "analyst")
        self.assertIsNotNone(db.session.execute(stmt).first())

    def test_delete_dept_project_associated(self):
        """Testea que no se pueda eliminar un departamento con proyectos asociados."""
        self._login_admin()

        # Elimina un departamento con proyectos asociados
        self.client.post("/workshop-departments/0/delete/", follow_redirects=True)

        # Verifica que no se eliminó el departamento
        stmt = db.select(Department).where(Department.description == "Mecánica")
        self.assertIsNotNone(db.session.execute(stmt).first())
