from cmath import isnan, nan
from datetime import datetime
from collections import defaultdict
from pyparsing import empty

from ..modelos import Apuesta
from ..modelos.dao_apostadores import ApostadorDAO

class ControladorApostadores():
    def __init__(self):
        self.apostador_dao = ApostadorDAO()

    def dar_apostadores(self):
        return self.apostador_dao.get_all_apostadores()

    def crear_apostador(self, nombre):
        if not nombre or len(nombre) > 200:
            return False

        if self.apostador_dao.get_apostador_by_nombre(nombre):
            return False

        apostador = self.apostador_dao.create_apostador(nombre)
        return True

    def editar_apostador(self, id, nombre):
        if not nombre or len(nombre) > 200:
            return False

        apostador = self.apostador_dao.get_apostador_by_id(id)
        if not apostador:
            return False

        existente = self.apostador_dao.get_apostador_by_nombre(nombre)
        if existente and id != existente.id:
            return False

        apostador.nombre = nombre
        self.apostador_dao.update_apostador(apostador)
        return True

    def dar_apostadores_apuestas(self, id_carrera):
        apuestas = self.apostador_dao.session.query(Apuesta).filter(Apuesta.carrera_id == id_carrera).all()
        lista_apostadores = []
        for apuesta in apuestas:
            apostador = self.apostador_dao.get_apostador_by_id(apuesta.apostador_id)
            lista_apostadores.append({'id': apostador.id, 'nombre': apostador.nombre, 'apuesta': apuesta.valor, 'competidor_id': apuesta.competidor_id})

        return lista_apostadores
    
    def eliminar_apostador(self, id_apostador):
        apostador = self.apostador_dao.get_apostador_by_id(id_apostador)
        self.apostador_dao.delete_apostador(apostador)
        return True
        
