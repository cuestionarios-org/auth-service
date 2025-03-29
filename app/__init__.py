from flask import Flask, jsonify
from sqlalchemy import create_engine, text
from app.config import config_dict
from app.extensions import db, migrate
from app.routes.auth import auth_bp
from app.routes.users import user_bp
from app.utils.commands.cli import init_db
from app.utils.errors.handlers import register_error_handlers
import os
from flask_migrate import upgrade
from app.models.user import User, UserRoles

def create_app(config_name='development'):
    print(f"📌 Iniciando ...")

    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])
    
    

    db.init_app(app)
    migrate.init_app(app, db)

    # Intentar crear la base de datos si no existe
    create_database_if_not_exists(app)
    
    # Registra comandos personalizados
    app.cli.add_command(init_db)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/users')
    
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Welcome to the Flask application!',
            'status': 'success',
            'documentation': '/docs'  # Ejemplo de ruta de documentación
        })
    
    # Registra manejadores de errores
    register_error_handlers(app)
    
    return app

def create_database_if_not_exists(app):
    """Crea la base de datos en PostgreSQL si no existe"""
    db_url = app.config["SQLALCHEMY_DATABASE_URI"]
    
    # Conectar a la base `postgres` en lugar de la que aún no existe
    temp_db_url = db_url.rsplit("/", 1)[0] + "/postgres"
    engine = create_engine(temp_db_url, isolation_level="AUTOCOMMIT")  # 🔥 Se agrega `isolation_level="AUTOCOMMIT"`

    with engine.connect() as connection:
        db_name = os.getenv('AUTH_POSTGRES_DB')
        result = connection.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'"))
        exists = result.scalar()
        
        if not exists:
            print(f"📌 Creando la base de datos {db_name}...")
            connection.execute(text(f"CREATE DATABASE {db_name}"))
            print(f"✅ Base de datos {db_name} creada exitosamente.")

            # 🔥 Ejecutar migraciones usando Flask Migrate directamente
            print("📌 Ejecutando migraciones...")
            with app.app_context():
                try:
                    upgrade()
                    print("✅ Migraciones aplicadas correctamente.")
                    # Insertar usuarios con cada rol
                    print("📌 Creando usuarios predeterminados...")
                    seed_users()
                    print("✅ Usuarios predeterminados creados.")
                except Exception as e:
                    print(f"❌ Error al aplicar migraciones: {e}")
        else:
            print(f"✅ La base de datos {db_name} ya existe.")

def seed_users():
    """Inserta usuarios con cada rol en la base de datos."""
    users = [
        {"username": "admin", "email": "admin@example.com", "password": "admin123", "role": UserRoles.ADMIN},
        {"username": "tutor", "email": "tutor@example.com", "password": "tutor123", "role": UserRoles.TUTOR},
        {"username": "docente", "email": "docente@example.com", "password": "docente123", "role": UserRoles.DOCENTE},
        {"username": "alumno", "email": "alumno@example.com", "password": "alumno123", "role": UserRoles.ALUMNO},
        {"username": "usuario", "email": "usuario@example.com", "password": "usuario123", "role": UserRoles.USUARIO},
    ]

    for user_data in users:
        existing_user = User.query.filter_by(email=user_data["email"]).first()
        if not existing_user:
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                role=user_data["role"]
            )
            user.set_password(user_data["password"])
            db.session.add(user)

    db.session.commit()