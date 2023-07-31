
from flask_restful import Resource
from flask import request, send_file, send_from_directory
from ..modelos import Apostador
from ..logica.controlador_apostadores import ControladorApostadores

controlador_apostadores = ControladorApostadores()

class VistaApostadores(Resource):

    def get(self):
        self.apostadores = []
        for apostador in controlador_apostadores.dar_apostadores(): 
            self.apostadores.append({'id':apostador['id'], 'Nombre':apostador['nombre']})

        return self.apostadores.copy()
    def post(self):
        nombre = request.json["nombre"]
        response = controlador_apostadores.crear_apostador(nombre=nombre)
        return response, 200
    
class VistaApostador(Resource):

    def post(self, id_apostador):
        nombre = request.json["nombre"]
        return controlador_apostadores.editar_apostador(id=id_apostador, nombre=nombre)
    
    def delete(self, id_apostador):
        response = controlador_apostadores.eliminar_apostador(id_apostador)
        return response, 200


class HelloWorld(Resource):
    def get(self):
        return {"hello":"world"}, 200

class VistaCheck(Resource):
    def get(self):
        return "ok", 200

class VistaCheckR(Resource):
    def get(self):
        return "ok", 200
         

