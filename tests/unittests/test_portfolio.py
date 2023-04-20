from tests.unittests import BaseTestClass

from SAGTMA.models import User, Role, db, Project
from SAGTMA.utils.auth import hash_password
from SAGTMA.utils import projects
from datetime import date


class TestPortfolio(BaseTestClass):
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

        db.session.add_all([manager_user, project])
        db.session.commit()

    def test_register_project_valid(self):
        """Testea la creación de proyecto válidos."""
        self._login_manager()

        # Proyecto válido con descripción corta
        self.client.post(
            "/project-portfolio/add/",
            data={
                "description": "Proyecto de ejemplo",
                "start-date": "2022-04-01",
                "deadline": "2022-06-30",
            },
            follow_redirects=True,
        )

        stmt = db.select(Project).where(Project.description == "Proyecto de ejemplo")
        self.assertIsNotNone(db.session.execute(stmt).first())
        self._test_logger_works()

    def test_validate_descrip_project_valid(self):
        "Testea la validacion de descripciones de proyecto válidas"

        def _test_validate_descrip_project_valid(description: str):
            self.assertIsNone(projects.validate_descrip_project(description))

        # Descripciones de 6 y 100 caracteres
        _test_validate_descrip_project_valid("Hello!")
        _test_validate_descrip_project_valid(
            "A project description of 100 characters should be valid... right? No se que escribir aqui para llena"
        )

        # Valor nominal
        _test_validate_descrip_project_valid(
            "Esta es una descripción de proyecto válida!"
        )

    def test_validate_descrip_project_invalid(self):
        "Testea la validacion de descripciones de proyecto inválidas"

        def _test_validate_descrip_project_invalid(description: str):
            with self.assertRaises(projects.ProjectError):
                projects.validate_descrip_project(description)

        # Descripciones de 5 y 101 caracteres
        _test_validate_descrip_project_invalid("Nope")
        _test_validate_descrip_project_invalid(
            "Una descripción de proyecto que tome literalmente CIENTO UN CARACTERES no debe ser valida, es así???."
        )

        # Descripción con caracteres no válidos
        _test_validate_descrip_project_invalid("Descripcion con caracteres *invalidos*")

    def test_delete_project(self):
        """Testea la eliminación de proyectos."""
        self._login_manager()

        # Elimina un proyecto existente
        self.client.post(f"/project-portfolio/0/delete/", follow_redirects=True)

        # Verifica que se eliminó el proyecto
        stmt = db.select(Project).where(Project.description == "Proyecto Automotriz 1")
        self.assertIsNone(db.session.execute(stmt).first())
        self._test_logger_works()

    def test_edit_project_valid(self):
        """Testea la edición de un proyecto válido."""
        self._login_manager()

        self.client.post(
            "/project-portfolio/0/edit/",
            data={
                "description": "Proyecto Editado",
                "start-date": "2023-03-26",
                "deadline": "2023-06-30",
            },
            follow_redirects=True,
        )

        # Verifica que el proyecto anterior no existe
        stmt = db.select(Project).where(Project.description == "Proyecto Automotriz 1")
        self.assertIsNone(db.session.execute(stmt).first())

        # Verifica que el proyecto editado existe
        stmt = db.select(Project).where(Project.description == "Proyecto Editado")
        self.assertIsNotNone(db.session.execute(stmt).first())
        self._test_logger_works()
