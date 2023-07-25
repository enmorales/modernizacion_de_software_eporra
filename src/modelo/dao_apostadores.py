from src.modelo.apostador import Apostador
from src.modelo.declarative_base import session

class ApostadorDAO:
    def get_apostador_by_id(self, id):
        return session.query(Apostador).get(id)

    def get_apostador_by_nombre(self, nombre):
        return session.query(Apostador).filter(Apostador.nombre == nombre).first()

    def create_apostador(self, nombre):
        apostador = Apostador(nombre=nombre)
        session.add(apostador)
        session.commit()
        return apostador

    def update_apostador(self, apostador):
        session.add(apostador)
        session.commit()

    def get_all_apostadores(self):
        apostadores = session.query(Apostador).order_by(Apostador.nombre).all()
        return [{'id': apostador.id, 'nombre': apostador.nombre} for apostador in apostadores]
