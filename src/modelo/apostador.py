from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .declarative_base import Base

class Apostador(Base):
    __tablename__ = 'apostador'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)