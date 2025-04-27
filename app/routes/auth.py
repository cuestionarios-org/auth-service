from flask import Blueprint, request, jsonify
from app.services.AuthService import AuthService
import jwt
import datetime
from functools import wraps
from app.config import Config
from app.utils.errors.decorators import with_context_error

auth_bp = Blueprint('auth', __name__)

def token_required(f):
    """
    Decorador para verificar el token JWT y cargar el usuario actual.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"message": "Token no proporcionado."}), 401

        try:
            token = auth_header.split("Bearer ")[1]
            payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
            current_user = AuthService.get_user_by_id(payload['user_id'])
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as jwt_error:
            return jsonify({"message": "Token inválido o expirado.", "error": str(jwt_error)}), 401
        except Exception as e:
            return jsonify({"message": "Error de autenticación.", "error": str(e)}), 401

        return f(current_user, *args, **kwargs)

    return decorated

def serialize_user(user):
    """
    Helper para extraer solo los campos públicos de un usuario.
    """
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role
    }

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Endpoint para registrar un nuevo usuario.
    """
    return handle_register()

@with_context_error(context="Register_AuthController")
def handle_register():
    data = request.get_json()

    result = AuthService.register_user(
        username=data['username'],
        fullname=data.get('fullname', ""),  # fullname opcional
        email=data['email'],
        password=data['password'],
    )

    return jsonify({
        "message": "Usuario creado con éxito",
        "access_token": result['token'],
        "user": serialize_user(result['user'])
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint para autenticar usuarios.
    """
    return handle_login()

@with_context_error(context="Login_AuthController")
def handle_login():
    data = request.get_json()

    result = AuthService.login_user(
        email=data['email'],
        password=data['password']
    )

    return jsonify({
        "access_token": result['token'],
        "user": serialize_user(result['user'])
    }), 200

@auth_bp.route('/me', methods=['GET'])
@token_required
def me(current_user):
    """
    Endpoint para obtener los detalles del usuario autenticado.
    """
    return jsonify(serialize_user(current_user))

@auth_bp.route('/protected', methods=['GET'])
@token_required
def protected(current_user):
    """
    Endpoint protegido con JWT.
    """
    return jsonify({
        "message": f"Bienvenido, {current_user.username}!",
        "fullname": current_user.fullname,
        "email": current_user.email,
        "role": current_user.role
    })
