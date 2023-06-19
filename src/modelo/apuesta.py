from sqlalchemy import Column, Integer, Float, ForeignKey

from .declarative_base import Base

class Apuesta(Base):
    __tablename__ = 'apuesta'

    id = Column(Integer, primary_key=True)
    valor = Column(Float)
    carrera_id = Column(Integer, ForeignKey('carrera.id'), nullable=False)
    competidor_id = Column(Integer, ForeignKey('competidor.id'), nullable=False)
    apostador_id = Column(Integer, ForeignKey('apostador.id'), nullable=False)