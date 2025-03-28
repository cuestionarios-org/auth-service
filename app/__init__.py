from flask import Flask, jsonify
from sqlalchemy import create_engine, text
from app.config import config_dict
from app.extensions import db, migrate
from app.routes.auth import auth_bp
from app.routes.users import user_bp
from app.utils.commands.cli import init_db
from app.utils.errors.handlers import register_error_handlers
import os
import subprocess
from flask_migrate import upgrade

def create_app(config_name='development'):
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
                except Exception as e:
                    print(f"❌ Error al aplicar migraciones: {e}")

            # # 🔥 Ejecutar migraciones automáticamente
            # print("📌 Ejecutando migraciones...")
            # try:
            #     subprocess.run(["flask", "db", "upgrade"], check=True)
            #     print("✅ Migraciones aplicadas correctamente.")
            # except subprocess.CalledProcessError as e:
            #     print(f"❌ Error al aplicar migraciones: {e}")