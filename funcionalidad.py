import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

# Funciones utilitarias
def generar_matriz_cuadrada(n):
    return [[0 for _ in range(n)] for _ in range(n)]

def es_cuadrada(matriz):
    return all(len(fila) == len(matriz) for fila in matriz)

def encontrar_unos(matriz):
    posiciones = []
    for y, fila in enumerate(matriz):
        for x, valor in enumerate(fila):
            if valor == 1:
                posiciones.append((x, y))
    return posiciones

def calcular_ganancia(array, y, x):
    sumatoria = 0
    for jy in range(max(0, y - 1), min(len(array), y + 2)):
        for jx in range(max(0, x - 1), min(len(array[0]), x + 2)):
            sumatoria += array[jy][jx]
    return sumatoria

def es_contiguo(x, y, ubicaciones_existentes, n):
    for ux, uy in ubicaciones_existentes:
        if max(0, y - 1) <= uy <= min(n - 1, y + 1) and max(0, x - 1) <= ux <= min(n - 1, x + 1):
            return True
    return False

def generar_matriz_ganancias(array, ubicaciones_existentes, minimo_numero):
    n = len(array)
    matriz = generar_matriz_cuadrada(n)
    for y in range(n):
        for x in range(n):
            if es_contiguo(x, y, ubicaciones_existentes, n) or calcular_ganancia(array, y, x) < minimo_numero:
                matriz[y][x] = 0
            else:
                matriz[y][x] = calcular_ganancia(array, y, x)
    return matriz

def ganancia_cotigua(arreglo, y, x):
    sumatoria = 0
    for jy in range(max(0, y - 1), min(len(arreglo), y + 2)):
        for jx in range(max(0, x - 1), min(len(arreglo[0]), x + 2)):
            sumatoria += arreglo[jy][jx]
    return sumatoria

def ganancia(matriz1, matriz2, ubicaciones_existentes):
    suma = 0
    for ux, uy in ubicaciones_existentes:
        suma += ganancia_cotigua(matriz1, uy, ux)
        suma += ganancia_cotigua(matriz2, uy, ux)
    return suma

def formatear_posiciones(posiciones):
    return ', '.join([f"({x}, {y})" for x, y in posiciones])

def actualizar_matriz_salida(matriz_salida, nuevas_sedes):
    for x, y in nuevas_sedes:
        matriz_salida[y][x] = 1
    return matriz_salida

def solucion(poblacion, empresas, ubicaciones_existentes, n_sedes):
    """
    Calcula las nuevas ubicaciones maximizando la ganancia, evitando contigüidad y respetando restricciones.
    """
    matriz_ganancias_poblacion = generar_matriz_ganancias(poblacion, ubicaciones_existentes, 25)
    matriz_ganancias_empresas = generar_matriz_ganancias(empresas, ubicaciones_existentes, 20)

    nuevas_sedes = [(x, y) for x in range(len(poblacion)) for y in range(len(poblacion[0])) if matriz_ganancias_poblacion[y][x] > 0][:n_sedes]

    ganancia_existente = ganancia(poblacion, empresas, ubicaciones_existentes)

    # Crear matriz de salida
    matriz_salida = generar_matriz_cuadrada(len(poblacion))
    for x, y in ubicaciones_existentes:
        matriz_salida[y][x] = 1
    matriz_salida = actualizar_matriz_salida(matriz_salida, nuevas_sedes)

    # Ordenar posiciones antes de formatear
    ubicaciones_existentes = sorted(ubicaciones_existentes, key=lambda pos: (pos[0], pos[1]))
    nuevas_sedes = sorted(nuevas_sedes, key=lambda pos: (pos[0], pos[1]))

    resultado = f"""
Ganancia inicial: {ganancia_existente}
Ganancia final: {ganancia_existente + sum(matriz_ganancias_poblacion[y][x] for x, y in nuevas_sedes)}

Posiciones iniciales ordenadas:
{formatear_posiciones(ubicaciones_existentes)}

Posiciones nuevas ordenadas:
{formatear_posiciones(nuevas_sedes)}

Matriz de salida:
{np.array(matriz_salida)}
"""

    print(resultado)  # Mostrar en consola
    return resultado

def leer_entrada_desde_archivo(nombre_archivo):
    """
    Lee los datos de entrada desde un archivo estructurado.
    Formato:
    - Primera línea: Dimensión de la matriz (n).
    - Siguientes n líneas: Matriz de población.
    - Siguientes n líneas: Matriz empresarial.
    - Línea siguiente: Número de sedes a ubicar.
    - Última línea: Coordenadas de las ubicaciones existentes (como lista de tuplas).
    """
    with open(nombre_archivo, 'r') as archivo:
        lineas = archivo.readlines()

    # Leer dimensión de la matriz
    n = int(lineas[0].strip())

    # Leer matriz de población
    poblacion = []
    for i in range(1, n + 1):
        fila = list(map(int, lineas[i].strip().split()))
        poblacion.append(fila)

    # Leer matriz empresarial
    empresarial = []
    for i in range(n + 1, 2 * n + 1):
        fila = list(map(int, lineas[i].strip().split()))
        empresarial.append(fila)

    # Leer número de nuevas sedes
    n_sedes = int(lineas[2 * n + 1].strip())

    # Leer ubicaciones existentes
    ubicaciones_existentes = eval(lineas[2 * n + 2].strip())

    # Validaciones
    if not es_cuadrada(poblacion) or not es_cuadrada(empresarial) or len(poblacion) != n or len(empresarial) != n:
        raise ValueError("Las matrices de población o empresarial no son cuadradas o no coinciden con la dimensión especificada.")

    if len(ubicaciones_existentes) != len(set(ubicaciones_existentes)):
        raise ValueError("Las ubicaciones existentes tienen valores duplicados.")

    return poblacion, empresarial, ubicaciones_existentes, n_sedes

def solucion_archivo():
    """
    Lee los datos de entrada desde un archivo, ejecuta la solución y escribe el resultado en un archivo de salida.
    """
    # Abrir cuadro de diálogo para seleccionar el archivo de entrada
    Tk().withdraw()  # Oculta la ventana principal de Tkinter
    nombre_archivo_entrada = askopenfilename(title="Seleccione el archivo de entrada", filetypes=[("Archivos de texto", "*.txt")])
    if not nombre_archivo_entrada:
        print("No se seleccionó ningún archivo de entrada.")
        return

    nombre_archivo_salida = asksaveasfilename(title="Seleccione dónde guardar el archivo de salida", defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
    if not nombre_archivo_salida:
        print("No se seleccionó ningún archivo de salida.")
        return

    poblacion, empresarial, ubicaciones_existentes, n_sedes = leer_entrada_desde_archivo(nombre_archivo_entrada)

    # Ejecutar solución
    resultado = solucion(poblacion, empresarial, ubicaciones_existentes, n_sedes)

    # Escribir resultado en archivo de salida
    with open(nombre_archivo_salida, 'w') as salida:
        salida.write(resultado)

if __name__ == "__main__":
    solucion_archivo()
