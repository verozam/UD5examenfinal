from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate  # Importar Migrate
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()  # Instancia de Migrate

def create_app():
    app = Flask(__name__)
    csrf = CSRFProtect(app)

    # Configuración de la aplicación (como ya lo tienes)
    app.config['SECRET_KEY'] = 'task_2025_esti'  
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)  # Inicia Migrate con la app y la base de datos

    # Importar modelos dentro de la función create_app
    from .models import User, Task  # Ahora importa aquí después de que la app esté inicializada

    login_manager.login_view = 'main.login'

    # Aquí definimos el user_loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Busca al usuario por ID

    from .routes import main
    app.register_blueprint(main)

    return app
