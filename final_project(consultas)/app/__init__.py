from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    # Importar y registrar blueprints
    from app.auth_routes import auth       # Rutas de autenticación
    from app.routes import main           # Rutas principales (incluye dashboard, usuarios)
    from app.test_routes import main as test_main  # Rutas de prueba/API

    # Registrar los blueprints
    app.register_blueprint(auth)
    app.register_blueprint(main)
    
    # Solo registrar test_routes si estamos en modo desarrollo
    if app.config.get('DEBUG', False):
        app.register_blueprint(test_main)

    return app