from cmath import isnan, nan
from datetime import datetime

from pyparsing import empty

from src.modelo.declarative_base import engine, Base, session

from src.modelo.carrera import Carrera
from src.modelo.competidor import Competidor
from src.modelo.apostador import Apostador
from src.modelo.apuesta import Apuesta

# Lógica de negocio de EPorra
class Carreras():
	def __init__(self):
		Base.metadata.create_all(engine)

	def dar_carreras(self):
		carreras = []
		carreras_registradas = session.query(Carrera).order_by(Carrera.nombre).all()

		for item in carreras_registradas:
			competidores_map = []
			for competidor in item.competidores:
				competidores_map.append({'id':competidor.id, 'nombre': competidor.nombre, 'probabilidad': competidor.probabilidad})

			carrera = {'id': item.id ,'nombre': item.nombre, 'competidores': competidores_map, 'terminada':item.terminada}
			carreras.append(carrera)		

		return carreras
	
	def esCompetidorValido(self, competidor):
		return competidor["nombre"] == '' or competidor['probabilidad'] is None or len(competidor["nombre"]) > 200 or \
			   float(competidor['probabilidad']) < 0 or float(competidor['probabilidad']) > 1

	def crear_carrera(self, nombre, competidores):
		competidoresCarrera = []
		if nombre == "" or len(nombre)> 200:
			return False

		carreras_exitentes = session.query(Carrera).filter(Carrera.nombre == nombre).all() 

		if len(carreras_exitentes) > 0 :
			return False

		if(len(competidores)==0):
			return False	

		contadorRepetidos = 0
		suma_probabilidades = 0
		for competidor in competidores:			
			if self.esCompetidorValido(competidor):
				return False
			
			for item in competidores:
				if(competidor["nombre"] == item["nombre"]):
					contadorRepetidos += 1
	 		
			suma_probabilidades += competidor["probabilidad"]
   
		if(contadorRepetidos > len(competidores)):
			return False

		if(suma_probabilidades != 1):    
			return False
			
		carrera = Carrera(nombre = nombre, terminada=False)
		session.add(carrera)
		for item in competidores:			
			if item['probabilidad'] != 1:
				cuota = item['probabilidad']/(1-item['probabilidad'])
			else:
				cuota = 1

			competidor = Competidor(nombre=item["nombre"], carrera=carrera.id, probabilidad= item["probabilidad"], cuota = cuota,  ganador = False)
			session.add(competidor)
			competidoresCarrera.append(competidor)
			carrera.competidores = competidoresCarrera				
		
		session.commit()

		return True

	def terminarCarrera(self, id, competidorganadorid):	
		carrera =  session.query(Carrera).get(id)
		carrera.terminada = True 
		session.add(carrera)		

		competidor = session.query(Competidor).get(competidorganadorid)
		competidor.ganador = True
		session.add(competidor)

		session.commit()  

		return True

	def dar_reporte_ganancias(self, id_carrera, id_competidor_ganador):
		self.terminarCarrera(id_carrera, id_competidor_ganador)
		apostadores_carrera =  self.dar_apostadores_apuestas(id_carrera) 
		
		apostadores = []
		gananciaCasa = 0
		competidor_ganador = self.dar_competidor_ganador(id_competidor_ganador)		
		for apostador in apostadores_carrera:
			ganancia = 0
			apuesta = apostador['apuesta']
			if apostador['competidor_id'] == id_competidor_ganador:
				ganancia = apuesta + (apuesta/competidor_ganador.cuota)
			apostadores.append((apostador['nombre'], ganancia))
			gananciaCasa += apuesta - ganancia
		return apostadores, gananciaCasa

	def dar_apuestas_carrera(self, carrera_id):
		lista_apuestas = []	
		apuestas = session.query(Apuesta).filter(Apuesta.carrera_id == carrera_id).all()
		for apuesta in apuestas :
			carrera = session.query(Carrera).get(apuesta.carrera_id)
			competidor = session.query(Competidor).get(apuesta.competidor_id) 
			apostador = session.query(Apostador).get(apuesta.apostador_id) 
			lista_apuestas.append({'id':apuesta.id, 'Apostador':apostador.nombre, 'Carrera':carrera.nombre, 'Valor':apuesta.valor, 'Competidor':competidor.nombre})
		return lista_apuestas

	def crear_apuesta(self, carrera_id, apostador_id, competidor_id, valor):
		if not(self.validar_datos_apuesta(apostador_id, competidor_id, valor)):
			return False

		carrera = session.query(Carrera).get(carrera_id)
		if(len(carrera.competidores) < 2) : 
			return False

		apuesta = Apuesta(carrera_id = carrera_id, apostador_id = apostador_id, competidor_id = competidor_id, valor = valor)		
		session.add(apuesta)
		session.commit()
		return True

	def dar_apostadores(self):
     
		lista_apostadores = []
		apostadores = session.query(Apostador).order_by(Apostador.nombre).all()
		for apostador in apostadores : 
			lista_apostadores.append({'id':apostador.id, 'nombre':apostador.nombre})
		return lista_apostadores

	def dar_apostadores_apuestas(self, id_carrera):     
		apuestas = session.query(Apuesta).filter(Apuesta.carrera_id == id_carrera).all()
		lista_apostadores = []
		for apuesta in apuestas:
			apostador = session.query(Apostador).filter(Apostador.id == apuesta.apostador_id).first()
			lista_apostadores.append({'id':apostador.id, 'nombre':apostador.nombre, 'apuesta':apuesta.valor, 'competidor_id': apuesta.competidor_id})
		
		return lista_apostadores

	
	def dar_competidor_ganador(self, id_competidor_ganador):
		competidor = session.query(Competidor).get(id_competidor_ganador) 
		return competidor

	def crear_apostador(self, nombre):
		if nombre == "" or len(nombre) > 200:
			return False
		existeApostador = session.query(Apostador).filter(Apostador.nombre == nombre).all()
		if len(existeApostador) > 0:
			return False

		apostador = Apostador(nombre = nombre)
		session.add(apostador)
		session.commit()
		return True

	def editar_apostador(self, id, nombre):
		if nombre == "" or len(nombre) > 200:
			return False
		  
		apostador =  session.query(Apostador).get(id)
		existeApostador = session.query(Apostador).filter(Apostador.nombre == nombre).first()
		if not(existeApostador == None) and id != existeApostador.id:
			return False
  
		apostador.nombre = nombre 
		session.add(apostador)
		session.commit()
  
		return True

	def borrar_carrera(self, carreraid):
		carrera = session.query(Carrera).get(carreraid)
		if len(carrera.apuestas) == 0:
			session.delete(carrera)
			session.commit()
			return True
		return False

	def editar_apuesta(self, apuesta_id, carrera_id, apostador_id, competidor_id, valor):
		if not(self.validar_datos_apuesta(apostador_id, competidor_id, valor)):
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
		if(apostador_id is None or competidor_id is None or valor is None or valor == '') :
			return False

		valor = float(valor)
		if(valor <= 0) :
			return False

		return True