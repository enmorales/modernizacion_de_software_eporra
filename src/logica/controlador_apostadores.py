from cmath import isnan, nan
from datetime import datetime
from collections import defaultdict
from pyparsing import empty

from src.modelo.declarative_base import engine, Base, session

from src.modelo.carrera import Carrera  # Missing import
from src.modelo.competidor import Competidor
from src.modelo.apostador import Apostador
from src.modelo.apuesta import Apuesta

class ControladorApostadores():
    def __init__(self):
        Base.metadata.create_all(engine)

    def dar_apostadores(self):
        lista_apostadores = []
        apostadores = session.query(Apostador).order_by(Apostador.nombre).all()
        for apostador in apostadores:
            lista_apostadores.append({'id': apostador.id, 'nombre': apostador.nombre})
        return lista_apostadores

    def crear_apostador(self, nombre):
        if nombre == "" or len(nombre) > 200:
            return False
        existeApostador = session.query(Apostador).filter(Apostador.nombre == nombre).all()
        if len(existeApostador) > 0:
            return False

        apostador = Apostador(nombre=nombre)
        session.add(apostador)
        session.commit()
        return True

    def editar_apostador(self, id, nombre):
        if nombre == "" or len(nombre) > 200:
            return False

        apostador = session.query(Apostador).get(id)
        existeApostador = session.query(Apostador).filter(Apostador.nombre == nombre).first()
        if existeApostador is not None and id != existeApostador.id:
            return False

        apostador.nombre = nombre
        session.add(apostador)
        session.commit()

        return True

    def dar_apostadores_apuestas(self, id_carrera):
        apuestas = session.query(Apuesta).filter(Apuesta.carrera_id == id_carrera).all()
        lista_apostadores = []
        for apuesta in apuestas:
            apostador = session.query(Apostador).filter(Apostador.id == apuesta.apostador_id).first()
            lista_apostadores.append({'id': apostador.id, 'nombre': apostador.nombre, 'apuesta': apuesta.valor, 'competidor_id': apuesta.competidor_id})

        return lista_apostadores
