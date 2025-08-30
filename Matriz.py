from ListaSimpleEnlazada import ListaEnlazada
from Frecuencia import Frecuencia

class Matriz:
    def __init__(self, num_filas, num_columnas):
        self.num_filas = num_filas
        self.num_columnas = num_columnas
        self.matriz = ListaEnlazada()
        
        # Crear matriz inicializada con ceros
        for i in range(num_filas):
            fila = ListaEnlazada()
            for j in range(num_columnas):
                frecuencia = Frecuencia("", "0")
                fila.insertar(frecuencia)
            self.matriz.insertar(fila)
    
    def establecer(self, num_fila, num_columna, frecuencia):
        # Establece un valor en la posicion [fila, columna]
        fila = self.matriz.obtener(num_fila)
        if fila:
            # Buscar el nodo en la columna especifica
            columna = fila.primero
            for i in range(num_columna):
                if columna:
                    columna = columna.siguiente
            if columna:
                columna.dato = frecuencia
    
    def obtener(self, num_fila, num_columna):
        # Obtiene el valor en la posicion [fila, columna]
        fila = self.matriz.obtener(num_fila)
        if fila:
            return fila.obtener(num_columna)
        return None
    
    def mostrar(self, titulo, headers_fila, headers_columna):
        # Muestra la matriz de forma tabular
        print(f"\n{titulo}")
        print("=" * 50)
        
        # Headers de columnas
        print("Estacion\\Sensor", end="\t")
        for j in range(self.num_columnas):
            sensor = headers_columna.obtener(j)
            print(f"{sensor.id}", end="\t")
        print()
        
        # Filas con datos
        for i in range(self.num_filas):
            estacion = headers_fila.obtener(i)
            print(f"{estacion.id}", end="\t\t")
            for j in range(self.num_columnas):
                frecuencia = self.obtener(i, j)
                print(f"{frecuencia.valor}", end="\t")
            print()

    def generar_graphviz_tabla(self, titulo, headers_fila, headers_columna, nombre_archivo="matriz_tabla"):
        """
        Genera un archivo DOT con una tabla HTML válida para Graphviz.
        """
        def esc(s):
            return str(s).replace('"', '\\"')

        # Construir cabecera de columnas
        th_cols = '<td border="1" bgcolor="#f5f7fa"></td>'  # celda vacía de esquina
        for j in range(self.num_columnas):
            sensor = headers_columna.obtener(j)
            th_cols += f'<td border="1" bgcolor="#f5f7fa"><b>{esc(sensor.id)}</b></td>'

        # Construir filas
        filas_html = ""
        for i in range(self.num_filas):
            estacion = headers_fila.obtener(i)
            filas_html += f'<tr><td border="1" bgcolor="#f5f7fa"><b>{esc(estacion.id)}</b></td>'
            for j in range(self.num_columnas):
                frecuencia = self.obtener(i, j)
                valor = esc(frecuencia.valor) if frecuencia and hasattr(frecuencia, "valor") else "0"
                bg = "#ffffff" if valor == "0" else "#ffd6d6"
                filas_html += f'<td border="1" bgcolor="{bg}">{valor}</td>'
            filas_html += '</tr>\n'

        # Tabla HTML anidada
        tabla = f'''<<table BORDER="0" CELLBORDER="0" CELLSPACING="0">
<tr><td>
<table BORDER="1" CELLBORDER="1" CELLSPACING="0">
<tr>{th_cols}</tr>
{filas_html}
</table>
</td></tr>
</table>>'''

        # Escribir archivo DOT manualmente (sin usar graphviz.Digraph para evitar problemas de encoding)
        with open(f'{nombre_archivo}.dot', 'w', encoding='utf-8') as f:
            f.write('digraph {\n')
            f.write('    rankdir=LR\n')
            f.write(f'    matriz_tabla [label={tabla} shape=plain]\n')
            f.write(f'    titulo [label="{titulo}" fillcolor=lightgreen shape=box style=filled]\n')
            f.write('    titulo -> matriz_tabla [style=invis]\n')
            f.write('}\n')

        print(f"Archivo DOT generado: {nombre_archivo}.dot")
        print(f"Para generar PNG: dot -Tpng {nombre_archivo}.dot -o {nombre_archivo}.png")