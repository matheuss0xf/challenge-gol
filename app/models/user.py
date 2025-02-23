from sqlalchemy import Column, String

from app.database.connection import Base


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
