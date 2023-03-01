import unittest

from SAGTMA import create_app


class BaseTestClass(unittest.TestCase):
    def setUp(self):
        # Crea la aplicación y un cliente para las pruebas
        self.app = create_app(test_config={
            'TESTING': True,
            'DEBUG': True,
            'APP_ENV': 'testing',
            'DATABASE_NAME': 'SAGTMA_test',
            'SQLALCHEMY_TRACK_MODIFICATIONS': False
        })
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

        # Puebla la base de datos para el conjunto de tests, si es necesario
        if hasattr(self, 'populate_db'):
            self.populate_db()

    def tearDown(self):
        # Elimina todas las tablas de la base de datos
        from SAGTMA.models import db
        db.drop_all()

        # Elimina el contexto de la aplicación
        self.ctx.pop()