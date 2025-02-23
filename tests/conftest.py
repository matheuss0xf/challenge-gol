import pytest

from app.database.connection import DBConnectionHandler
from app.models.user import UserModel


@pytest.fixture(scope='module')
def db_session():
    db = DBConnectionHandler()
    db.create_all()  # Cria as tabelas no banco de dados
    yield db
    db.drop_all()  # Limpa o banco de dados após os testes


@pytest.fixture
def user(db_session):
    # Cria um usuário de teste no banco de dados
    user = UserModel(id='123', name='João Silva', email='joao@example.com', password='hashed_password')
    db_session.session.add(user)
    db_session.session.commit()
    return user
