from sqlalchemy import Column, Integer, Numeric, String

from app.database.connection import Base


class FlightModel(Base):
    __tablename__ = 'flights'

    id = Column(String, primary_key=True)
    ano = Column(Integer, nullable=False)
    mes = Column(Integer, nullable=False)
    mercado = Column(String(20), nullable=False)
    rpk = Column(Numeric, nullable=False)
