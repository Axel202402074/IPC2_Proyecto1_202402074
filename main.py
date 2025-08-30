from SistemaAgricultura import SistemaAgricultura
from Campo import Campo
from Matriz import Matriz

def mostrar_datos_estudiante():
    print("DATOS DEL ESTUDIANTE")

    print("➢ Nombre : Axel David González Molina")
    print("➢ Carnet : 202402074")
    print("➢ Introducción a la Programación y Computación 2")
    print("➢ Sección : `C` ")
    print("➢ 4to. Semestre")
    print("➢ Enlace a documentación: https://github.com/Axel202402074/IPC2_Proyecto1_202402074 ")


def escribir_archivo_salida(sistema):
    if sistema.campos.longitud == 0:
        print("Error: No hay campos cargados")
        return
    
    # Verificar si hay campos procesados
    hay_procesados = False
    actual = sistema.campos.primero
    while actual:
        campo = actual.dato
        if hasattr(campo, 'estaciones_reducidas') and campo.estaciones_reducidas:
            hay_procesados = True
            break
        actual = actual.siguiente
    
    if not hay_procesados:
        print("Error: Debe procesar los campos primero")
        return
    
    print("\nEscribir archivo de salida:")
    ruta = input("Ingrese la ruta del archivo: ")
    nombre = input("Ingrese el nombre del archivo: ")
    
    # Construir ruta completa
    if ruta:
        archivo_salida = ruta + "/" + nombre
    else:
        archivo_salida = nombre
    
    # Asegurar extensión .xml
    if not archivo_salida.endswith('.xml'):
        archivo_salida += '.xml'
    
    try:
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0"?>\n')
            f.write('<camposAgricolas>\n')
            
            # Escribir cada campo procesado
            actual = sistema.campos.primero
            while actual:
                campo = actual.dato
                if hasattr(campo, 'estaciones_reducidas') and campo.estaciones_reducidas:
                    f.write(f'    <campo id="{campo.id}" nombre="{campo.nombre}">\n')
                    
                    # Escribir estaciones base reducidas
                    f.write('        <estacionesBaseReducidas>\n')
                    actual_est = campo.estaciones_reducidas.primero
                    while actual_est:
                        estacion = actual_est.dato
                        f.write(f'            <estacion id="{estacion.id}" nombre="{estacion.nombre}"/>\n')
                        actual_est = actual_est.siguiente
                    f.write('        </estacionesBaseReducidas>\n')
                    
                    # Escribir sensores de suelo con frecuencias reducidas
                    f.write('        <sensoresSuelo>\n')
                    for i in range(campo.sensores_suelo.longitud):
                        sensor = campo.sensores_suelo.obtener(i)
                        f.write(f'            <sensorS id="{sensor.id}" nombre="{sensor.nombre}">\n')
                        
                        # Escribir frecuencias reducidas
                        for j in range(campo.estaciones_reducidas.longitud):
                            frecuencia = campo.matriz_suelo_reducida.obtener(j, i)
                            if int(frecuencia.valor) > 0:  # Solo escribir si la frecuencia > 0
                                estacion_red = campo.estaciones_reducidas.obtener(j)
                                f.write(f'                <frecuencia idEstacion="{estacion_red.id}"> {frecuencia.valor} </frecuencia>\n')
                        
                        f.write('            </sensorS>\n')
                    f.write('        </sensoresSuelo>\n')
                    
                    # Escribir sensores de cultivo con frecuencias reducidas
                    f.write('        <sensoresCultivo>\n')
                    for i in range(campo.sensores_cultivo.longitud):
                        sensor = campo.sensores_cultivo.obtener(i)
                        f.write(f'            <sensorT id="{sensor.id}" nombre="{sensor.nombre}">\n')
                        
                        # Escribir frecuencias reducidas
                        for j in range(campo.estaciones_reducidas.longitud):
                            frecuencia = campo.matriz_cultivo_reducida.obtener(j, i)
                            if int(frecuencia.valor) > 0:  # Solo escribir si la frecuencia > 0
                                estacion_red = campo.estaciones_reducidas.obtener(j)
                                f.write(f'                <frecuencia idEstacion="{estacion_red.id}"> {frecuencia.valor} </frecuencia>\n')
                        
                        f.write('            </sensorT>\n')
                    f.write('        </sensoresCultivo>\n')
                    f.write('    </campo>\n')
                
                actual = actual.siguiente
            
            f.write('</camposAgricolas>\n')
        
        print(f"✓ Archivo de salida generado exitosamente: {archivo_salida}")
        
    except Exception as e:
        print(f"Error al escribir archivo de salida: {e}")

