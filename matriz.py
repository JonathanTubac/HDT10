"""
    Hoja de Trabajo 10 - Algoritmos y Estructuras de Datos
    Carlos López - 24531
    Jonathan Tubac - 24...
"""

import sys
import math

INF = math.inf

class Logistica:
    def __init__(self):
        self.ciudades = []  
        self.indice = {}  
        self.tiempo = {}  
        self.t_actual = 'normal' 
        self.dist = None  # este es el resultado de la distuancia una vez usado floyd
        self.next = None  # este es el resutlado para el siguiente nodo una vez usado floyd

    def cargarDatos(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            lineas_usadas = [ln.strip() for ln in f if ln.strip()]

        nombreCiudad = set()
        conexiones = []
        
        for linea in lineas_usadas:
            ciudad1, ciudad2, tiempoNormal, tiempoLLuvia, tiempoNieve, tiempoTormenta = linea.split()
            nombreCiudad.add(ciudad1); nombreCiudad.add(ciudad2)
            conexiones.append((ciudad1, ciudad2, float(tiempoNormal), float(tiempoLLuvia), float(tiempoNieve), float(tiempoTormenta)))

        self.ciudades = sorted(nombreCiudad)
        numCiudades = len(self.ciudades)
        self.indice = {ciudad: i for i, ciudad in enumerate(self.ciudades)}
        
        tipoClima = ['normal', 'lluvia', 'nieve', 'tormenta']
        for clima in tipoClima:
            matriz = [[INF] * numCiudades for _ in range(numCiudades)]
            for i in range(numCiudades):
                matriz[i][i] = 0  
            self.tiempo[clima] = matriz
        
        for conexion in conexiones:
            origen, destino, *tiempos = conexion
            origen = self.indice[origen]
            destino = self.indice[destino]
            
            for i, clima in enumerate(tipoClima):
                tiempo = tiempos[i]
                self.tiempo[clima][origen][destino] = tiempo
                self.tiempo[clima][destino][origen] = tiempo

    def mostrar_matriz(self):
        total = len(self.ciudades)
        matriz_clima = self.tiempo[self.t_actual]
        
        encabezado = ['Ciudad'] + self.ciudades
        filas = [encabezado]
        
        for indice, ciudad in enumerate(self.ciudades):
            valores = [
                str(t) if t < INF else '∞' 
                for t in matriz_clima[indice]
            ]
            filas.append([ciudad] + valores)
        
        anchos = [max(len(str(item)) for item in columna) for columna in zip(*filas)]
        
        for fila in filas:
            linea_formateada = '  '.join(
                elemento.ljust(anchos[i]) 
                for i, elemento in enumerate(fila)
            )
            print(linea_formateada)

def main():
    net = Logistica()
    try:
        net.cargarDatos('logistica.txt')
    except Exception as e:
        print(f"Error leyendo archivo: {e}")
        sys.exit(1)

    cond = True

    while cond == True:
        print("\nBienvenido a la aplicación de logística entre ciudades, ¿qué desea hacer?")
        print("1. Buscar la ruta más corta entre dos ciudades")
        print("2. Ciudad centro del grafo")
        print("3. Modificar el grafo")
        print("4. Mostrar la matriz de distancias para el estado actual")
        print("5. Salir de la aplicación")
        
        opcion = input("Seleccione una opción: ")
        if opcion == '1':
            print("hola")
        elif opcion == '4':
            print("Mostrando matriz de distancias")
            net.mostrar_matriz()
        elif opcion == '5':
            print("Saliendo de la aplicación...")
            cond = False
        else:
            print("Opción no existente, intente de nuevo.")

if __name__ == '__main__':
    main()

