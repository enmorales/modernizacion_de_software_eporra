from src.modelo.carrera import Carrera
from src.modelo.competidor import Competidor
from src.modelo.apostador import Apostador
from src.modelo.apuesta import Apuesta
from src.modelo.declarative_base import session

class ApuestaDAO:
    def get_apuestas_by_carrera(self, carrera_id):
        lista_apuestas = []
        apuestas = session.query(Apuesta).filter(Apuesta.carrera_id == carrera_id).all()
        for apuesta in apuestas:
            carrera = session.query(Carrera).get(apuesta.carrera_id)
            competidor = session.query(Competidor).get(apuesta.competidor_id)
            apostador = session.query(Apostador).get(apuesta.apostador_id)
            lista_apuestas.append({'id': apuesta.id, 'Apostador': apostador.nombre, 'Carrera': carrera.nombre, 'Valor': apuesta.valor, 'Competidor': competidor.nombre})
        return lista_apuestas

    def create_apuesta(self, carrera_id, apostador_id, competidor_id, valor):
        if not (self.validar_datos_apuesta(apostador_id, competidor_id, valor)):
            return False

        carrera = session.query(Carrera).get(carrera_id)
        if len(carrera.competidores) < 2:
            return False

        apuesta = Apuesta(carrera_id=carrera_id, apostador_id=apostador_id, competidor_id=competidor_id, valor=valor)
        session.add(apuesta)
        session.commit()
        return True

    def editar_apuesta(self, apuesta_id, carrera_id, apostador_id, competidor_id, valor):
        if not (self.validar_datos_apuesta(apostador_id, competidor_id, valor)):
            return False

        apuesta = session.query(Apuesta).get(apuesta_id)
        apuesta.carrera_id = carrera_id
        apuesta.apostador_id = apostador_id
        apuesta.competidor_id = competidor_id
        apuesta.valor = valor
        session.add(apuesta)
        session.commit()
        return True

    def validar_datos_apuesta(self, apostador_id, competidor_id, valor):
        if apostador_id is None or competidor_id is None or valor is None or valor == '':
            return False

        valor = float(valor)
        if valor <= 0:
            return False

        return True