def generar_grafica(sistema):
    if sistema.campos.longitud == 0:
        print("Error: No hay campos cargados")
        return
    
    print("\nGenerar gráfica:")
    sistema.listar_campos()
    id_campo = input("Ingrese el ID del campo: ")
    
    # Buscar el campo
    actual = sistema.campos.primero
    campo_encontrado = None
    while actual:
        campo = actual.dato
        if campo.id == id_campo:
            campo_encontrado = campo
            break
        actual = actual.siguiente
    
    if not campo_encontrado:
        print(f"Campo {id_campo} no encontrado")
        return
    
    # Menú de tipos de matriz
    print("\nSeleccione el tipo de matriz a graficar:")
    print("1. Matriz de frecuencias original")
    print("2. Matriz de patrones")
    print("3. Matriz reducida")
    
    opcion_matriz = input("Seleccione una opción: ")
    
    if opcion_matriz == "1":
        # Matriz de frecuencias original
        print("Generando gráficas de matrices de frecuencias...")
        if campo_encontrado.matriz_suelo:
            campo_encontrado.matriz_suelo.generar_graphviz_tabla(
                f"Matriz de Frecuencias Suelo - Campo {campo_encontrado.id}",
                campo_encontrado.estaciones,
                campo_encontrado.sensores_suelo,
                f"frecuencias_suelo_campo_{campo_encontrado.id}"
            )
        
        if campo_encontrado.matriz_cultivo:
            campo_encontrado.matriz_cultivo.generar_graphviz_tabla(
                f"Matriz de Frecuencias Cultivo - Campo {campo_encontrado.id}",
                campo_encontrado.estaciones,
                campo_encontrado.sensores_cultivo,
                f"frecuencias_cultivo_campo_{campo_encontrado.id}"
            )
    
    elif opcion_matriz == "2":
        # Matriz de patrones
        if not hasattr(campo_encontrado, 'matriz_patron_suelo') or not campo_encontrado.matriz_patron_suelo:
            print("Error: Debe procesar el agrupamiento primero (opción 2)")
            return
        
        print("Generando gráficas de matrices de patrones...")
        campo_encontrado.matriz_patron_suelo.generar_graphviz_tabla(
            f"Matriz de Patrones Suelo - Campo {campo_encontrado.id}",
            campo_encontrado.estaciones,
            campo_encontrado.sensores_suelo,
            f"patrones_suelo_campo_{campo_encontrado.id}"
        )
        
        campo_encontrado.matriz_patron_cultivo.generar_graphviz_tabla(
            f"Matriz de Patrones Cultivo - Campo {campo_encontrado.id}",
            campo_encontrado.estaciones,
            campo_encontrado.sensores_cultivo,
            f"patrones_cultivo_campo_{campo_encontrado.id}"
        )
    
    elif opcion_matriz == "3":
        # Matriz reducida
        if not hasattr(campo_encontrado, 'matriz_suelo_reducida') or not campo_encontrado.matriz_suelo_reducida:
            print("Error: Debe procesar el agrupamiento primero (opción 2)")
            return
        
        print("Generando gráficas de matrices reducidas...")
        campo_encontrado.matriz_suelo_reducida.generar_graphviz_tabla(
            f"Matriz Reducida Suelo - Campo {campo_encontrado.id}",
            campo_encontrado.estaciones_reducidas,
            campo_encontrado.sensores_suelo,
            f"reducida_suelo_campo_{campo_encontrado.id}"
        )
        
        campo_encontrado.matriz_cultivo_reducida.generar_graphviz_tabla(
            f"Matriz Reducida Cultivo - Campo {campo_encontrado.id}",
            campo_encontrado.estaciones_reducidas,
            campo_encontrado.sensores_cultivo,
            f"reducida_cultivo_campo_{campo_encontrado.id}"
        )
    
    else:
        print("Opción no válida")

def main():
    sistema = SistemaAgricultura()
    
    while True:
        print("\n" + "="*50)
        print("| Menu principal                               |") 
        print("| 1. Cargar archivo                            |")
        print("| 2. Procesar archivo                          |")
        print("| 3. Escribir archivo de salida                |")
        print("| 4. Mostrar datos del estudiante              |")
        print("| 5. Generar gráfica                           |")
        print("| 6. Salida                                   |")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            print("\nOpción cargar archivo")
            ruta = input("Ingrese la ruta del archivo: ")
            nombre = input("Ingrese el nombre del archivo: ")
            
            # Construir ruta completa
            if ruta:
                archivo = ruta + "/" + nombre
            else:
                archivo = nombre
            
            sistema.cargar_archivo(archivo)
        
        elif opcion == "2":
            print("\nOpción procesar archivo")
            sistema.procesar_campos()
        
        elif opcion == "3":
            print("\nOpción generar archivo de salida")
            escribir_archivo_salida(sistema)
        
        elif opcion == "4":
            mostrar_datos_estudiante()
        
        elif opcion == "5":
            generar_grafica(sistema)
        
        elif opcion == "6":
            print("Saliendo del programa")
            break
        
        else:
            print("Opción no válida")

if __name__ == "__main__":
    main()