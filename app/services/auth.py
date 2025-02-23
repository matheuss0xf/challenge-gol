import logging
from datetime import timedelta

from flask_jwt_extended import create_access_token

from app.repositories.auth import AuthRepository
from app.utils.password import hash_password, verify_password


class AuthService:
    def __init__(self):
        self.repo = AuthRepository()

    def register_user(self, name, email, password):
        if self.repo.find_user_by_email(email):
            logging.warning(f'Tentativa de registro com email já cadastrado: {email}')
            return {'error': 'Erro ao registrar usuário'}

        hashed_password = hash_password(password)

        self.repo.create_user(name, email, hashed_password)

        return {
            'message': 'Usuário registrado com sucesso',
        }

    def authenticate_user(self, email, password):
        user = self.repo.find_user_by_email(email)
        if not user:
            logging.warning(f'Tentativa de login com email não cadastrado: {email}')
            return {'error': 'Credenciais inválidas'}

        if not verify_password(password, user.password):
            logging.warning(f'Tentativa de login com senha incorreta para o email: {email}')
            return {'error': 'Credenciais inválidas'}

        access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=7))

        return {'access_token': access_token, 'user': {'id': user.id, 'name': user.name, 'email': user.email}}
