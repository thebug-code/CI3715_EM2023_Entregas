from tests.unittests import BaseTestClass
from SAGTMA.utils import departments
from SAGTMA.models import Department, db


class TestProfiles(BaseTestClass):
    def populate_db(self):
        super().populate_db()

        # Añade un departamento
        dept = Department("Eléctrica")
        dept.id = 0

        db.session.add(dept)
        db.session.commit()

    def _login_admin(self):
        """Inicia sesión con un usuario Analista de Operaciones."""

        return self.client.post(
            "/login/",
            data={"username": "admin", "password": "Admin123."},
            follow_redirects=True,
        )

    def test_validate_dept_invalid(self):
        """Testea la validación de nombres de departamentos inválidos."""

        def _test_validate_dept_invalid(dept: str):
            with self.assertRaises(departments.DepartmentError):
                departments.validate_descrip_dept(dept)

        # Menos de 6 caracteres
        _test_validate_dept_invalid("Ciena")
        _test_validate_dept_invalid("C")
        _test_validate_dept_invalid("")

        # Más de 100 caracteres
        _test_validate_dept_invalid("Diez char." * 10 + "1")

        # Con caracteres inválidos
        for char in ",;*/\\+@#$%&()=":
            _test_validate_dept_invalid(f"Departamento {char}")

    def test_validate_dept_valid(self):
        """Testea la validación de nombres de departamentos válidos."""

        def _test_validate_dept_valid(dept: str):
            self.assertIsNone(departments.validate_descrip_dept(dept))

        # Descripción de 6 caracteres
        _test_validate_dept_valid("6chars")

        # Descripción de 100 caracteres
        _test_validate_dept_valid("Diez char." * 10)

        # Valor nominal
        _test_validate_dept_valid("Mecánica")

        # Con caracteres válidos
        for char in " -_?¿¡!:.":
            _test_validate_dept_valid(f"Departamento {char}")

    def test_register_dept_valid(self):
        """Testea el registro de un departamento válido"""
        self._login_admin()

        # Datos de depto válidos
        self.client.post(
            "/workshop-departments/register/",
            data={
                "description": "Mecánica",
            },
            follow_redirects=True,
        )

        stmt = db.select(Department).where(Department.description == "Mecánica")
        self.assertIsNotNone(db.session.execute(stmt).first())

    def test_register_dept_invalid(self):
        """Testea el registro de un departamento inválido"""
        self._login_admin()

        # Datos de depto inválidos
        self.client.post(
            "/workshop-departments/register/",
            data={
                "description": "Mec",
            },
            follow_redirects=True,
        )

        stmt = db.select(Department).where(Department.description == "Mec")
        self.assertIsNone(db.session.execute(stmt).first())

        #  Request vacía
        self.client.post(
            "/workshop-departments/register/",
            follow_redirects=True,
        )

        stmt = db.select(Department)
        self.assertEqual(len(db.session.execute(stmt).fetchall()), 1)

    def test_edit_dept_valid(self):
        """Testea la edición de departamentos válidos."""
        self._login_admin()

        # Edita el departamento agregado en el setup
        self.client.post(
            "/workshop-departments/0/edit/",
            data={
                "description": "Mecatrónica",
            },
            follow_redirects=True,
        )

        stmt = db.select(Department).where(Department.description == "Eléctrica")
        self.assertIsNone(db.session.execute(stmt).first())

        stmt = db.select(Department).where(Department.description == "Mecatrónica")
        self.assertIsNotNone(db.session.execute(stmt).first())

    def test_edit_dept_invalid(self):
        """Testea la edición de departamentos de manera inválida."""
        self._login_admin()

        # Edita el departamento agregado en el setup
        self.client.post(
            "/project-details/0/edit/",
            data={
                "description": "M",
            },
            follow_redirects=True,
        )

        stmt = db.select(Department).where(Department.description == "M")
        self.assertIsNone(db.session.execute(stmt).first())

        self.client.post("/project-details/0/edit/", follow_redirects=True)

        stmt = db.select(Department).where(Department.description == "Eléctrica")
        self.assertIsNotNone(db.session.execute(stmt).first())

    def test_delete_dept(self):
        """Testea la eliminación de departamentos válidos."""
        self._login_admin()

        # Elimina un departamento existente
        self.client.post(f"/workshop-departments/0/delete/", follow_redirects=True)

        # Verifica que se eliminó el proyecto
        stmt = db.select(Department)
        self.assertEqual(len(db.session.execute(stmt).fetchall()), 0)
