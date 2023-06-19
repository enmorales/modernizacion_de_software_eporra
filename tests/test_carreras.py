import unittest
import random 
import string
from unittest.util import _MAX_LENGTH

from faker import Faker

from src.logica.carreras import Carreras
from src.modelo.carrera import Carrera
from src.modelo.apuesta import Apuesta
from src.modelo.competidor import Competidor
from src.modelo.apostador import Apostador
from src.modelo.declarative_base import Session

class CarrerasTestCase(unittest.TestCase):

	def setUp(self):
		self.session = Session()
		self.logica = Carreras()
		self.data_factory = Faker()
		self.carreras_test = []
		self.apostadores_test = self.inicializar_apostadores(4)

	def tearDown(self):

		for apostador in self.apostadores_test : 
			self.session.delete(apostador)

		for carrera in self.carreras_test : 
			carreraExiste = self.session.query(Carrera).filter(Carrera.nombre == carrera.nombre).first()
			if carreraExiste is not None:
				apuestas = self.session.query(Apuesta).filter(Apuesta.carrera_id == carrera.id).all()
				for apuesta in apuestas : 
					self.session.delete(apuesta)
				self.session.delete(carrera)

		self.session.commit()

	def inicializar_carrera_valida(self) : 
		carrera_nombre = self.data_factory.name()
		
		competidores = [{'nombre':self.data_factory.name(), 'probabilidad':0.2},
						{'nombre':self.data_factory.name(), 'probabilidad':0.8}]
		self.logica.crear_carrera(carrera_nombre, competidores)
		carrera = self.session.query(Carrera).filter(Carrera.nombre == carrera_nombre).first()
		self.carreras_test.append(carrera)
		return carrera

	def inicializar_carrera_un_competidor(self, carrera_nombre = None) : 
		if carrera_nombre is None : 
			carrera_nombre = self.data_factory.name()
		
		competidores = [{'nombre':self.data_factory.name(), 'probabilidad':1}]
		self.logica.crear_carrera(carrera_nombre, competidores)
		carrera = self.session.query(Carrera).filter(Carrera.nombre == carrera_nombre).first()
		self.carreras_test.append(carrera)
		return carrera

	def inicializar_apostadores(self, cant = 0):
		apostadores_test = []
		for i in range(cant) : 
			apostador = Apostador(nombre=self.data_factory.name())
			self.session.add(apostador)
			apostadores_test.append(apostador)
		
		self.session.commit()
		return apostadores_test
		
	def test_carrera_crear_satisfactoriamente(self):
 		# Test de crear carrera
		nombre = self.data_factory.name()
		competidores = [{'nombre': self.data_factory.name(), 'probabilidad': 1}]

		self.logica.crear_carrera(nombre, competidores)
		consulta1 = self.session.query(Carrera).filter(Carrera.nombre == nombre).first()
		self.assertEqual(consulta1.nombre, nombre)
  
	def test_carrera_nombre_no_vacio(self):
		# El nombre de la carrera no debe estar vacío
		nombre = ''
		competidores = [{'nombre': self.data_factory.name(), 'probabilidad': 1}]		
		es_carrera_valida = self.logica.crear_carrera(nombre, competidores)
		self.assertEqual(False, es_carrera_valida)

	def test_carrera_nombre_no_superior_a_200_caracteres(self):
		# El nombre de la carrera debe ser menor a 200 caracteres
		nombre = '12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890MAYOR200' + self.data_factory.name()
		competidores = [{'nombre': self.data_factory.name(), 'probabilidad': 1}]	
		es_carrera_valida = self.logica.crear_carrera(nombre, competidores)
		self.assertEqual(False, es_carrera_valida)
  	
	def test_carrera_nombre_existe(self):
		# El nombre de la carrera no debe estar repetido	
		nombre = self.data_factory.name()
		competidores = [{'nombre': self.data_factory.name(), 'probabilidad': 1}]
		self.logica.crear_carrera(nombre, competidores)
		self.logica.crear_carrera(nombre, competidores)

		carreras = self.session.query(Carrera).filter(Carrera.nombre == nombre).all()  
		self.assertEqual(1, len(carreras))

	def test_carrera_competidores_existen(self):
		nombre = self.data_factory.name()
		competidores = []
		es_carrera_valida = self.logica.crear_carrera(nombre, competidores)
		self.assertEqual(False, es_carrera_valida)
  
	def test_carrera_competidores_se_guardan(self):
		nombre = self.data_factory.name()
		competidores = [{'nombre': self.data_factory.name(), 'probabilidad': 0.3}, 
						{'nombre': self.data_factory.name(), 'probabilidad': 0.3},
						{'nombre': self.data_factory.name(), 'probabilidad': 0.4}]
		self.logica.crear_carrera(nombre, competidores)
		carrera = self.session.query(Carrera).filter(Carrera.nombre == nombre).first()

		self.assertEqual(3, len(carrera.competidores))
    
	def test_carrera_competidor_nombre_vacio(self):
    		# Test: El nombre de competidor no debe ser vacío
		nombre = self.data_factory.name()
		competidores = [{'nombre': '', 'probabilidad': 1}]
		es_carrera_valida = self.logica.crear_carrera(nombre, competidores)
		self.assertEqual(False, es_carrera_valida)
  
	def test_carrera_competidor_probabilidad_nulo(self):
		# Test: La probabilidad del competidor no debe ser nulo
		nombre = self.data_factory.name()
		competidores = [{'nombre': self.data_factory.name(),'probabilidad': None}]
		es_carrera_valida = self.logica.crear_carrera(nombre, competidores)
		self.assertEqual(False, es_carrera_valida)
       
	def test_carrera_competidor_nombre_largo(self):
		# El nombre del competidor debe ser menor a 200 caracteres
		nombre_carrera = self.data_factory.name()
		nombre_competidor = '12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890MAYOR200' + self.data_factory.name()
		competidores = [{'nombre': nombre_competidor, 'probabilidad': 1}]	
		es_carrera_valida = self.logica.crear_carrera(nombre_carrera, competidores)
		self.assertEqual(False, es_carrera_valida)
  
	def test_carrera_competidor_probabilidad_mayor0_menor1(self):
    		# Test: La probabilidad del competidor debe tener un valor entre 0 y 1
		nombre = self.data_factory.name()
		competidores = [{'nombre': self.data_factory.name(),'probabilidad': 2}]
		es_carrera_valida = self.logica.crear_carrera(nombre, competidores)
		self.assertEqual(False, es_carrera_valida)
  
		nombre = self.data_factory.name()
		competidores = [{'nombre': self.data_factory.name(),'probabilidad': -1}]
		es_carrera_valida = self.logica.crear_carrera(nombre, competidores)
		self.assertEqual(False, es_carrera_valida)
  		
	def test_carrera_competidor_existente(self):
		# Competidor que ya existe en la misma carrera
		nombre_carrera = self.data_factory.name()
		nombre_competidor = self.data_factory.name()
		competidores = [{'nombre': nombre_competidor, 'probabilidad': 0.1}, 
						{'nombre': nombre_competidor, 'probabilidad': 0.9}]	
		es_carrera_valida = self.logica.crear_carrera(nombre_carrera, competidores)
		self.assertEqual(False, es_carrera_valida)
  
	def test_carrera_competidor_cuota_valida(self):
		# Competidores debe calcular y almacenar la cuota de cada competidor: cuota = probabilidad / 1- probabilidad
		nombre_carrera = self.data_factory.name()
		competidores = [{'nombre': self.data_factory.name(), 'probabilidad': 0.1}, 
						{'nombre': self.data_factory.name(), 'probabilidad': 0.3},
						{'nombre': self.data_factory.name(), 'probabilidad': 0.6}]	
		self.logica.crear_carrera(nombre_carrera, competidores)
  
		carrera =  self.session.query(Carrera).filter(Carrera.nombre == nombre_carrera).first()		
		
		cuotas_validas = True 
		for competidor in carrera.competidores:
			cuota = competidor.probabilidad/(1-competidor.probabilidad)
			if cuota != competidor.cuota:
				cuotas_validas = False

		self.assertEqual(cuotas_validas, True)

	def test_carrera_competidores_suma_probabilidades(self):
		# Al guardar la carrera, debe confirmar que la suma de las probabilidades de todos los competidores sea igual a 1 (esto es, el 100%)

		# Assert 1: validar suma de probabilidades = 1
		nombre_carrera_valida = self.data_factory.name()
		competidores = [{'nombre': self.data_factory.name(), 'probabilidad': 0.2},
						{'nombre': self.data_factory.name(), 'probabilidad': 0.5},
						{'nombre': self.data_factory.name(), 'probabilidad': 0.3}]	
		self.logica.crear_carrera(nombre_carrera_valida, competidores)
		carrera =  self.session.query(Carrera).filter(Carrera.nombre == nombre_carrera_valida).first()
		carrera_probabilidades_suma = 0
		for item in carrera.competidores:
			carrera_probabilidades_suma += item.probabilidad
  	
		self.assertEqual(1, carrera_probabilidades_suma)

		# Assert 2: validar error en suma de probabilidades != 1
		nombre_carrera_no_valida = self.data_factory.name()
		competidores = [{'nombre': self.data_factory.name(), 'probabilidad': 0.1},
						{'nombre': self.data_factory.name(), 'probabilidad': 0.3},
						{'nombre': self.data_factory.name(), 'probabilidad': 0.8}]	
		es_carrera_valida = self.logica.crear_carrera(nombre_carrera_no_valida, competidores)
		self.assertEqual(False, es_carrera_valida)
		
	def test_carrera_lista_ordenada_alfabeticamente(self): 
		# Lista de carreras ordenadas alfabeticamente

		nombre_carrera_1 = 'Z' + self.data_factory.name() 
		competidores = [{'nombre': self.data_factory.name(), 'probabilidad': 1}]	 
		self.logica.crear_carrera(nombre_carrera_1, competidores)

		nombre_carrera_2 = 'A' + self.data_factory.name() 
		competidores = [{'nombre': self.data_factory.name(), 'probabilidad': 1}]	 
		self.logica.crear_carrera(nombre_carrera_2, competidores)

		primer_nombre = ''
		carreras = self.logica.dar_carreras() 
		index = 0
		while index < len(carreras) and primer_nombre == '':
			carrera = carreras[index]
			if carrera['nombre'] == nombre_carrera_1:
				primer_nombre = nombre_carrera_1
			if carrera['nombre'] == nombre_carrera_2:
				primer_nombre = nombre_carrera_2
			index += 1

		self.assertEqual(nombre_carrera_2, primer_nombre)

	def test_carrera_lista_estado(self):
		# Lista incluye carreras terminadas y no terminadas

		nombre_carrera_1 = self.data_factory.name()
		competidores = [{'nombre': self.data_factory.name(), 'probabilidad': 1}]	
		self.logica.crear_carrera(nombre_carrera_1, competidores)

		nombre_carrera_2 = self.data_factory.name()
		competidores = [{'nombre': self.data_factory.name(), 'probabilidad': 1}]	
		self.logica.crear_carrera(nombre_carrera_2, competidores)
		
		carrera =  self.session.query(Carrera).filter(Carrera.nombre == nombre_carrera_2).first()
		self.logica.terminarCarrera(carrera.id, 1)

		carreras = self.logica.dar_carreras()

		incluye_carreras_terminadas = False 
		incluye_carreras_no_terminadas = False 
		for item in carreras:
			if item['terminada']:
				incluye_carreras_terminadas = True
			else:
				incluye_carreras_no_terminadas = True

		self.assertEqual(True, incluye_carreras_terminadas and incluye_carreras_no_terminadas)
  
	def test_carrera_guarda_terminada(self):  
		carreras = self.logica.dar_carreras()		
		carreraid = carreras[0]['id']
    
		competidores = carreras[0]['competidores']
		competidorganadorid = competidores[0]["id"]	
  		
		self.logica.terminarCarrera(carreraid, competidorganadorid)
		
		carrera = self.session.query(Carrera).get(carreraid)
		self.assertEqual(True, carrera.terminada)

		competidor = self.session.query(Competidor).get(competidorganadorid)
		self.assertEqual(True, competidor.ganador)
	
	def test_reporte_apostador_ganador(self):
		carrera_nombre = self.data_factory.name()
		competidores = [{'nombre':self.data_factory.name(), 'probabilidad':0.2},
						{'nombre':self.data_factory.name(), 'probabilidad':0.8}]
		self.logica.crear_carrera(carrera_nombre, competidores)
		carrera = self.session.query(Carrera).filter(Carrera.nombre == carrera_nombre).first()
		competidor_ganador = carrera.competidores[0]
		apostador_id = self.apostadores_test[0].id
		competidor_id = competidor_ganador.id
		valor_apostado = 1000
		self.logica.crear_apuesta(carrera.id, apostador_id, competidor_id, valor_apostado)
		ganancia = valor_apostado + (valor_apostado/competidor_ganador.cuota)
	
		ganancia_apostador_ganador = 0
		ganancias_apostadores, ganancia_casa = self.logica.dar_reporte_ganancias(carrera.id, competidor_ganador.id)
		for ganancia_apostador in ganancias_apostadores:
			nombre, valor = ganancia_apostador
			if self.apostadores_test[0].nombre == nombre:
				ganancia_apostador_ganador = valor		
  
		self.assertEqual(ganancia_apostador_ganador, ganancia)

	def test_reporte_apostador_perdedor(self):
		carrera_nombre = self.data_factory.name()
		competidores = [{'nombre':self.data_factory.name(), 'probabilidad':0.2},
						{'nombre':self.data_factory.name(), 'probabilidad':0.8}]
		self.logica.crear_carrera(carrera_nombre, competidores)
		carrera = self.session.query(Carrera).filter(Carrera.nombre == carrera_nombre).first()
		competidor_ganador = carrera.competidores[0]
		apostador_id = self.apostadores_test[0].id
		competidor_id = carrera.competidores[1].id
		valor_apostado = 1000
		self.logica.crear_apuesta(carrera.id, apostador_id, competidor_id, valor_apostado)		
 
		ganancia_apostador_perdedor = 0
		ganancias_apostadores, ganancia_casa = self.logica.dar_reporte_ganancias(carrera.id, competidor_ganador.id)
		for ganancia_apostador in ganancias_apostadores:
			nombre, valor = ganancia_apostador
			if self.apostadores_test[0].nombre == nombre:
				ganancia_apostador_perdedor = valor		
  
		self.assertEqual(ganancia_apostador_perdedor, 0)

	def test_reporte_ganancia_casa_positiva(self):
		carrera_nombre = self.data_factory.name()
		competidores = [{'nombre':self.data_factory.name(), 'probabilidad':0.2},
						{'nombre':self.data_factory.name(), 'probabilidad':0.8}]
		self.logica.crear_carrera(carrera_nombre, competidores)
		carrera = self.session.query(Carrera).filter(Carrera.nombre == carrera_nombre).first()
		competidor_perdedor = carrera.competidores[0]
		competidor_ganador = carrera.competidores[1]

		apostador_1_id = self.apostadores_test[0].id
		competidor_apuesta_1_id = competidor_ganador.id
		apuesta_1_valor_apostado = 1000
		self.logica.crear_apuesta(carrera.id, apostador_1_id, competidor_apuesta_1_id, apuesta_1_valor_apostado)
		ganancia_apuesta_1 = apuesta_1_valor_apostado + (apuesta_1_valor_apostado/competidor_ganador.cuota)

		apostador_2_id = self.apostadores_test[2].id
		competidor_apuesta_2_id = competidor_ganador.id
		apuesta_2_valor_apostado = 500
		self.logica.crear_apuesta(carrera.id, apostador_2_id, competidor_apuesta_2_id, apuesta_2_valor_apostado)
		ganancia_apuesta_2 = apuesta_2_valor_apostado + (apuesta_2_valor_apostado/competidor_ganador.cuota)
	
		apostador_3_id = self.apostadores_test[3].id
		competidor_apuesta_3_id = competidor_perdedor.id
		apuesta_3_valor_apostado = 3000
		self.logica.crear_apuesta(carrera.id, apostador_3_id, competidor_apuesta_3_id, apuesta_3_valor_apostado)
		ganancia_apuesta_3 = 0

		ganancia_casa_esperado = (apuesta_1_valor_apostado + apuesta_2_valor_apostado + apuesta_3_valor_apostado) - \
						(ganancia_apuesta_1 + ganancia_apuesta_2 + ganancia_apuesta_3)

		ganancias_apostadores, ganancia_casa = self.logica.dar_reporte_ganancias(carrera.id, competidor_ganador.id)
 
		self.assertEqual(ganancia_casa, ganancia_casa_esperado)
  
	def test_reporte_ganancia_casa_negativa(self):
		carrera_nombre = self.data_factory.name()
		competidores = [{'nombre':self.data_factory.name(), 'probabilidad':0.2},
						{'nombre':self.data_factory.name(), 'probabilidad':0.8}]
		self.logica.crear_carrera(carrera_nombre, competidores)
		carrera = self.session.query(Carrera).filter(Carrera.nombre == carrera_nombre).first()
		competidor_perdedor = carrera.competidores[0]
		competidor_ganador = carrera.competidores[1]

		apostador_1_id = self.apostadores_test[0].id
		competidor_apuesta_1_id = competidor_ganador.id
		apuesta_1_valor_apostado = 1000
		self.logica.crear_apuesta(carrera.id, apostador_1_id, competidor_apuesta_1_id, apuesta_1_valor_apostado)
		ganancia_apuesta_1 = apuesta_1_valor_apostado + (apuesta_1_valor_apostado/competidor_ganador.cuota)

		apostador_2_id = self.apostadores_test[2].id
		competidor_apuesta_2_id = competidor_ganador.id
		apuesta_2_valor_apostado = 500
		self.logica.crear_apuesta(carrera.id, apostador_2_id, competidor_apuesta_2_id, apuesta_2_valor_apostado)
		ganancia_apuesta_2 = apuesta_2_valor_apostado + (apuesta_2_valor_apostado/competidor_ganador.cuota)
	
		apostador_3_id = self.apostadores_test[3].id
		competidor_apuesta_3_id = competidor_ganador.id
		apuesta_3_valor_apostado = 3000
		self.logica.crear_apuesta(carrera.id, apostador_3_id, competidor_apuesta_3_id, apuesta_3_valor_apostado)
		ganancia_apuesta_3 = apuesta_3_valor_apostado + (apuesta_3_valor_apostado/competidor_ganador.cuota)

		ganancia_casa_esperado = (apuesta_1_valor_apostado + apuesta_2_valor_apostado + apuesta_3_valor_apostado) - \
						(ganancia_apuesta_1 + ganancia_apuesta_2 + ganancia_apuesta_3)

		ganancias_apostadores, ganancia_casa = self.logica.dar_reporte_ganancias(carrera.id, competidor_ganador.id)
		self.assertEqual(ganancia_casa, ganancia_casa_esperado)
  
	def test_reporte_ganancia_casa_cero(self):
		carrera_nombre = self.data_factory.name()
		competidores = [{'nombre':self.data_factory.name(), 'probabilidad':0.5},
						{'nombre':self.data_factory.name(), 'probabilidad':0.5}]
		self.logica.crear_carrera(carrera_nombre, competidores)
		carrera = self.session.query(Carrera).filter(Carrera.nombre == carrera_nombre).first()
		competidor_perdedor = carrera.competidores[0]
		competidor_ganador = carrera.competidores[1]

		apostador_1_id = self.apostadores_test[0].id
		competidor_apuesta_1_id = competidor_ganador.id
		apuesta_1_valor_apostado = 2000
		self.logica.crear_apuesta(carrera.id, apostador_1_id, competidor_apuesta_1_id, apuesta_1_valor_apostado)
		ganancia_apuesta_1 =  apuesta_1_valor_apostado + (apuesta_1_valor_apostado/competidor_ganador.cuota)

		apostador_2_id = self.apostadores_test[2].id
		competidor_apuesta_2_id = competidor_perdedor.id
		apuesta_2_valor_apostado = 2000
		self.logica.crear_apuesta(carrera.id, apostador_2_id, competidor_apuesta_2_id, apuesta_2_valor_apostado)
		ganancia_apuesta_2 = 0

		ganancia_casa_esperado = (apuesta_1_valor_apostado + apuesta_2_valor_apostado)
		ganancia_casa_esperado -= (ganancia_apuesta_1 + ganancia_apuesta_2)
		ganancias_apostadores, ganancia_casa = self.logica.dar_reporte_ganancias(carrera.id, competidor_ganador.id)
		
		self.assertEqual(ganancia_casa, ganancia_casa_esperado)
  
	def test_apuesta_lista_vacia(self):
 		# Test de listar apuestas cuando la carrera no tiene apuestas
		carrera_id = 0

		apuestas = self.logica.dar_apuestas_carrera(carrera_id)
		self.assertListEqual([],apuestas)

	def test_apuesta_satisfactoria(self):
		# Test de apuesta creada satisfactoriamente
		carrera = self.inicializar_carrera_valida()
		apostador_id = self.apostadores_test[0].id
		competidor_id = carrera.competidores[0].id
		self.logica.crear_apuesta(carrera.id, apostador_id, competidor_id, 1000)
		apuesta = self.session.query(Apuesta).filter(Apuesta.carrera_id == carrera.id, Apuesta.apostador_id == apostador_id, Apuesta.competidor_id == competidor_id).first()
		self.assertEqual(1000,apuesta.valor)

	def test_apuesta_lista_con_datos(self):
		# Test lista incluye nombre de apostador, nombre de competidor y valor
		carrera = self.inicializar_carrera_valida()
		apostador_1_id = self.apostadores_test[0].id
		apostador_2_id = self.apostadores_test[1].id
		competidor_1_id = carrera.competidores[0].id
		competidor_2_id = carrera.competidores[1].id
		self.logica.crear_apuesta(carrera.id, apostador_1_id, competidor_1_id, 1000)
		self.logica.crear_apuesta(carrera.id, apostador_2_id, competidor_2_id, 2000)
		apuestas = self.logica.dar_apuestas_carrera(carrera.id)
		self.assertEqual(2,len(apuestas))

	def test_apuesta_apostador_nulo(self):
		# Test de apuesta: Apostador no puede ser nulo
		carrera = self.inicializar_carrera_valida()
		apostador_id = None 
		competidor_id = carrera.competidores[0].id
		apuesta_valida = self.logica.crear_apuesta(carrera.id, apostador_id, competidor_id, 1000)
		self.assertFalse(apuesta_valida)

	def test_apuesta_competidor_nulo(self):
		# Test de apuesta: Competidor no puede ser nulo
		carrera = self.inicializar_carrera_valida()
		apostador_id = self.apostadores_test[0].id
		competidor_id = None
		apuesta_valida = self.logica.crear_apuesta(carrera.id, apostador_id, competidor_id, 1000)
		self.assertFalse(apuesta_valida)

	def test_apuesta_valor_nulo(self):
		# Test de apuesta: Valor no puede ser nulo
		carrera = self.inicializar_carrera_valida()
		apostador_id = self.apostadores_test[0].id
		competidor_id = carrera.competidores[0].id
		valor = None 
		apuesta_valida = self.logica.crear_apuesta(carrera.id, apostador_id, competidor_id, valor)
		self.assertFalse(apuesta_valida)

	def test_apuesta_valor_cero(self):
		# Test de apuesta: Valor no puede ser cero
		carrera = self.inicializar_carrera_valida()
		apostador_id = self.apostadores_test[0].id
		competidor_id = carrera.competidores[0].id
		valor = 0
		apuesta_valida = self.logica.crear_apuesta(carrera.id, apostador_id, competidor_id, valor)
		self.assertFalse(apuesta_valida)

	def test_apuesta_valor_negativo(self):
		# Test de apuesta: Valor no puede ser negativo
		carrera = self.inicializar_carrera_valida()
		apostador_id = self.apostadores_test[0].id
		competidor_id = carrera.competidores[0].id
		valor = -1
		apuesta_valida = self.logica.crear_apuesta(carrera.id, apostador_id, competidor_id, valor)
		self.assertFalse(apuesta_valida)

	def test_apuesta_carrera_competidores_minimos(self):
		# Test de apuesta: No permitir apuestas si la carrera no tiene al menos dos competidores
		carrera = self.inicializar_carrera_un_competidor()
		apostador_id = self.apostadores_test[0].id
		competidor_id = carrera.competidores[0].id
		apuesta_valida = self.logica.crear_apuesta(carrera.id,apostador_id, competidor_id, 1000)		
		self.assertFalse(apuesta_valida)

	def test_apuesta_apostador_multiples_apuestas(self):
		# Test de apuesta: Apostador realiza varias apuestas
		carrera = self.inicializar_carrera_valida()
		apostador_id = self.apostadores_test[0].id
		competidor_1_id = carrera.competidores[0].id
		competidor_2_id = carrera.competidores[1].id
		self.logica.crear_apuesta(carrera.id, apostador_id, competidor_1_id, 1000)
		self.logica.crear_apuesta(carrera.id, apostador_id, competidor_2_id, 2000)
		apuestas = self.session.query(Apuesta).filter(Apuesta.carrera_id == carrera.id).all()
		apuestas_suma = 0
		for apuesta in apuestas :
			apuestas_suma += apuesta.valor
		self.assertEqual(3000, apuestas_suma)

	def test_apuesta_competidor_multiples_apuestas(self):
		# Test de apuesta: Varias apuestas por el mismo competidor
		carrera = self.inicializar_carrera_valida()
		apostador_1_id = self.apostadores_test[0].id
		apostador_2_id = self.apostadores_test[1].id
		competidor_id = carrera.competidores[0].id
		self.logica.crear_apuesta(carrera.id, apostador_1_id, competidor_id, 1000)
		self.logica.crear_apuesta(carrera.id, apostador_2_id, competidor_id, 2000)
		apuestas = self.session.query(Apuesta).filter(Apuesta.carrera_id == carrera.id).all()
		apuestas_suma = 0 
		for apuesta in apuestas :
			apuestas_suma += apuesta.valor
		self.assertEqual(3000, apuestas_suma)

	def test_apuesta_apostador_multiples_apuestas_igual_competidor(self): 
		# Test de apuesta: Apostador varias apuestas por el mismo competidor
		carrera = self.inicializar_carrera_valida()
		apostador_id = self.apostadores_test[0].id
		competidor_id = carrera.competidores[0].id
		self.logica.crear_apuesta(carrera.id, apostador_id, competidor_id, 1000)
		self.logica.crear_apuesta(carrera.id, apostador_id, competidor_id, 2000)
		apuestas = self.session.query(Apuesta).filter(Apuesta.carrera_id == carrera.id).all()
		apuestas_suma = 0
		for apuesta in apuestas :
			apuestas_suma += apuesta.valor
		self.assertEqual(3000, apuestas_suma)
  
	
	def test_listar_apostadores_en_orden_alfabeticio_asc(self):
		nombre_apostador = "0FirstInOrderAscByName"
		apostador = Apostador(nombre = nombre_apostador)
		self.session.add(apostador)
		self.session.commit()
  
		apostadores = self.logica.dar_apostadores()
		self.assertEqual(nombre_apostador, apostadores[0]["nombre"])
  
	def test_crear_apostador(self):
		nombre = self.data_factory.name()	
		self.logica.crear_apostador(nombre)
		
		apostador_creado = self.session.query(Apostador).filter(Apostador.nombre == nombre).first()
			
		self.assertEqual(nombre, apostador_creado.nombre)
  
	def test_validar_nombre_requerido_en_crear_apostador(self):
		nombre = ""
		apostador_creado = self.logica.crear_apostador(nombre)

		self.assertEqual(False, apostador_creado)
	def test_validar_nombre_requerido_en_crear_apostador(self):
		MAX_LENGTH_OF_STRING = 201
		nombre = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(MAX_LENGTH_OF_STRING))
		apostador_creado = self.logica.crear_apostador(nombre)

		self.assertEqual(False, apostador_creado)
  
	def test_nombre_apostador_no_debe_repetirse(self):
		nombre = self.data_factory.name()	
		self.logica.crear_apostador(nombre)
		self.logica.crear_apostador(nombre)

		apostadores = self.session.query(Apostador).filter(Apostador.nombre == nombre).all()
		self.assertEqual(1, len(apostadores))
		
	def test_editar_apostador(self):
		nombre = self.data_factory.name()		
		self.logica.crear_apostador(nombre)
		apostadorCreado = self.session.query(Apostador).filter(Apostador.nombre == nombre).first()

		nuevoNombre = self.data_factory.name()		
		resultado = self.logica.editar_apostador(apostadorCreado.id, nuevoNombre)
		apostadorActualizado = self.session.query(Apostador).filter(Apostador.nombre == nuevoNombre).first()
			
		self.assertEqual(apostadorCreado.id, apostadorActualizado.id)
  
	def test_editar_apostador_nombre_no_vacio(self):
		nombre = ""
		resultado = self.logica.editar_apostador(1, nombre)
		self.assertEqual(False, resultado)
  
	def test_editar_apostador_nombre_maximo_caracteres(self):
		nombre = self.data_factory.name()		
		self.logica.crear_apostador(nombre)
		apostadorCreado = self.session.query(Apostador).filter(Apostador.nombre == nombre).first()
  
		MAX_LENGTH_OF_STRING = 201
		nombreNuevo = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(MAX_LENGTH_OF_STRING))

		resultado = self.logica.editar_apostador(apostadorCreado.id, nombreNuevo)
		self.assertEqual(False, resultado)
  
	def test_editar_apostado_nombre_no_debe_repetirse(self):
		nombre1 = self.data_factory.name()	
		self.logica.crear_apostador(nombre1)

		nombre2 = self.data_factory.name()	
		self.logica.crear_apostador(nombre2)

		apostador1Creado = self.session.query(Apostador).filter(Apostador.nombre == nombre1).first()
		self.logica.editar_apostador(apostador1Creado.id, nombre2)

		apostadores = self.session.query(Apostador).filter(Apostador.nombre == nombre2).all()
		self.assertEqual(1, len(apostadores)) 
  
	def test_carrera_borrado_satisfactorio(self):
		# Test de carrera: Borrado satisfactorio
		carrera = self.inicializar_carrera_valida()
		self.logica.borrar_carrera(carrera.id)
		carreraQuery = self.session.query(Carrera).filter(Carrera.nombre == carrera.nombre).first()
		self.assertIsNone(carreraQuery)

	def test_carrera_borrado_cancelado_por_apuestas_asociadas(self):
		# Test de carrera: Impedir el borrado de carrera con apuestas asociadas
		carrera = self.inicializar_carrera_valida()
		apostador_id = self.apostadores_test[0].id
		competidor_id = carrera.competidores[0].id
		self.logica.crear_apuesta(carrera.id, apostador_id, competidor_id, 1000)
		self.logica.borrar_carrera(carrera.id)
		carreraQuery = self.session.query(Carrera).filter(Carrera.nombre == carrera.nombre).first()
		self.assertIsInstance(carreraQuery, Carrera)		

	def test_apuesta_editar_satisfactorio(self):
		# Test de apuesta: Edición de apuesta satisfactoria
		carrera = self.inicializar_carrera_valida()
		apostador_id = self.apostadores_test[0].id
		competidor_id = carrera.competidores[0].id
		self.logica.crear_apuesta(carrera.id, apostador_id, competidor_id, 1000)
		apostador_upd_id = self.apostadores_test[1].id
		competidor_upd_id = carrera.competidores[1].id
		apuesta = self.session.query(Apuesta).filter(Apuesta.carrera_id == carrera.id, Apuesta.apostador_id == apostador_id, Apuesta.competidor_id == competidor_id).first()
		self.logica.editar_apuesta(apuesta.id, carrera.id, apostador_upd_id, competidor_upd_id, 2000)
		apuestaEditada = self.session.query(Apuesta).filter(Apuesta.carrera_id == carrera.id, Apuesta.apostador_id == apostador_upd_id, Apuesta.competidor_id == competidor_upd_id).first()
		self.session.refresh(apuestaEditada)
		self.assertEqual(2000,apuestaEditada.valor)

	def test_apuesta_editar_apostador_nulo(self):
		# Test de apuesta: Apostador no puede ser nulo
		carrera = self.inicializar_carrera_valida()
		apostador_id = self.apostadores_test[0].id
		competidor_id = carrera.competidores[0].id
		self.logica.crear_apuesta(carrera.id, apostador_id, competidor_id, 1000)
		apuesta = self.session.query(Apuesta).filter(Apuesta.carrera_id == carrera.id, Apuesta.apostador_id == apostador_id, Apuesta.competidor_id == competidor_id).first()
		apostador_upd_id = None 
		apuesta_valida = self.logica.editar_apuesta(apuesta.id, carrera.id, apostador_upd_id, apuesta.competidor_id, apuesta.valor)
		self.assertFalse(apuesta_valida)

	def test_apuesta_editar_competidor_nulo(self):
		# Test de apuesta: Competidor no puede ser nulo
		carrera = self.inicializar_carrera_valida()
		apostador_id = self.apostadores_test[0].id
		competidor_id = carrera.competidores[0].id
		self.logica.crear_apuesta(carrera.id, apostador_id, competidor_id, 1000)
		apuesta = self.session.query(Apuesta).filter(Apuesta.carrera_id == carrera.id, Apuesta.apostador_id == apostador_id, Apuesta.competidor_id == competidor_id).first()
		competidor_upd_id = None 
		apuesta_valida = self.logica.editar_apuesta(apuesta.id, carrera.id, apuesta.apostador_id, competidor_upd_id, apuesta.valor)
		self.assertFalse(apuesta_valida)

	def test_apuesta_editar_valor_nulo(self):
		# Test de apuesta: Valor no puede ser nulo
		carrera = self.inicializar_carrera_valida()
		apostador_id = self.apostadores_test[0].id
		competidor_id = carrera.competidores[0].id
		self.logica.crear_apuesta(carrera.id, apostador_id, competidor_id, 1000)
		apuesta = self.session.query(Apuesta).filter(Apuesta.carrera_id == carrera.id, Apuesta.apostador_id == apostador_id, Apuesta.competidor_id == competidor_id).first()
		valor_upd = None 
		apuesta_valida = self.logica.editar_apuesta(apuesta.id, carrera.id, apuesta.apostador_id, apuesta.competidor_id, valor_upd)
		self.assertFalse(apuesta_valida)

	def test_apuesta_editar_valor_cero(self):
		# Test de apuesta: Valor no puede ser cero
		carrera = self.inicializar_carrera_valida()
		apostador_id = self.apostadores_test[0].id
		competidor_id = carrera.competidores[0].id
		self.logica.crear_apuesta(carrera.id, apostador_id, competidor_id, 1000)
		apuesta = self.session.query(Apuesta).filter(Apuesta.carrera_id == carrera.id, Apuesta.apostador_id == apostador_id, Apuesta.competidor_id == competidor_id).first()
		valor_upd = 0 
		apuesta_valida = self.logica.editar_apuesta(apuesta.id, carrera.id, apuesta.apostador_id, apuesta.competidor_id, valor_upd)
		self.assertFalse(apuesta_valida)

	def test_apuesta_editar_valor_negativo(self):
		# Test de apuesta: Valor no puede ser negativo
		carrera = self.inicializar_carrera_valida()
		apostador_id = self.apostadores_test[0].id
		competidor_id = carrera.competidores[0].id
		self.logica.crear_apuesta(carrera.id, apostador_id, competidor_id, 1000)
		apuesta = self.session.query(Apuesta).filter(Apuesta.carrera_id == carrera.id, Apuesta.apostador_id == apostador_id, Apuesta.competidor_id == competidor_id).first()
		valor_upd = -1000
		apuesta_valida = self.logica.editar_apuesta(apuesta.id, carrera.id, apuesta.apostador_id, apuesta.competidor_id, valor_upd)
		self.assertFalse(apuesta_valida)

	def test_apuesta_editar_valor_decimal(self):
		# Test de apuesta: Valor recibe decimales
		carrera = self.inicializar_carrera_valida()
		apostador_id = self.apostadores_test[0].id
		competidor_id = carrera.competidores[0].id
		self.logica.crear_apuesta(carrera.id, apostador_id, competidor_id, 1000)
		apuesta = self.session.query(Apuesta).filter(Apuesta.carrera_id == carrera.id, Apuesta.apostador_id == apostador_id, Apuesta.competidor_id == competidor_id).first()
		valor_upd = 1000.53
		apuesta_valida = self.logica.editar_apuesta(apuesta.id, carrera.id, apuesta.apostador_id, apuesta.competidor_id, valor_upd)
		self.assertTrue(apuesta_valida)
	
	def test_apuesta_editar_valor_decimal(self):
		# Test de apuesta: Valor recibe decimales
		carrera = self.inicializar_carrera_valida()
		apostador_id = self.apostadores_test[0].id
		competidor_id = carrera.competidores[0].id
		self.logica.crear_apuesta(carrera.id, apostador_id, competidor_id, 1000)
		apuesta = self.session.query(Apuesta).filter(Apuesta.carrera_id == carrera.id, Apuesta.apostador_id == apostador_id, Apuesta.competidor_id == competidor_id).first()
		valor_upd = 1000.53
		apuesta_valida = self.logica.editar_apuesta(apuesta.id, carrera.id, apuesta.apostador_id, apuesta.competidor_id, valor_upd)
		self.assertTrue(apuesta_valida)

	def test_apuesta_editar_apostador_multiples_apuestas(self):
		# Test de apuesta: Apostador realiza varias apuestas
		carrera = self.inicializar_carrera_valida()
		apostador_1_id = self.apostadores_test[0].id
		apostador_2_id = self.apostadores_test[1].id
		competidor_1_id = carrera.competidores[0].id
		competidor_2_id = carrera.competidores[1].id
		self.logica.crear_apuesta(carrera.id, apostador_1_id, competidor_1_id, 1000)
		self.logica.crear_apuesta(carrera.id, apostador_2_id, competidor_2_id, 2000)
		apostador_unico = apostador_1_id
		apuestas = self.session.query(Apuesta).filter(Apuesta.carrera_id == carrera.id).all()
		for apuesta in apuestas :
			valor_upd = apuesta.valor * 2
			self.logica.editar_apuesta(apuesta.id, carrera.id, apostador_unico, apuesta.competidor_id, valor_upd)
		apuestas = self.session.query(Apuesta).filter(Apuesta.carrera_id == carrera.id, Apuesta.apostador_id == apostador_unico).all()
		apuestas_suma = 0
		for apuesta in apuestas :
			self.session.refresh(apuesta)
			apuestas_suma += apuesta.valor
		self.assertEqual(6000, apuestas_suma)

	def test_apuesta_editar_competidor_multiples_apuestas(self):
		# Test de apuesta: Varias apuestas por el mismo competidor
		carrera = self.inicializar_carrera_valida()
		apostador_1_id = self.apostadores_test[0].id
		apostador_2_id = self.apostadores_test[1].id
		competidor_1_id = carrera.competidores[0].id
		competidor_2_id = carrera.competidores[1].id
		self.logica.crear_apuesta(carrera.id, apostador_1_id, competidor_1_id, 1000)
		self.logica.crear_apuesta(carrera.id, apostador_2_id, competidor_2_id, 2000)
		competidor_unico = competidor_1_id
		apuestas = self.session.query(Apuesta).filter(Apuesta.carrera_id == carrera.id).all()
		for apuesta in apuestas :
			valor_upd = apuesta.valor * 2
			self.logica.editar_apuesta(apuesta.id, carrera.id, apuesta.apostador_id, competidor_unico, valor_upd)
		apuestas = self.session.query(Apuesta).filter(Apuesta.carrera_id == carrera.id, Apuesta.competidor_id == competidor_unico).all()
		apuestas_suma = 0
		for apuesta in apuestas :
			self.session.refresh(apuesta)
			apuestas_suma += apuesta.valor
		self.assertEqual(6000, apuestas_suma)

	def test_apuesta_editar_apostador_multiples_apuestas_igual_competidor(self):
		# Test de apuesta: Apostador varias apuestas por el mismo competidor
		carrera = self.inicializar_carrera_valida()
		apostador_1_id = self.apostadores_test[0].id
		apostador_2_id = self.apostadores_test[1].id
		competidor_1_id = carrera.competidores[0].id
		competidor_2_id = carrera.competidores[1].id
		self.logica.crear_apuesta(carrera.id, apostador_1_id, competidor_1_id, 1000)
		self.logica.crear_apuesta(carrera.id, apostador_2_id, competidor_2_id, 2000)
		apostador_unico = apostador_1_id
		competidor_unico = competidor_1_id
		apuestas = self.session.query(Apuesta).filter(Apuesta.carrera_id == carrera.id).all()
		for apuesta in apuestas :
			valor_upd = apuesta.valor * 2
			self.logica.editar_apuesta(apuesta.id, carrera.id, apostador_unico, competidor_unico, valor_upd)
		apuestas = self.session.query(Apuesta).filter(Apuesta.carrera_id == carrera.id).all()
		apuestas_suma = 0
		for apuesta in apuestas :
			self.session.refresh(apuesta)
			apuestas_suma += apuesta.valor
		self.assertEqual(6000, apuestas_suma)