from SistemaAgricultura import SistemaAgricultura
from Campo import Campo
from Matriz import Matriz

def main():
    sistema = SistemaAgricultura()
    
    while True:
        print("---------------------------------------")
        print("| SISTEMA DE AGRICULTURA DE PRECISION |")
        print("---------------------------------------")
        print("|1. Cargar archivo                    |")
        print("|2. Mostrar matrices                  |")
        print("|3. Graficar matrices                 |")
        print("|4. Salir                             |")
        print("---------------------------------------")
        opcion = input("Seleccione una opcion: ")
        
        if opcion == "1":
            print("\nCargar archivo:")
            ruta = input("Ingrese la ruta del archivo: ")
            nombre = input("Ingrese el nombre del archivo: ")
            archivo = ruta + "/" + nombre if ruta else nombre
            sistema.cargar_archivo(archivo)

        elif opcion == "2":
            print("\nMostrar matrices:")
            sistema.listar_campos()
            id_campo = input("Ingrese el ID del campo: ")
            sistema.mostrar_campo(id_campo)

        elif opcion == "3":
            print("\nGraficar matrices con Graphviz:")
            sistema.listar_campos()
            id_campo = input("Ingrese el ID del campo: ")

            # Buscar el campo y graficar
            actual = sistema.campos.primero
            encontrado = False
            while actual:
                campo = actual.dato
                if campo.id == id_campo:
                    campo.matriz_suelo.generar_graphviz_tabla(
                        f"Matriz de Suelo - Campo {campo.id}",
                        campo.estaciones,
                        campo.sensores_suelo,
                        f"matriz_suelo_tabla_campo_{campo.id}"
                    )
                    encontrado = True
                    break
                actual = actual.siguiente
            if not encontrado:
                print(f"Campo {id_campo} no encontrado")

        elif opcion == "4":
            print("Ejecucion Finalizada...")
            break

        else:
            print("Opcion no valida")

if __name__ == "__main__":
    main()