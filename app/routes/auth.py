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
@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Endpoint para registrar un nuevo usuario.
    """
    return handle_register()

@with_context_error(context="Register_AuthController")
def handle_register():
    
    data = request.get_json()

    new_user = AuthService.register_user(
        username=data['username'],
        fullname=data.get('fullname', ""),  # Maneja fullname como opcional
        email=data['email'],
        password=data['password'],
    )
    return jsonify({
        "message": "Usuario creado con éxito",
        "user": new_user.to_dict()
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    return handle_login()

@with_context_error(context="Login_AuthController")
def handle_login():
    """
    Endpoint para autenticar usuarios.
    """
    data = request.get_json()

    authenticated_user = AuthService.login_user(email=data['email'], password=data['password'])

    if authenticated_user:
        token = jwt.encode(
            {
                'user_id': authenticated_user.id,
                'user_name': authenticated_user.username,
                'role': authenticated_user.role,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
            },
            Config.JWT_SECRET_KEY,
            algorithm="HS256"
        )
        # Convertir el user a dict y seleccionar solo los campos que queremos devolver
        user_data = authenticated_user.to_dict()
        filtered_user_data = {
            "id": user_data["id"],
            "username": user_data["username"],
            "email": user_data["email"],
            "role": user_data["role"]
        }

        return jsonify({
            "access_token": token,
            "user": filtered_user_data
        }), 200
    return jsonify({"message": "Credenciales inválidas"}), 401

# ruta para /me
@auth_bp.route('/me', methods=['GET'])
@token_required
def me(current_user):
    """
    Endpoint para obtener los detalles del usuario autenticado.
    """
    return jsonify({
        "id": current_user.id,
        "username": current_user.username,
        "fullname": current_user.fullname,
        "email": current_user.email,
        "role": current_user.role
    })

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
