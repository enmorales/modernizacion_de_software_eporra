from cmath import isnan, nan
from datetime import datetime
from collections import defaultdict
from pyparsing import empty

from src.modelo.declarative_base import engine, Base, session

from src.modelo.carrera import Carrera  # Missing import
from src.modelo.competidor import Competidor
from src.modelo.apostador import Apostador
from src.modelo.apuesta import Apuesta
from src.modelo.dao_apuestas import ApuestaDAO

class ControladorApuestas():
    def __init__(self):
        Base.metadata.create_all(engine)
        self.apuesta_dao = ApuestaDAO()

    def dar_apuestas_carrera(self, carrera_id):
        return self.apuesta_dao.get_apuestas_by_carrera(carrera_id)

    def crear_apuesta(self, carrera_id, apostador_id, competidor_id, valor):
        return self.apuesta_dao.create_apuesta(carrera_id, apostador_id, competidor_id, valor)

    def editar_apuesta(self, apuesta_id, carrera_id, apostador_id, competidor_id, valor):
        return self.apuesta_dao.editar_apuesta(apuesta_id, carrera_id, apostador_id, competidor_id, valor)