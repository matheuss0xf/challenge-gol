import logging
import uuid

from app.database.connection import DBConnectionHandler
from app.models.user import UserModel


class AuthRepository:
    @staticmethod
    def find_user_by_email(email):
        try:
            with DBConnectionHandler() as db:
                return db.session.query(UserModel).filter_by(email=email).first()
        except Exception as e:
            logging.error(f'Erro ao buscar usuário por email: {e}')
            raise

    @staticmethod
    def create_user(name, email, password):
        try:
            user_id = uuid.uuid4().hex
            new_user = UserModel(id=user_id, name=name, email=email, password=password)

            with DBConnectionHandler() as db:
                db.session.add(new_user)
                db.session.commit()
        except Exception as e:
            logging.error(f'Erro ao criar usuário: {e}')
            raise

    @staticmethod
    def check_user_credentials(email, password):
        try:
            with DBConnectionHandler() as db:
                user = db.session.query(UserModel).filter_by(email=email).first()
                if user:
                    return {'id': user.id, 'name': user.name, 'email': user.email}
            return None
        except Exception as e:
            logging.error(f'Erro ao verificar credenciais do usuário: {e}')
            raise
