from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.user import User
from app.services.AuthService import AuthService
from app.utils.errors.CustomException import CustomException
from app.models.user_roles import UserRoles
from app.routes.auth import token_required

user_bp = Blueprint('user', __name__)

@user_bp.route('/update/<int:user_id>', methods=['PUT'])
def update_user(current_user, user_id):
    """
    Endpoint para actualizar los detalles de un usuario.
    Solo un admin puede cambiar el rol de un usuario.
    """
    data = request.get_json()

    try:
        # Actualización de usuario
        updated_user = User.update_user(
            user_id=user_id,
            username=data.get('username'),
            fullname=data.get('fullname'),
            email=data.get('email'),
            password=data.get('password'),
            role=data.get('role'),
            current_user=current_user  # Verificar permisos de actualización de rol
        )

        return jsonify({
            "message": "Usuario actualizado con éxito",
            "user": updated_user.to_dict()
        }), 200

    except CustomException as ex:
        return jsonify({"message": str(ex)}), 400

    except Exception as ex:
        return jsonify({"message": "Ocurrió un error", "error": str(ex)}), 500

@user_bp.route('/list', methods=['GET'])
def list_users():
    """
    Endpoint para listar todos los usuarios. 
    Solo un admin puede acceder a esta ruta.
    """

    try:
        # Obtener todos los usuarios
        users = User.query.all()
        users_data = [user.to_dict() for user in users]

        return jsonify({
            "message": "Lista de usuarios",
            "users": users_data
        }), 200

    except Exception as ex:
        return jsonify({"message": "Ocurrió un error al obtener la lista de usuarios", "error": str(ex)}), 500