from app.extensions import db
from app.models.user import User
from app.utils.errors.CustomException import ValidationError
from app.utils.errors.decorators import handle_db_errors, with_context_error
from sqlalchemy import or_

class AuthService:
    @classmethod
    @with_context_error(context="Login_User_AuthService")
    @handle_db_errors(context="Login_User_AuthService")
    def login_user(cls, email, password):
        user = User.query.filter_by(email=email, is_active=True).first()
        if user and user.check_password(password):
            return user
        raise ValidationError("Credenciales inválidas")


    @classmethod
    @with_context_error(context="Register_User_AuthService")
    @handle_db_errors(context="Register_User_AuthService")
    def register_user(cls, username, fullname, email, password):
        
        existing_user = User.query.filter(
            or_(User.email == email, User.username == username)
        ).first()

        if existing_user:
            if existing_user.email == email:
                raise ValidationError("El email ya está registrado.")
            if existing_user.username == username:
                raise ValidationError("El nombre de usuario ya está registrado.")

        fullname = fullname or ""
        user = User(username=username, fullname=fullname, email=email, role="usuario")

        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    @with_context_error(context="GetUserById_AuthService")
    @handle_db_errors(context="GetUserById_AuthService")
    def get_user_by_id(cls, user_id):
        user = User.query.get(user_id)
        if not user:
            raise ValidationError("Usuario no encontrado.")
        return user
