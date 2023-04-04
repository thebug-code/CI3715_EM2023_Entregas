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

        stmt = db.select(Role).where(Role.name == "Gerente de Operaciones")
        (manager,) = db.session.execute(stmt).fetchone()

        # Añade un usuario Gerente de Operaciones
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

        db.session.add_all([manager_user, project, client, dept])
        db.session.commit()

    def _login_manager(self):
        return self.client.post(
            "/login/",
            data={"username": "manager", "password": "Manager123."},
            follow_redirects=True,
        )

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
                "amount": "150",
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
        self.assertIsNone(db.session.execute(stmt).first())

        # Hace la request con solo solución
        self.client.post(
            "/project-details/0/register/",
            data={
                "solution": "Arreglarlo p",
            },
            follow_redirects=True,
        )

        stmt = db.select(ProjectDetail).where(ProjectDetail.solution == "Arreglarlo p")
        self.assertIsNone(db.session.execute(stmt).first())

    def test_validate_amount_invalid(self):
        "Testea la validacion de montos válidos"

        def _test_validate_amount_invalid(amount: str):
            with self.assertRaises(pd.ProjectDetailError):
                pd.validate_amount(amount)

        # Monto negativo
        _test_validate_amount_invalid("-.1")
        _test_validate_amount_invalid("-100")

        # Monto no numérico
        _test_validate_amount_invalid("abc")
        _test_validate_amount_invalid("1.1.1")
        _test_validate_amount_invalid("1,1")
        _test_validate_amount_invalid("--1")

    def test_validate_amount_valid(self):
        "Testea la validacion de montos inválidos"

        def _test_validate_amount_valid(amount: str):
            self.assertEqual(pd.validate_amount(amount), float(amount))

        # Montos válidos
        _test_validate_amount_valid("0")
        _test_validate_amount_valid("1")
        _test_validate_amount_valid("1.1")
        _test_validate_amount_valid("100")
    
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

        # Agrega primero un proyecto
        self.client.post(
            "/project-details/0/register/",
            data={
                "vehicle": "0",
                "department": "0",
                "manager": "1",
                "solution": "Arreglarlo p",
                "amount": "150",
                "observations": "Ninguna por ahora",
            },
            follow_redirects=True,
        )

        # Edita el proyecto
        self.client.post(
            "/project-details/1/edit/",
            data={
                "vehicle": "0",
                "department": "0",
                "manager": "1",
                "solution": "Dejarlo asi",
                "amount": "150",
                "observations": "Ninguna por ahora",
                "project-id": "0",
            },
            follow_redirects=True,
        )

        stmt = db.select(ProjectDetail).where(ProjectDetail.solution == "Arreglarlo p")
        self.assertIsNone(db.session.execute(stmt).first())

        stmt = db.select(ProjectDetail).where(ProjectDetail.solution == "Dejarlo asi")
        self.assertIsNotNone(db.session.execute(stmt).first())

    def test_edit_project_data_invalid(self):
        """Testea la edición de datos proyecto válidos."""
        self._login_manager()

        # Agrega primero un proyecto
        self.client.post(
            "/project-details/0/register/",
            data={
                "vehicle": "0",
                "department": "0",
                "manager": "1",
                "solution": "Arreglarlo p",
                "amount": "150",
                "observations": "Ninguna por ahora",
            },
            follow_redirects=True,
        )

        # Edita el proyecto con un dato inválido
        self.client.post(
            "/project-details/1/edit/",
            data={
                "vehicle": "0",
                "department": "0",
                "manager": "1",
                "solution": "Dejarlo asi",
                "amount": "-150",
                "observations": "Ninguna por ahora",
                "project-id": "0",
            },
            follow_redirects=True,
        )

        stmt = db.select(ProjectDetail).where(ProjectDetail.solution == "Arreglarlo p")
        self.assertIsNotNone(db.session.execute(stmt).first())

        stmt = db.select(ProjectDetail).where(ProjectDetail.solution == "Dejarlo asi")
        self.assertIsNone(db.session.execute(stmt).first())

    # def test_delete_project(self):
    #     """Testea la eliminación de proyectos."""
    #     self._login_manager()

    #     # Elimina un proyecto existente
    #     self.client.post(f"/project-portfolio/0/delete/", follow_redirects=True)

    #     # Verifica que se eliminó el proyecto
    #     stmt = db.select(Project).where(Project.description == "Proyecto Automotriz 1")
    #     self.assertIsNone(db.session.execute(stmt).first())

    # def test_edit_project_valid(self):
    #     """Testea la edición de un proyecto válido."""
    #     self._login_manager()

    #     self.client.post(
    #         "/project-portfolio/0/edit/",
    #         data={
    #             "description": "Proyecto Editado",
    #             "start-date": "2023-03-26",
    #             "deadline": "2023-06-30",
    #         },
    #         follow_redirects=True,
    #     )

    #     # Verifica que el proyecto anterior no existe
    #     stmt = db.select(Project).where(Project.description == "Proyecto Automotriz 1")
    #     self.assertIsNone(db.session.execute(stmt).first())

    #     # Verifica que el proyecto editado existe
    #     stmt = db.select(Project).where(Project.description == "Proyecto Editado")
    #     self.assertIsNotNone(db.session.execute(stmt).first())
