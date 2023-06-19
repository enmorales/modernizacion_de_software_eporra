from PyQt5.QtWidgets import QApplication

from .Vista_lista_carreras import Vista_lista_carreras
from .Vista_lista_apostadores import Vista_lista_apostadores
from .Vista_carrera import Vista_carrera
from .Vista_lista_apuestas import Vista_lista_apuestas
from .Vista_reporte_ganancias import Vista_reporte_ganancias

class App_EPorra(QApplication):
    """
    Clase principal de la interfaz que coordina las diferentes vistas/ventanas de la aplicación
    """

    def __init__(self, sys_argv, logica):
        """
        Constructor de la interfaz. Debe recibir la lógica e iniciar la aplicación en la ventana principal.
        """
        super(App_EPorra, self).__init__(sys_argv)
        
        self.logica = logica
        self.mostrar_vista_lista_carreras()
        self.competidores = []
        
    def mostrar_vista_lista_carreras(self):
        """
        Esta función inicializa la ventana de la lista de carreras
        """
        self.vista_lista_carreras = Vista_lista_carreras(self) 
        self.vista_lista_carreras.mostrar_carreras(self.logica.dar_carreras())

    def guardar_carrera(self, nombre, competidores):
        """
        Esta función guarda una nueva carrera o los cambios sobre una existente
        """
        carrera_guardada = False
        if self.carrera_actual == -1:
            carrera_guardada = self.logica.crear_carrera(nombre,competidores)
        else:
            self.logica.editar_carrera(self.carrera_actual, nombre)

        if not(carrera_guardada):
            return False
            
        self.vista_lista_carreras.mostrar_carreras(self.logica.dar_carreras())
        return True

    def dar_competidor(self, id_competidor):
        """
        Esta función retorna la información de un competidor
        """
        return self.logica.dar_competidor(self.carrera_actual, id_competidor)    

    def editar_competidor(self, id_competidor, nombre, probabilidad):
        """
        Esta función edita la información de un competidor en una carrera
        """
        self.logica.editar_competidor(self.carrera_actual, id_competidor, nombre, probabilidad)
    
    def eliminar_competidor(self, id_competidor):
        """
        Esta función elimina un competidor de una carrera
        """
        if self.carrera_actual!=-1:
            self.logica.eliminar_competidor(self.carrera_actual, id_competidor)
        
    def aniadir_apostador(self, nombre):
        """
        Esta función inserta un apostador a la aplicación
        """
        registro_exitoso = self.logica.aniadir_apostador(nombre)
        if not(registro_exitoso):
            titulo = "Error"
            mensaje = "El nombre del apostador debe ser único, no debe ser vacio o superior a 200 caracteres." 
            self.vista_lista_apostadores.mostrar_mensaje(titulo, mensaje)
            
        self.vista_lista_apostadores.mostrar_apostadores(self.logica.dar_apostadores())
        
    def editar_apostador(self, id, nombre):
        """
        Esta función edita la información de un apostador
        """     
        self.logica.editar_apostador(id, nombre)
        self.vista_lista_apostadores.mostrar_apostadores(self.logica.dar_apostadores())

    def mostrar_apostadores(self):
        """
        Esta función muestra la ventana con la lista de apostadores
        """
        self.vista_lista_apostadores=Vista_lista_apostadores(self)
        self.vista_lista_apostadores.mostrar_apostadores(self.logica.dar_apostadores())

    def dar_apostadores(self):
        """
        Esta función retorna la lista de apostadores desde la lógica
        """
        return self.logica.dar_apostadores()

    def dar_competidores(self):
        """
        Esta función retorna la lista de competidores
        """
        return self.logica.dar_competidores_carrera(self.carrera_actual)

    def mostrar_apuestas(self, id_carrera):
        """
        Esta función muestra las apuestas de una carrera
        """
        self.carrera_actual = id_carrera
        nombre_carrera = self.logica.dar_carrera(id_carrera)['Nombre']
        self.vista_lista_apuestas=Vista_lista_apuestas(self, (len(self.logica.carreras[id_carrera]['Competidores']) > 1))
        self.vista_lista_apuestas.mostrar_apuestas(nombre_carrera, self.logica.dar_apuestas_carrera(id_carrera))

    def dar_apuesta(self, id_apuesta):
        """
        Esta función retorna la información de una apuesta particular
        """
        return self.logica.dar_apuesta(self.carrera_actual, id_apuesta)

    def aniadir_apuesta(self, competidor, valor, apostador):
        """
        Esta función crea una nueva apuesta asociada a una carrera
        """
        apuesta_guardada = self.logica.crear_apuesta(apostador, self.carrera_actual, valor, competidor)
        if not(apuesta_guardada):
            self.vista_lista_apuestas.mostrar_mensaje('Error', 
                ('Surgió un error al guardar la Apuesta por uno de los siguientes motivos: \n'
                'La carrera no tiene mínimo dos competidores \n'
                'El valor es obligatorio y debe ser mayor a cero \n'))
        nombre_carrera = self.logica.dar_carrera(self.carrera_actual)['Nombre']

        self.vista_lista_apuestas.mostrar_apuestas(nombre_carrera, self.logica.dar_apuestas_carrera(self.carrera_actual))

    def editar_apuesta(self, id_apuesta, competidor, valor, apostador):
        """
        Esta función edita una apuesta asociada a una carrera
        """
        apuesta_editada = self.logica.editar_apuesta(id_apuesta, apostador, self.carrera_actual, valor, competidor)
        if not(apuesta_editada):
            self.vista_lista_apuestas.mostrar_mensaje('Error', 
                ('Surgió un error al actualizar la Apuesta por uno de los siguientes motivos: \n'
                'El valor es obligatorio y debe ser mayor a cero \n'))
        nombre_carrera = self.logica.dar_carrera(self.carrera_actual)['Nombre']
        self.vista_lista_apuestas.mostrar_apuestas(nombre_carrera, self.logica.dar_apuestas_carrera(self.carrera_actual))

    def eliminar_carrera(self, indice_carrera):
        """
        Esta función elimina una carrera
        """
        carrera_eliminada = self.logica.eliminar_carrera(indice_carrera)
        if not(carrera_eliminada):
            self.vista_lista_carreras.mostrar_mensaje('Error', 
            ('No es posible eliminar la carrera porque tiene apuestas asociadas'))
        
        self.vista_lista_carreras.mostrar_carreras(self.logica.dar_carreras())

    def mostrar_reporte_ganancias(self, id_ganador):
        """
        Esta función muestra el reporte de ganancias para una carrera con apuestas
        """
        lista_ganancias, ganancias_casa = self.logica.dar_reporte_ganancias(self.carrera_actual, id_ganador)
        self.vista_reporte_ganancias = Vista_reporte_ganancias(self)
        self.vista_reporte_ganancias.mostrar_ganancias(lista_ganancias, ganancias_casa)


    def eliminar_apostador(self, id_apostador):
        """
        Esta función elimina un apostador
        """
        self.logica.eliminar_apostador(id_apostador)
        self.vista_lista_apostadores.mostrar_apostadores(self.logica.dar_apostadores())

    def eliminar_apuesta(self, id_apuesta):
        """
        Esta función elimina una apuesta
        """
        resultado = self.logica.eliminar_apuesta(self.carrera_actual, id_apuesta)       
        nombre_carrera = self.logica.dar_carrera(self.carrera_actual)['Nombre']
        self.vista_lista_apuestas.mostrar_apuestas(nombre_carrera, self.logica.dar_apuestas_carrera(self.carrera_actual))
    
    def mostrar_carrera(self, id_carrera=-1):
        """
        Esta función muestra una carrera en la ventana de carreras
        """
        self.carrera_actual = id_carrera
        if id_carrera != -1:
            self.vista_carrera = Vista_carrera(self)
            nombre_carrera = self.logica.dar_carrera(self.carrera_actual)['Nombre']
            self.vista_carrera.mostrar_competidores(nombre_carrera, self.logica.dar_competidores_carrera(self.carrera_actual))
        else:
            self.vista_carrera = Vista_carrera(self)
            self.vista_carrera.mostrar_competidores('',[])

    def aniadir_competidor(self, nombre, probabilidad):
        """
        Esta función inserta un nuevo competidor en una carrera
        """
        self.competidores.append({'Nombre':nombre, 'Probabilidad': probabilidad})
        
        self.logica.aniadir_competidor(self.carrera_actual, nombre, probabilidad)
        nombre_carrera = self.logica.dar_carrera(self.carrera_actual)['Nombre']
        self.vista_carrera.mostrar_competidores(nombre_carrera, self.logica.dar_competidores_carrera(self.carrera_actual))

