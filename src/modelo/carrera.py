from sqlalchemy import Column, Integer, Boolean, String, DateTime
from sqlalchemy.orm import relationship

from .declarative_base import Base

class Carrera(Base):
    __tablename__ = 'carrera'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    terminada = Column(Boolean)
    competidores = relationship('Competidor', cascade='all, delete, delete-orphan')
    apuestas = relationship('Apuesta')