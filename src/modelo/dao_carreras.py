from src.modelo.carrera import Carrera
from src.modelo.competidor import Competidor
from src.modelo.apostador import Apostador
from src.modelo.apuesta import Apuesta
from src.modelo.declarative_base import session
from collections import defaultdict

class CarreraDAO:
    def get_all_carreras(self):
        carreras_registradas = session.query(Carrera).order_by(Carrera.nombre).all()
        carreras = []
        for item in carreras_registradas:
            competidores_map = [{'id': competidor.id, 'nombre': competidor.nombre, 'probabilidad': competidor.probabilidad} for competidor in item.competidores]
            carrera = {'id': item.id, 'nombre': item.nombre, 'competidores': competidores_map, 'terminada': item.terminada}
            carreras.append(carrera)
        return carreras

    def create_carrera(self, nombre, competidores):
        if not self.validar_nombre(nombre) or self.existe_carrera(nombre) or not self.validar_competidores(competidores):
            return False

        try:
            carrera = Carrera(nombre=nombre, terminada=False)
            session.add(carrera)

            cuotas = [1 / comp['probabilidad'] - 1 if comp['probabilidad'] > 0 else float('inf') for comp in competidores]
            competidores_obj = [Competidor(nombre=comp['nombre'], carrera=carrera.id, probabilidad=comp['probabilidad'], cuota=cuota, ganador=False) for comp, cuota in zip(competidores, cuotas)]
            session.add_all(competidores_obj)

            session.commit()
            return True

        except:
            session.rollback()
            return False

    def validar_nombre(self, nombre):
        return nombre and len(nombre) <= 200

    def existe_carrera(self, nombre):
        return session.query(Carrera).filter(Carrera.nombre == nombre).count() > 0

    def validar_competidores(self, competidores):
        if len(competidores) < 2 or sum(comp['probabilidad'] for comp in competidores) != 1:
            return False

        competidores_map = defaultdict(int)
        for competidor in competidores:
            if not self.es_competidor_valido(competidor) or competidores_map[competidor['nombre']] > 0:
                return False
            competidores_map[competidor['nombre']] += 1

        return True

    def es_competidor_valido(self, competidor):
        return isinstance(competidor.get('nombre'), str) and 0 <= competidor.get('probabilidad', 0) <= 1

    def terminar_carrera(self, id_carrera, id_competidor_ganador):
        carrera = session.query(Carrera).get(id_carrera)
        carrera.terminada = True
        session.add(carrera)

        competidor = session.query(Competidor).get(id_competidor_ganador)
        competidor.ganador = True
        session.add(competidor)

        session.commit()

        return True

    def dar_reporte_ganancias(self, id_carrera, id_competidor_ganador):
        self.terminar_carrera(id_carrera, id_competidor_ganador)
        apostadores_carrera = self.dar_apostadores_apuestas(id_carrera)

        apostadores = []
        ganancia_casa = 0
        competidor_ganador = self.dar_competidor_ganador(id_competidor_ganador)
        for apostador in apostadores_carrera:
            ganancia = 0
            apuesta = apostador['apuesta']
            if apostador['competidor_id'] == id_competidor_ganador:
                ganancia = apuesta + (apuesta / competidor_ganador.cuota)
            apostadores.append((apostador['nombre'], ganancia))
            ganancia_casa += apuesta - ganancia
        return apostadores, ganancia_casa

    def dar_apuestas_carrera(self, carrera_id):
        lista_apuestas = []
        apuestas = session.query(Apuesta).filter(Apuesta.carrera_id == carrera_id).all()
        for apuesta in apuestas:
            carrera = session.query(Carrera).get(apuesta.carrera_id)
            competidor = session.query(Competidor).get(apuesta.competidor_id)
            apostador = session.query(Apostador).get(apuesta.apostador_id)
            lista_apuestas.append({'id': apuesta.id, 'Apostador': apostador.nombre, 'Carrera': carrera.nombre, 'Valor': apuesta.valor, 'Competidor': competidor.nombre})
        return lista_apuestas

    def borrar_carrera(self, carrera_id):
        carrera = session.query(Carrera).get(carrera_id)
        if len(carrera.apuestas) == 0:
            session.delete(carrera)
            session.commit()
            return True
        return False
