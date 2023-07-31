import requests
from src.logica.controlador_carreras import ControladorCarreras
from src.logica.controlador_apuestas import ControladorApuestas
from src.logica.controlador_apostadores import ControladorApostadores

class Logica_mock():

    def __init__(self):
        self.controlador_carreras = ControladorCarreras()
        self.controlador_apuestas = ControladorApuestas()
        self.controlador_apostadores = ControladorApostadores()
        self.carreras = []
        self.url_service = "http://127.0.0.1:5000/api"
        
    def dar_carreras(self):
        self.carreras = []
        for carrera in self.controlador_carreras.dar_carreras().copy(): 
            competidores_map = []
            for competidor in carrera['competidores']:
                competidores_map.append({'id':competidor['id'],'Nombre': competidor['nombre'], 'Probabilidad': competidor['probabilidad']})
            self.carreras.append({'id':carrera['id'],'Nombre':carrera['nombre'],'Competidores':competidores_map,'Abierta':not(carrera['terminada'])})

        return self.carreras

    def dar_carrera(self, id_carrera):
        return self.carreras[id_carrera].copy()
    
    def crear_carrera(self, nombre, competidores):
        competidores_map = [{'nombre': comp['Nombre'], 'probabilidad': comp['Probabilidad']} for comp in competidores]
        carrera_guardada = self.controlador_carreras.crear_carrera(nombre, competidores_map)
        return carrera_guardada

    def editar_carrera(self, id, nombre):
        self.carreras[id]['Nombre'] = nombre

    def terminar_carrera(self, id, ganador):
        self.carreras[id]['Ganador'] = ganador

    def eliminar_carrera(self, id):
        carrera_eliminada = self.controlador_carreras.borrar_carrera(self.carreras[id]['id'])
        return carrera_eliminada

    def dar_apostadores(self):
        response = requests.get(self.url_service+"/apostadores")
        response_json = response.json()
        return response_json

    def aniadir_apostador(self, nombre):
        payload = {"nombre": nombre}
        response = requests.post(self.url_service+"/apostadores", json=payload)
        return response.json()
    
    def editar_apostador(self, id, nombre):
        payload = {"nombre": nombre}
        response = requests.post(self.url_service+"/apostador/"+str(id), json=payload)
        return response.json()
    
    def eliminar_apostador(self, id):
        response = requests.delete(self.url_service+"/apostador/"+str(id), json={})
        return response.json()

    def dar_competidores_carrera(self, id):
        return self.carreras[id]['Competidores'].copy()

    def dar_competidor(self, id_carrera, id_competidor):
        return self.carreras[id_carrera]['Competidores'][id_competidor].copy()

    def aniadir_competidor(self, id, nombre, probabilidad):
        self.carreras[id]['Competidores'].append({'Nombre':nombre, 'Probabilidad':probabilidad})

    def editar_competidor(self, id_carrera, id_competidor, nombre, probabilidad):
        self.carreras[id_carrera]['Competidores'][id_competidor]['Nombre']=nombre
        self.carreras[id_carrera]['Competidores'][id_competidor]['Probabilidad']=probabilidad
    
    def eliminar_competidor(self, id_carrera, id_competidor):
        del self.carreras[id_carrera]['Competidores'][id_competidor]

    def dar_apuestas_carrera(self, id_carrera):
        self.apuestas = self.controlador_apuestas.dar_apuestas_carrera(self.carreras[id_carrera]['id'])
        return list(self.apuestas)

    def dar_apuesta(self, id_carrera, id_apuesta):
        return self.dar_apuestas_carrera(id_carrera)[id_apuesta].copy()

    def crear_apuesta(self, apostador, id_carrera, valor, competidor):

        carrera_id = self.carreras[id_carrera]['id']
        apostador_id = list(filter(lambda x: x['Nombre']==apostador, self.apostadores))[0]['id']
        competidor_id = list(filter(lambda x: x['Nombre']==competidor, self.carreras[id_carrera]['Competidores']))[0]['id']
        
        apuesta_valida = self.controlador_apuestas.crear_apuesta(carrera_id, apostador_id, competidor_id, valor)
        return apuesta_valida

    def editar_apuesta(self, id_apuesta, apostador, id_carrera, valor, competidor):
        carrera_id = self.carreras[id_carrera]['id']
        apuesta_id = self.apuestas[id_apuesta]['id']
        apostador_id = list(filter(lambda x: x['Nombre']==apostador, self.apostadores))[0]['id']
        competidor_id = list(filter(lambda x: x['Nombre']==competidor, self.carreras[id_carrera]['Competidores']))[0]['id']
        
        apuesta_valida = self.controlador_apuestas.editar_apuesta(apuesta_id, carrera_id, apostador_id, competidor_id, valor)
        return apuesta_valida

    def eliminar_apuesta(self, id_carrera, id_apuesta):
        nombre_carrera =self.carreras[id_carrera]['Nombre']
        i = 0
        id = 0
        while i < len(self.apuestas):
            if self.apuestas[i]['Carrera'] == nombre_carrera:
                if id == id_apuesta:
                    self.apuestas.pop(i)
                    return True
                else:
                    id+=1
            i+=1
        
        return False
        del self.apuesta[id_apuesta]

    def dar_reporte_ganancias(self, index_carrera, index_competidor_ganador):       
        carrera = self.carreras[index_carrera]
        id_carrera = carrera['id']      
        id_competidor_ganador = carrera['Competidores'][index_competidor_ganador]['id']       
        return  self.controlador_carreras.dar_reporte_ganancias(id_carrera, id_competidor_ganador)   