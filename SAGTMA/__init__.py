import os
from flask import Flask


def flask_app(test_config=None):
    """Crea y configura una aplicación de flask"""
    # Crea la app
    app = Flask(__name__, instance_relative_config=True)

    # Configura la app
    app.config.from_mapping(
        # Genera bits aleatorios para la clave secreta
        SECRET_KEY="una_clave_muy_secreta",
        # Habilita el modo de depuración
        DEBUG=True,
        # Configuración de la base de datos
        DATABASE_NAME="SAGTMA",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is not None:
        # Carga el archivo de confifuración pasado por argumento, si existe
        app.config.from_mapping(test_config)

    # Configura la base de datos
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        app.instance_path, f'{app.config["DATABASE_NAME"]}.sqlite'
    )

    # Asegura que exista el directorio de la instancia
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():
        # Registra las vistas
        from SAGTMA.routes import (
            home,
            auth,
            errors,
            admin,
            manager,
            api,
            analyst,
        )

        # Registra los comandos
        from SAGTMA import commands

        # Inicializa la base de datos
        from SAGTMA.models import db

        db.init_app(app)
        db.create_all()

    return app


def create_app():
    """Crea y configura la aplicación principal de flask

    Se ejecuta cuando se ejecuta el comando `flask --app SAGTMA --debug run`
    """
    return flask_app()


def test_app():
    """Crea y configura la aplicación para pruebas.

    Se ejecuta con el comando `flask --app SAGTMA:test_app run` --host:5001
    """
    return flask_app(
        test_config={
            "TESTING": True,
            "DEBUG": True,
            "APP_ENV": "testing",
            "DATABASE_NAME": "SAGTMA_test",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )
