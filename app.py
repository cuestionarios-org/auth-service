from flask import Flask, jsonify
from config import config_dict
from extensions import db, migrate
from routes.auth import auth_bp
from routes.users import user_bp

from utils.errors.handlers import register_error_handlers

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])
    
    db.init_app(app)
    migrate.init_app(app, db)

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

if __name__ == '__main__':
    import os
    env = os.getenv('FLASK_ENV', 'development')
    app = create_app(env)
    # app.run(port=5001)
    app.run(host='0.0.0.0', port=5001)

