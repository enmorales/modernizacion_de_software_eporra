from src.logica.carreras import Carreras

class Logica_mock():

    def __init__(self):
        self.logica_carreras = Carreras()
        self.carreras = []
        
    def dar_carreras(self):
        self.carreras = []
        for carrera in self.logica_carreras.dar_carreras().copy(): 
            competidores_map = []
            for competidor in carrera['competidores']:
                competidores_map.append({'id':competidor['id'],'Nombre': competidor['nombre'], 'Probabilidad': competidor['probabilidad']})
            self.carreras.append({'id':carrera['id'],'Nombre':carrera['nombre'],'Competidores':competidores_map,'Abierta':not(carrera['terminada'])})

        return self.carreras

    def dar_carrera(self, id_carrera):
        return self.carreras[id_carrera].copy()
    
    def crear_carrera(self, nombre, competidores):
        competidores_map = [{'nombre': comp['Nombre'], 'probabilidad': comp['Probabilidad']} for comp in competidores]
        carrera_guardada = self.logica_carreras.crear_carrera(nombre, competidores_map)
        return carrera_guardada

    def editar_carrera(self, id, nombre):
        self.carreras[id]['Nombre'] = nombre

    def terminar_carrera(self, id, ganador):
        self.carreras[id]['Ganador'] = ganador

    def eliminar_carrera(self, id):
        carrera_eliminada = self.logica_carreras.borrar_carrera(self.carreras[id]['id'])
        return carrera_eliminada

    def dar_apostadores(self):
        self.apostadores = []
        for apostador in self.logica_carreras.dar_apostadores(): 
            self.apostadores.append({'id':apostador['id'], 'Nombre':apostador['nombre']})

        return self.apostadores.copy()

    def aniadir_apostador(self, nombre):
        return self.logica_carreras.crear_apostador(nombre=nombre)
    
    def editar_apostador(self, id, nombre):
        apostador_id = self.apostadores[id]['id']
        return self.logica_carreras.editar_apostador(id=apostador_id, nombre=nombre)
    
    def eliminar_apostador(self, id):
        del self.apostadores[id]

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
        self.apuestas = self.logica_carreras.dar_apuestas_carrera(self.carreras[id_carrera]['id'])
        return list(self.apuestas)

    def dar_apuesta(self, id_carrera, id_apuesta):
        return self.dar_apuestas_carrera(id_carrera)[id_apuesta].copy()

    def crear_apuesta(self, apostador, id_carrera, valor, competidor):

        carrera_id = self.carreras[id_carrera]['id']
        apostador_id = list(filter(lambda x: x['Nombre']==apostador, self.apostadores))[0]['id']
        competidor_id = list(filter(lambda x: x['Nombre']==competidor, self.carreras[id_carrera]['Competidores']))[0]['id']
        
        apuesta_valida = self.logica_carreras.crear_apuesta(carrera_id, apostador_id, competidor_id, valor)
        return apuesta_valida

    def editar_apuesta(self, id_apuesta, apostador, id_carrera, valor, competidor):
        carrera_id = self.carreras[id_carrera]['id']
        apuesta_id = self.apuestas[id_apuesta]['id']
        apostador_id = list(filter(lambda x: x['Nombre']==apostador, self.apostadores))[0]['id']
        competidor_id = list(filter(lambda x: x['Nombre']==competidor, self.carreras[id_carrera]['Competidores']))[0]['id']
        
        apuesta_valida = self.logica_carreras.editar_apuesta(apuesta_id, carrera_id, apostador_id, competidor_id, valor)
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
        return  self.logica_carreras.dar_reporte_ganancias(id_carrera, id_competidor_ganador)   