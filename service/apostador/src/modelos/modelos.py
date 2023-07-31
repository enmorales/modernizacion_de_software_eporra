from email.policy import default
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
""" from connection_gcp import connect_with_connector """
""" from app import db """
    
db = SQLAlchemy()

class Apostador(db.Model):
    __tablename__ = 'apostador'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)

class Apuesta(db.Model):
    __tablename__ = 'apuesta'

    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float)
    carrera_id = db.Column(db.Integer, db.ForeignKey('carrera.id'), nullable=False)
    competidor_id = db.Column(db.Integer,db.ForeignKey('competidor.id'), nullable=False)
    apostador_id = db.Column(db.Integer, db.ForeignKey('apostador.id'), nullable=False)