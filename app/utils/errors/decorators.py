from functools import wraps
from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.utils.errors.CustomException import BusinessError, CustomException

def handle_db_errors(context="Usuarios", code=500):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except SQLAlchemyError as e:
                db.session.rollback()
                raise CustomException(
                    message=f"Error en la base de datos ({context})",
                    code=code
                ) from e
        return wrapper
    return decorator

def with_context_error(context="General", code=500):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except CustomException:
                raise  # Dejá pasar errores ya formateados
            except Exception as e:
                raise CustomException(
                    message=f"Error inesperado en {context}",
                    code=code
                )
        return wrapper
    return decorator