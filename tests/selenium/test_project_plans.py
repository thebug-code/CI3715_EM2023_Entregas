from time import sleep
from datetime import date

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

import SAGTMA.utils.project_plans as pp
from SAGTMA.models import (
    ActionPlan,
    Activity,
    Client,
    Department,
    HumanTalent,
    MaterialSupply,
    MeasureUnit,
    Project,
    ProjectDetail,
    Role,
    User,
    Vehicle,
    db,
)
from SAGTMA.utils.auth import hash_password
from tests.selenium import BaseTestClass


data = [
    "Acción existente",
    "Lavado",
    "Bad Bunny",
    "Echarle jabón",
    "04/20/2022",
    "04/25/2022",
    "8",
    "7",
    "7.5",
    "Insumos",
    "Jabón",
    "4",
    "4",
    "6 Centímetros",
]


data2 = [
    "Lavado",
    "Bad Bunny",
    "Soplarlo duro",
    "04/20/2022",
    "04/25/2022",
    "8",
    "7",
    "7.5",
    "Insumos",
    "Jabón",
    "4",
    "4",
    "6 Centímetros",
]


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

    def _login_manager(self):
        self.login_user("manager", "Manager123.")
        self.driver.get(f"{self.base_url}/action-plans/0/")

    def _register_activity(
        self,
        action_type: str,
        action_name: str,
        charge_person: str,
        activity: str,
        start_date: str,
        deadline: str,
        work_hours: str,
        n_people: str,
        cost_people: str,
        material_category: str,
        description: str,
        n_material: str,
        cost_material: str,
        unit: str,
    ):
        self.driver.find_element(
            By.CSS_SELECTOR, ".input-group > .btn:nth-child(3)"
        ).click()

        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "#add-action-plan-modal .modal-header")
            )
        )

        # Primera página
        Select(self.driver.find_element(By.ID, "action-type")).select_by_visible_text(
            action_type
        )
        Select(
            self.driver.find_element(By.ID, "add-charge-person")
        ).select_by_visible_text(charge_person)
        self.driver.find_element(By.ID, "add-activity").send_keys(activity)
        self.driver.find_element(By.ID, "add-start-date").send_keys(start_date)
        self.driver.find_element(By.ID, "add-deadline").send_keys(deadline)
        self.driver.find_element(By.ID, "add-work-hours").send_keys(work_hours)
        if action_type == "Nueva acción":
            self.driver.find_element(By.ID, "new-action").send_keys(action_name)
        elif action_type == "Acción existente":
            Select(
                self.driver.find_element(By.ID, "existing-action")
            ).select_by_visible_text(action_name)
        self.driver.find_element(
            By.CSS_SELECTOR, "#add-action-plan-form > .pagination .btn:nth-child(2)"
        ).click()

        # Segunda página
        self.driver.find_element(By.ID, "add-amount-person-hl").send_keys(n_people)
        self.driver.find_element(By.ID, "add-cost-hl").send_keys(cost_people)
        self.driver.find_element(
            By.CSS_SELECTOR, "#add-action-plan-form .btn:nth-child(3)"
        ).click()

        # Tercera página
        Select(
            self.driver.find_element(By.ID, "add-category-ms")
        ).select_by_visible_text(material_category)
        Select(
            self.driver.find_element(By.ID, "measure-unit-ms")
        ).select_by_visible_text(unit)
        self.driver.find_element(By.ID, "add-description-ms").send_keys(description)
        self.driver.find_element(By.ID, "add-amount-ms").send_keys(n_material)
        self.driver.find_element(By.ID, "add-cost-ms").send_keys(cost_material)
        self.driver.find_element(
            By.CSS_SELECTOR, ".modal-footer:nth-child(5) > .btn-primary"
        ).click()

        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, ".toast-body")
            )
        )

    def _edit_activity(
        self,
        action_name: str,
        charge_person: str,
        activity: str,
        start_date: str,
        deadline: str,
        work_hours: str,
        n_people: str,
        cost_people: str,
        material_category: str,
        description: str,
        n_material: str,
        cost_material: str,
        unit: str,
    ):
        self.driver.find_element(By.CSS_SELECTOR, "#edit0").click()

        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "#edit-action-plan-modal .modal-header")
            )
        )

        # Primera página
        self.driver.find_element(By.ID, "edit-action").clear()
        self.driver.find_element(By.ID, "edit-action").send_keys(action_name)
        Select(
            self.driver.find_element(By.ID, "edit-charge-person")
        ).select_by_visible_text(charge_person)
        self.driver.find_element(By.ID, "edit-activity").clear()
        self.driver.find_element(By.ID, "edit-activity").send_keys(activity)
        self.driver.find_element(By.ID, "edit-start-date").clear()
        self.driver.find_element(By.ID, "edit-start-date").send_keys(start_date)
        self.driver.find_element(By.ID, "edit-deadline").clear()
        self.driver.find_element(By.ID, "edit-deadline").send_keys(deadline)
        self.driver.find_element(By.ID, "edit-work-hours").clear()
        self.driver.find_element(By.ID, "edit-work-hours").send_keys(work_hours)
        self.driver.find_element(
            By.CSS_SELECTOR, "#edit-action-plan-form > .pagination .btn:nth-child(2)"
        ).click()

        # Segunda página
        self.driver.find_element(By.ID, "edit-amount-person-hl").clear()
        self.driver.find_element(By.ID, "edit-amount-person-hl").send_keys(n_people)
        self.driver.find_element(By.ID, "edit-cost-hl").clear()
        self.driver.find_element(By.ID, "edit-cost-hl").send_keys(cost_people)
        self.driver.find_element(
            By.CSS_SELECTOR, "#edit-action-plan-form .btn:nth-child(3)"
        ).click()

        # Tercera página
        Select(
            self.driver.find_element(By.ID, "edit-category-ms")
        ).select_by_visible_text(material_category)
        Select(
            self.driver.find_element(By.ID, "edit-measure-unit-ms")
        ).select_by_visible_text(unit)
        self.driver.find_element(By.ID, "edit-description-ms").clear()
        self.driver.find_element(By.ID, "edit-description-ms").send_keys(description)
        self.driver.find_element(By.ID, "edit-amount-ms").clear()
        self.driver.find_element(By.ID, "edit-amount-ms").send_keys(n_material)
        self.driver.find_element(By.ID, "edit-cost-ms").clear()
        self.driver.find_element(By.ID, "edit-cost-ms").send_keys(cost_material)
        self.driver.find_element(
            By.CSS_SELECTOR, ".modal-footer:nth-child(10) > .btn-primary"
        ).click()

        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, ".toast-body")
            )
        )

    def test_register_activity_valid(self):
        """Testea el registro de una actividad válida"""
        self._login_manager()

        def _test(
            action_type: str,
            action_name: str,
            charge_person: str,
            activity: str,
            start_date: str,
            deadline: str,
            work_hours: str,
            n_people: str,
            cost_people: str,
            material_category: str,
            description: str,
            n_material: str,
            cost_material: str,
            unit: str,
        ):
            self._register_activity(
                action_type,
                action_name,
                charge_person,
                activity,
                start_date,
                deadline,
                work_hours,
                n_people,
                cost_people,
                material_category,
                description,
                n_material,
                cost_material,
                unit,
            )
            self.assertEqual(
                self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
                "Actividad registrada exitosamente",
            )
            self.assertIn(activity, self.driver.page_source)

        _data = data.copy()

        # Datos de actividad válidos con accion existente
        _test(*_data)

        # Datos de actividad válidos con accion nueva
        _data[0] = "Nueva acción"
        _data[1] = "Secado"
        _test(*_data)

        # Datos de actividad válidos con accion recien agregada y costos 0
        _data[0] = "Acción existente"
        _data[3] = "Soplarlo"
        _data[8] = "0"
        _data[-2] = "0"
        _test(*_data)

    def test_register_activity_invalid(self):
        """Testea el registro de una actividad inválida"""
        self._login_manager()

        def _test(
            action_type: str,
            action_name: str,
            charge_person: str,
            activity: str,
            start_date: str,
            deadline: str,
            work_hours: str,
            n_people: str,
            cost_people: str,
            material_category: str,
            description: str,
            n_material: str,
            cost_material: str,
            unit: str,
            error_message: str,
        ):
            self._register_activity(
                action_type,
                action_name,
                charge_person,
                activity,
                start_date,
                deadline,
                work_hours,
                n_people,
                cost_people,
                material_category,
                description,
                n_material,
                cost_material,
                unit,
            )
            self.assertEqual(
                self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
                error_message,
            )
            if error_message != "Ya existe una actividad con la misma descripción.":
                self.assertNotIn(activity, self.driver.page_source)

        _data = data.copy()

        # Datos de actividad duplicada
        _data[3] = "Preparar el material"
        _test(*_data, "Ya existe una actividad con la misma descripción.")

        # Rango de fechas fuera del proyecto
        msg = "Las fechas de inicio y finalización deben estar en el rango de fechas del detalle de proyecto."
        _data[0] = "Nueva acción"
        _data[1] = "Secado"
        _data[3] = "Secar puertas"
        _data[4] = "04/20/2020"
        _data[5] = "04/20/2022"
        _test(*_data, msg)

        _data[4] = "04/20/2022"
        _data[5] = "04/20/2024"
        _test(*_data, msg)

        _data[4] = "04/20/2020"
        _data[5] = "04/20/2024"
        _test(*_data, msg)

        # Start date > deadline
        _data[4] = "04/20/2022"
        _data[5] = "03/20/2022"
        _test(*_data, "La fecha de inicio no puede ser mayor que la fecha de cierre.")

        # Costo de mano de obra negativo
        _data[5] = "05/21/2022"
        _data[-6] = "-1"
        _test(*_data, "El costo de talento humano debe ser mayor o igual a 0.")

        # Costo de material negativo
        _data[-6] = "0"
        _data[-2] = "-1"
        _test(
            *_data, "El costo de materiales y suministros debe ser mayor o igual a 0."
        )

    def test_edit_activity_valid(self):
        """Testea la edición de una actividad válida"""
        self._login_manager()

        # Datos de actividad válidos
        def _test(
            action_name: str,
            charge_person: str,
            activity: str,
            start_date: str,
            deadline: str,
            work_hours: str,
            n_people: str,
            cost_people: str,
            material_category: str,
            description: str,
            n_material: str,
            cost_material: str,
            unit: str,
        ):
            self._edit_activity(
                action_name,
                charge_person,
                activity,
                start_date,
                deadline,
                work_hours,
                n_people,
                cost_people,
                material_category,
                description,
                n_material,
                cost_material,
                unit,
            )
            self.assertEqual(
                self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
                "Actividad editada exitosamente",
            )
            self.assertIn(activity, self.driver.page_source)

        _data = data2.copy()

        # Datos de actividad válidos con accion existente
        _test(*_data)

    def test_edit_activity_invalid(self):
        """Testea la edición de una actividad inválida"""
        self._login_manager()

        # Datos de actividad válidos
        def _test(
            action_name: str,
            charge_person: str,
            activity: str,
            start_date: str,
            deadline: str,
            work_hours: str,
            n_people: str,
            cost_people: str,
            material_category: str,
            description: str,
            n_material: str,
            cost_material: str,
            unit: str,
            error_message: str,
        ):
            self._edit_activity(
                action_name,
                charge_person,
                activity,
                start_date,
                deadline,
                work_hours,
                n_people,
                cost_people,
                material_category,
                description,
                n_material,
                cost_material,
                unit,
            )
            self.assertEqual(
                self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
                error_message,
            )
            self.assertNotIn(activity, self.driver.page_source)

        _data = data2.copy()

        # Rango de fechas fuera del proyecto
        msg = "Las fechas de inicio y finalización deben estar en el rango de fechas del detalle de proyecto."
        _data[2] = "Secar puertas"
        _data[3] = "04/20/2020"
        _data[4] = "04/20/2022"
        _test(*_data, msg)

        _data[3] = "04/20/2022"
        _data[4] = "04/20/2024"
        _test(*_data, msg)

        _data[3] = "04/20/2020"
        _data[4] = "04/20/2024"
        _test(*_data, msg)

        # Start date > deadline
        _data[3] = "04/20/2022"
        _data[4] = "03/20/2022"
        _test(*_data, "La fecha de inicio no puede ser mayor que la fecha de cierre.")

        # Costo de mano de obra negativo
        _data[4] = "05/21/2022"
        _data[-6] = "-1"
        _test(*_data, "El costo de talento humano debe ser mayor o igual a 0.")

        # Costo de material negativo
        _data[-6] = "0"
        _data[-2] = "-1"
        _test(
            *_data, "El costo de materiales y suministros debe ser mayor o igual a 0."
        )

    def test_delete_activity(self):
        """Testea la eliminación de una actividad de forma válida."""
        self._login_manager()

        self.driver.find_element(By.CSS_SELECTOR, "#delete0 > .table-button").click()

        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "#delete-action-plan-modal .modal-header")
            )
        )

        # Cancela la eliminación
        self.driver.find_element(
            By.CSS_SELECTOR, ".modal-footer:nth-child(3) > .btn"
        ).click()

        self.assertIn(
            "Preparar el material",
            self.driver.find_element(By.CSS_SELECTOR, ".table").text,
        )

        self.driver.find_element(By.CSS_SELECTOR, "#delete0 > .table-button").click()

        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "#delete-action-plan-modal .modal-header")
            )
        )

        self.driver.find_element(By.CSS_SELECTOR, ".btn-danger").click()

        WebDriverWait(self.driver, 1).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, ".toast-body")
            )
        )

        self.assertEqual(
            self.driver.find_element(By.CSS_SELECTOR, ".toast-body").text,
            "Actividad eliminada exitosamente",
        )

        self.assertEqual(
            "No se encontraron planes de acción para el proyecto",
            self.driver.find_element(By.CSS_SELECTOR, ".alert").text,
        )
