from flask import Flask
from config import Config
#from flask_migrate import Migrate
from auth.extensions import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    #migrate.init_app(app, db)
    from .models.user import User
    with app.app_context():
        db.create_all()

    from auth.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
