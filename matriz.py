"""
    Hoja de Trabajo 10 - Algoritmos y Estructuras de Datos
    Carlos López - 24531
    Jonathan Tubac - 24484
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
    def floyd(self):
        n = len(self.ciudades)
        matriz = self.tiempo[self.t_actual]
        self.dist = [row[:] for row in matriz]
        self.next = [[None if matriz[i][j] == INF else j for j in range(n)] for i in range(n)]

        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if self.dist[i][k] + self.dist[k][j] < self.dist[i][j]:
                        self.dist[i][j] = self.dist[i][k] + self.dist[k][j]
                        self.next[i][j] = self.next[i][k]
           
    def centro_del_grafo(self):
        if self.dist is None:
            self.floyd()

        excentricidades = [max(fila) for fila in self.dist]
        min_ex = min(excentricidades)
        centro = self.ciudades[excentricidades.index(min_ex)]
        return centro

    def obtener_ruta(self, origen, destino):
        if self.dist is None or self.next is None:
            self.floyd()

        i = self.indice.get(origen)
        j = self.indice.get(destino)
        if i is None or j is None:
            return None, []

        if self.next[i][j] is None:
            return INF, []

        ruta = [origen]
        while i != j:
            i = self.next[i][j]
            ruta.append(self.ciudades[i])
        
        return self.dist[self.indice[origen]][self.indice[destino]], ruta
    
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
            origen = input("Ciudad de origen: ").strip()
            destino = input("Ciudad de destino: ").strip()
            distancia, ruta = net.obtener_ruta(origen, destino)
            if distancia == INF:
                print("No hay ruta disponible entre esas ciudades.")
            else:
                print(f"Ruta más corta ({net.t_actual}): {' -> '.join(ruta)}")
                print(f"Tiempo total: {distancia:.2f} horas")
        elif opcion == '2':
            centro = net.centro_del_grafo()
            print(f"La ciudad centro del grafo es: {centro}")
        elif opcion == '3':
            print("1. Eliminar conexión entre ciudades")
            print("2. Agregar conexión nueva")
            print("3. Cambiar el tipo de clima actual")
            subop = input("Elija una opción: ")

            if subop == '1':
                c1 = input("Ciudad 1: ").strip()
                c2 = input("Ciudad 2: ").strip()
                if c1 in net.indice and c2 in net.indice:
                    for clima in net.tiempo:
                        i, j = net.indice[c1], net.indice[c2]
                        net.tiempo[clima][i][j] = INF
                        net.tiempo[clima][j][i] = INF
                    print("Conexión eliminada.")
                else:
                    print("Ciudades inválidas.")

            elif subop == '2':
                c1 = input("Ciudad 1: ").strip()
                c2 = input("Ciudad 2: ").strip()
                tiempos = []
                for clima in ['normal', 'lluvia', 'nieve', 'tormenta']:
                    t = float(input(f"Tiempo con {clima}: "))
                    tiempos.append(t)
                for i, clima in enumerate(['normal', 'lluvia', 'nieve', 'tormenta']):
                    i1, i2 = net.indice[c1], net.indice[c2]
                    net.tiempo[clima][i1][i2] = tiempos[i]
                    net.tiempo[clima][i2][i1] = tiempos[i]
                print("Conexión añadida.")

            elif subop == '3':
                clima = input("Clima actual (normal, lluvia, nieve, tormenta): ").strip().lower()
                if clima in ['normal', 'lluvia', 'nieve', 'tormenta']:
                    net.t_actual = clima
                    print(f"Clima actualizado a: {clima}")
                else:
                    print("Tipo de clima inválido.")

                net.floyd()  # Recalcular distancias

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

