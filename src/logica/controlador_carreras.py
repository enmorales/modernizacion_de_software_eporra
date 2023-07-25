from cmath import isnan, nan
from datetime import datetime
from collections import defaultdict
from pyparsing import empty

from src.modelo.declarative_base import engine, Base, session

from src.modelo.carrera import Carrera
from src.modelo.competidor import Competidor
from src.modelo.apostador import Apostador
from src.modelo.apuesta import Apuesta
from src.modelo.dao_carreras import CarreraDAO

class ControladorCarreras():
    def __init__(self):
        Base.metadata.create_all(engine)
        self.carrera_dao = CarreraDAO()

    def dar_carreras(self):
        return self.carrera_dao.get_all_carreras()

    def crear_carrera(self, nombre, competidores):
        return self.carrera_dao.create_carrera(nombre, competidores)

    def terminar_carrera(self, id, competidor_ganador_id):
        return self.carrera_dao.terminar_carrera(id, competidor_ganador_id)

    def dar_reporte_ganancias(self, id_carrera, id_competidor_ganador):
        return self.carrera_dao.dar_reporte_ganancias(id_carrera, id_competidor_ganador)

    def dar_apuestas_carrera(self, carrera_id):
        return self.carrera_dao.dar_apuestas_carrera(carrera_id)

    def borrar_carrera(self, carrera_id):
        return self.carrera_dao.borrar_carrera(carrera_id)
