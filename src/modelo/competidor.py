from sqlalchemy import Column, Integer, Float, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship

from .declarative_base import Base

class Competidor(Base):
    __tablename__ = 'competidor'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    probabilidad = Column(Float)
    cuota = Column(Float)
    ganador = Column(Boolean)
    carrera = Column(Integer, ForeignKey('carrera.id'))