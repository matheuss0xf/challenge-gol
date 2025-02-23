from unittest.mock import MagicMock, patch

import pytest

from app.models.user import UserModel
from app.services.auth import AuthService


@pytest.fixture
def mock_user():
    return UserModel(id='123', name='User Teste', email='userteste@example.com', password='senha_com_hash')


@patch('app.repositories.auth.AuthRepository.find_user_by_email')
@patch('app.repositories.auth.AuthRepository.create_user')
def test_register_user_success(mock_create_user, mock_find_user_by_email):
    service = AuthService()
    mock_find_user_by_email.return_value = None

    result = service.register_user('User Teste', 'userteste@example.com', 'senha123')

    assert result == {'message': 'Usuário registrado com sucesso'}
    mock_create_user.assert_called_once()


@patch('app.repositories.auth.AuthRepository.find_user_by_email')
def test_register_user_email_already_registered(mock_find_user_by_email):
    mock_find_user_by_email.return_value = MagicMock()
    service = AuthService()
    result = service.register_user('User Teste', 'userteste@example.com', 'senha123')

    assert result == {'error': 'Erro ao registrar usuário'}


@patch('app.repositories.auth.AuthRepository.find_user_by_email')
@patch('app.services.auth.verify_password')
@patch('app.services.auth.create_access_token')
def test_authenticate_user_success(mock_create_access_token, mock_verify_password, mock_find_user_by_email, mock_user):
    # Mockando o comportamento de busca e validação
    mock_find_user_by_email.return_value = mock_user
    mock_verify_password.return_value = True
    mock_create_access_token.return_value = 'access_token_fake'
    service = AuthService()
    result = service.authenticate_user('userteste@example.com', 'senha123')

    assert 'access_token' in result
    assert result['user'] == {'id': '123', 'name': 'User Teste', 'email': 'userteste@example.com'}


@patch('app.repositories.auth.AuthRepository.find_user_by_email')
def test_authenticate_user_invalid_email(mock_find_user_by_email):
    mock_find_user_by_email.return_value = None
    service = AuthService()
    result = service.authenticate_user('userteste@example.com', 'senha123')

    assert result == {'error': 'Credenciais inválidas'}


@patch('app.repositories.auth.AuthRepository.find_user_by_email')
@patch('app.services.auth.verify_password')
def test_authenticate_user_invalid_password(mock_verify_password, mock_find_user_by_email, mock_user):
    mock_find_user_by_email.return_value = mock_user
    mock_verify_password.return_value = False
    service = AuthService()
    result = service.authenticate_user('userteste@example.com', 'senha123')

    assert result == {'error': 'Credenciais inválidas'}
