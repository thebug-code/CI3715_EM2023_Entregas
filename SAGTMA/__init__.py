import os
from flask import Flask


def create_app(test_config=None):
    """Crea y configura la aplicación"""
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
