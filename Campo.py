from ListaSimpleEnlazada import ListaEnlazada
from Matriz import Matriz

class Campo:
    def __init__(self, id_campo, nombre):
        self.id = id_campo
        self.nombre = nombre
        self.estaciones = ListaEnlazada()
        self.sensores_suelo = ListaEnlazada()
        self.sensores_cultivo = ListaEnlazada()
        self.matriz_suelo = None
        self.matriz_cultivo = None
    
    def crear_matrices(self):
        # Crea y llena las matrices de frecuencias
        num_estaciones = self.estaciones.longitud
        num_sensores_suelo = self.sensores_suelo.longitud
        num_sensores_cultivo = self.sensores_cultivo.longitud
        
        # Crear matrices
        self.matriz_suelo = Matriz(num_estaciones, num_sensores_suelo)
        self.matriz_cultivo = Matriz(num_estaciones, num_sensores_cultivo)
        
        # Llenar matriz de suelo
        for num_columna in range(num_sensores_suelo):
            sensor = self.sensores_suelo.obtener(num_columna)
            actual_frecuencia = sensor.frecuencias.primero
            while actual_frecuencia:
                frecuencia = actual_frecuencia.dato
                num_fila = self.estaciones.buscar_indice(frecuencia.id_estacion)
                if num_fila != -1:
                    self.matriz_suelo.establecer(num_fila, num_columna, frecuencia)
                actual_frecuencia = actual_frecuencia.siguiente
        
        # Llenar matriz de cultivo
        for num_columna in range(num_sensores_cultivo):
            sensor = self.sensores_cultivo.obtener(num_columna)
            actual_frecuencia = sensor.frecuencias.primero
            while actual_frecuencia:
                frecuencia = actual_frecuencia.dato
                num_fila = self.estaciones.buscar_indice(frecuencia.id_estacion)
                if num_fila != -1:
                    self.matriz_cultivo.establecer(num_fila, num_columna, frecuencia)
                actual_frecuencia = actual_frecuencia.siguiente
    
    def mostrar_matrices(self):
        # Muestra ambas matrices del campo
        if self.matriz_suelo:
            titulo_suelo = f"Matriz de Suelo - Campo {self.id}"
            self.matriz_suelo.mostrar(titulo_suelo, self.estaciones, self.sensores_suelo)
        
        if self.matriz_cultivo:
            titulo_cultivo = f"Matriz de Cultivo - Campo {self.id}"
            self.matriz_cultivo.mostrar(titulo_cultivo, self.estaciones, self.sensores_cultivo)

    def visualizar_matrices_graphviz(self):
        """Genera visualizaciones de ambas matrices"""
        if self.matriz_suelo:
            print("Generando visualización de matriz de suelo...")
            self.matriz_suelo.generar_graphviz(
                f"Matriz Suelo - Campo {self.id}",
                self.estaciones,
                self.sensores_suelo,
                f"matriz_suelo_campo_{self.id}"
            )

        if self.matriz_cultivo:
            print("Generando visualización de matriz de cultivo...")
            self.matriz_cultivo.generar_graphviz(
                f"Matriz Cultivo - Campo {self.id}",
                self.estaciones,
                self.sensores_cultivo,
                f"matriz_cultivo_campo_{self.id}"
            )


