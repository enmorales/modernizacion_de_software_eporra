from .modelos import db, Apostador

class ApostadorDAO:
    def get_apostador_by_id(self, id):
        return db.session.query(Apostador).get(id)

    def get_apostador_by_nombre(self, nombre):
        return db.session.query(Apostador).filter(Apostador.nombre == nombre).first()

    def create_apostador(self, nombre):
        apostador = Apostador(nombre=nombre)
        db.session.add(apostador)
        db.session.commit()
        return apostador

    def update_apostador(self, apostador):
        db.session.add(apostador)
        db.session.commit()

    def get_all_apostadores(self):
        apostadores = db.session.query(Apostador).order_by(Apostador.nombre).all()
        return [{'id': apostador.id, 'nombre': apostador.nombre} for apostador in apostadores]
