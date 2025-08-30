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
        
        # Nuevos atributos para el agrupamiento
        self.estaciones_reducidas = None
        self.matriz_suelo_reducida = None
        self.matriz_cultivo_reducida = None
        self.matriz_patron_suelo = None
        self.matriz_patron_cultivo = None
        self.grupos_info = None
    
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

    def generar_matrices_patrones(self):
        """Genera las matrices de patrones Fp[n,s] y Fp[n,t]"""
        if not self.matriz_suelo or not self.matriz_cultivo:
            print("Error: Las matrices de frecuencia no han sido creadas")
            return None, None
        
        # Crear matrices de patrones con las mismas dimensiones
        matriz_patron_suelo = Matriz(self.matriz_suelo.num_filas, self.matriz_suelo.num_columnas)
        matriz_patron_cultivo = Matriz(self.matriz_cultivo.num_filas, self.matriz_cultivo.num_columnas)
        
        # Convertir frecuencias a patrones (1 si >0, 0 si =0) - Matriz Suelo
        for i in range(self.matriz_suelo.num_filas):
            for j in range(self.matriz_suelo.num_columnas):
                frecuencia = self.matriz_suelo.obtener(i, j)
                patron_valor = "1" if int(frecuencia.valor) > 0 else "0"
                from Frecuencia import Frecuencia
                patron_freq = Frecuencia("", patron_valor)
                matriz_patron_suelo.establecer(i, j, patron_freq)
        
        # Convertir frecuencias a patrones - Matriz Cultivo
        for i in range(self.matriz_cultivo.num_filas):
            for j in range(self.matriz_cultivo.num_columnas):
                frecuencia = self.matriz_cultivo.obtener(i, j)
                patron_valor = "1" if int(frecuencia.valor) > 0 else "0"
                patron_freq = Frecuencia("", patron_valor)
                matriz_patron_cultivo.establecer(i, j, patron_freq)
        
        return matriz_patron_suelo, matriz_patron_cultivo

    def obtener_patron_fila(self, matriz, num_fila):
        patron = ""
        for j in range(matriz.num_columnas):
            frecuencia = matriz.obtener(num_fila, j)
            if frecuencia:
                patron += str(frecuencia.valor)  # <-- Conversión a string
            else:
                patron += "0"
        return patron

    def encontrar_grupos(self, matriz_patron_suelo, matriz_patron_cultivo):
        """Encuentra grupos de estaciones con patrones idénticos"""
        grupos = {}  # {patron_combinado: [indices_estaciones]}
        
        for i in range(matriz_patron_suelo.num_filas):
            # Obtener patrón combinado de suelo y cultivo
            patron_suelo = self.obtener_patron_fila(matriz_patron_suelo, i)
            patron_cultivo = self.obtener_patron_fila(matriz_patron_cultivo, i)
            patron_combinado = patron_suelo + "|" + patron_cultivo
            
            if patron_combinado not in grupos:
                grupos[patron_combinado] = []
            grupos[patron_combinado].append(i)
        
        return grupos

    def crear_matrices_reducidas(self, grupos):
        """Crea las matrices reducidas agrupando estaciones con patrones similares"""
        from ListaSimpleEnlazada import ListaEnlazada
        from Estacion import Estacion
        
        # Crear nueva lista de estaciones reducidas
        estaciones_reducidas = ListaEnlazada()
        mapeo_indices = {}  # {indice_original: indice_reducido}
        
        indice_reducido = 0
        for patron, indices_estaciones in grupos.items():
            if len(indices_estaciones) == 1:
                # Estación individual
                estacion_original = self.estaciones.obtener(indices_estaciones[0])
                estacion_nueva = Estacion(estacion_original.id, estacion_original.nombre)
            else:
                # Estaciones agrupadas
                nombres_agrupados = []
                ids_agrupados = []
                for idx in indices_estaciones:
                    estacion = self.estaciones.obtener(idx)
                    nombres_agrupados.append(estacion.nombre)
                    ids_agrupados.append(estacion.id)
                
                # Usar el ID de la primera estación para la agrupada
                id_agrupado = ids_agrupados[0]
                nombre_agrupado = ", ".join(nombres_agrupados)
                estacion_nueva = Estacion(id_agrupado, nombre_agrupado)
            
            estaciones_reducidas.insertar(estacion_nueva)
            
            # Mapear todos los indices originales al nuevo indice reducido
            for idx_original in indices_estaciones:
                mapeo_indices[idx_original] = indice_reducido
            
            indice_reducido += 1
        
        # Crear matrices reducidas
        num_estaciones_reducidas = estaciones_reducidas.longitud
        matriz_suelo_reducida = Matriz(num_estaciones_reducidas, self.sensores_suelo.longitud)
        matriz_cultivo_reducida = Matriz(num_estaciones_reducidas, self.sensores_cultivo.longitud)
        
        # Llenar matrices reducidas sumando frecuencias de estaciones agrupadas
        indice_grupo = 0
        for patron, indices_estaciones in grupos.items():
            # Sumar frecuencias para sensores de suelo
            for j in range(self.sensores_suelo.longitud):
                suma_frecuencia = 0
                id_estacion_referencia = ""
                
                for idx_original in indices_estaciones:
                    frecuencia_original = self.matriz_suelo.obtener(idx_original, j)
                    suma_frecuencia += int(frecuencia_original.valor)
                    if not id_estacion_referencia:
                        id_estacion_referencia = frecuencia_original.id_estacion
                
                from Frecuencia import Frecuencia
                frecuencia_sumada = Frecuencia(id_estacion_referencia, str(suma_frecuencia))
                matriz_suelo_reducida.establecer(indice_grupo, j, frecuencia_sumada)
            
            # Sumar frecuencias para sensores de cultivo
            for j in range(self.sensores_cultivo.longitud):
                suma_frecuencia = 0
                id_estacion_referencia = ""
                
                for idx_original in indices_estaciones:
                    frecuencia_original = self.matriz_cultivo.obtener(idx_original, j)
                    suma_frecuencia += int(frecuencia_original.valor)
                    if not id_estacion_referencia:
                        id_estacion_referencia = frecuencia_original.id_estacion
                
                frecuencia_sumada = Frecuencia(id_estacion_referencia, str(suma_frecuencia))
                matriz_cultivo_reducida.establecer(indice_grupo, j, frecuencia_sumada)
            
            indice_grupo += 1
        
        return estaciones_reducidas, matriz_suelo_reducida, matriz_cultivo_reducida

    def procesar_agrupamiento(self):
        """Método principal que ejecuta todo el proceso de agrupamiento"""
        print(f"Procesando campo {self.id}...")
        
        # Paso 1: Generar matrices de patrones
        print("→ Generando matrices de patrones...")
        matriz_patron_suelo, matriz_patron_cultivo = self.generar_matrices_patrones()
        
        if not matriz_patron_suelo or not matriz_patron_cultivo:
            return False
        
        # Paso 2: Encontrar grupos
        print("→ Identificando grupos de estaciones con patrones similares...")
        grupos = self.encontrar_grupos(matriz_patron_suelo, matriz_patron_cultivo)
        
        # Mostrar información de agrupamiento
        estaciones_originales = self.estaciones.longitud
        grupos_resultantes = len(grupos)
        print(f"→ Estaciones originales: {estaciones_originales}")
        print(f"→ Grupos encontrados: {grupos_resultantes}")
        print(f"→ Optimización: {estaciones_originales - grupos_resultantes} estaciones reducidas")
        
        # Paso 3: Crear matrices reducidas
        print("→ Creando matrices reducidas...")
        estaciones_reducidas, matriz_suelo_reducida, matriz_cultivo_reducida = self.crear_matrices_reducidas(grupos)
        
        # Guardar resultados
        self.estaciones_reducidas = estaciones_reducidas
        self.matriz_suelo_reducida = matriz_suelo_reducida
        self.matriz_cultivo_reducida = matriz_cultivo_reducida
        self.matriz_patron_suelo = matriz_patron_suelo
        self.matriz_patron_cultivo = matriz_patron_cultivo
        self.grupos_info = grupos
        
        print(f"✓ Campo {self.id} procesado exitosamente")
        return True

    def mostrar_resultados_agrupamiento(self):
        """Muestra los resultados del proceso de agrupamiento"""
        if not hasattr(self, 'estaciones_reducidas'):
            print("Error: Debe procesar el agrupamiento primero")
            return
        
        print(f"\n{'='*60}")
        print(f"RESULTADOS DE OPTIMIZACIÓN - CAMPO {self.id}")
        print(f"{'='*60}")
        
        print("\n--- MATRIZ DE PATRONES SUELO ---")
        if hasattr(self, 'matriz_patron_suelo'):
            self.matriz_patron_suelo.mostrar(
                f"Patrones Suelo - Campo {self.id}", 
                self.estaciones, 
                self.sensores_suelo
            )
        
        print("\n--- MATRIZ DE PATRONES CULTIVO ---")
        if hasattr(self, 'matriz_patron_cultivo'):
            self.matriz_patron_cultivo.mostrar(
                f"Patrones Cultivo - Campo {self.id}", 
                self.estaciones, 
                self.sensores_cultivo
            )
        
        print("\n--- MATRIZ REDUCIDA SUELO ---")
        if hasattr(self, 'matriz_suelo_reducida'):
            self.matriz_suelo_reducida.mostrar(
                f"Matriz Reducida Suelo - Campo {self.id}", 
                self.estaciones_reducidas, 
                self.sensores_suelo
            )
        
        print("\n--- MATRIZ REDUCIDA CULTIVO ---")
        if hasattr(self, 'matriz_cultivo_reducida'):
            self.matriz_cultivo_reducida.mostrar(
                f"Matriz Reducida Cultivo - Campo {self.id}", 
                self.estaciones_reducidas, 
                self.sensores_cultivo
            )