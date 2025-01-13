import random
import math

# --------------------------------------------------------------------------------
# Parámetros del Algoritmo Genético
# --------------------------------------------------------------------------------
LONGITUD_CROMOSOMA = 8       # Representa valores de x en [0..255]
TAMANO_POBLACION = 30        # Número de individuos
PROB_CRUZA = 0.7             # Probabilidad de cruza
PROB_MUTACION = 0.02         # Probabilidad de mutación
GENERACIONES = 60            # Número de generaciones
ALPHA = (4.0 * math.pi) / 256.0  # Parámetro para f(x) = x * sin(ALPHA * x)

# Parámetros de Sharing
SIGMA_SHARE = 5.0  # Radio de nicho en el fenotipo (ajústalo según convenga)
SHARE_ALPHA = 1.0  # Exponente para la función de sharing

# --------------------------------------------------------------------------------
# Función objetivo: f(x) = x * sin(ALPHA * x)
# --------------------------------------------------------------------------------
def funcion_objetivo(x):
    return x * math.sin(ALPHA * x)

# --------------------------------------------------------------------------------
# Representación (genotipo-fenotipo)
# --------------------------------------------------------------------------------
def generar_cromosoma():
    """Genera un cromosoma aleatorio de 8 bits."""
    return ''.join(random.choice(['0','1']) for _ in range(LONGITUD_CROMOSOMA))

def decodificar(cromosoma):
    """Convierte el genotipo binario (cadena) a un valor entero (fenotipo)."""
    return int(cromosoma, 2)  # de 0 a 255

# --------------------------------------------------------------------------------
# Fitness básico (sin sharing)
# --------------------------------------------------------------------------------
def fitness_original(cromosoma):
    """Evalúa la función objetivo y devuelve su valor."""
    x = decodificar(cromosoma)
    return funcion_objetivo(x)

# --------------------------------------------------------------------------------
# Distancia fenotípica (en 1D basta la diferencia absoluta)
# --------------------------------------------------------------------------------
def distancia_fenotipica(ind1, ind2):
    x1 = decodificar(ind1)
    x2 = decodificar(ind2)
    return abs(x1 - x2)

# --------------------------------------------------------------------------------
# Función de Sharing: sh(d)
# --------------------------------------------------------------------------------
def sharing_function(distance):
    """Aplica la función de sharing en función de la distancia."""
    if distance < SIGMA_SHARE:
        return 1.0 - (distance / SIGMA_SHARE) ** SHARE_ALPHA
    else:
        return 0.0

# --------------------------------------------------------------------------------
# Cálculo de Fitness Compartido para cada individuo
# --------------------------------------------------------------------------------
def fitness_compartido(poblacion):
    """
    Devuelve una lista con la fitness compartida de cada individuo en la población.
    shared_fitness(i) = fitness_original(i) / sum_j( sh(dist(i,j)) ).
    """
    # Calculamos la fitness original de todos
    fitness_vals = [fitness_original(ind) for ind in poblacion]
    N = len(poblacion)

    # Para cada individuo, calculamos la suma de sharing function con los demás.
    shared_fits = []
    for i in range(N):
        dist_sum = 0.0
        for j in range(N):
            dist_ij = distancia_fenotipica(poblacion[i], poblacion[j])
            dist_sum += sharing_function(dist_ij)
        # Evitar dividir por cero en caso extremo
        if dist_sum == 0:
            dist_sum = 1e-9
        shared_fits.append(fitness_vals[i] / dist_sum)

    return shared_fits

# --------------------------------------------------------------------------------
# SELECCIÓN (por Ruleta) usando fitness compartido
# --------------------------------------------------------------------------------
def seleccionar_ruleta(poblacion):
    """
    Selección por ruleta usando la fitness compartida como probabilidad.
    Se eligen 2 padres de la misma población.
    """
    shared_fits = fitness_compartido(poblacion)
    total_fitness = sum(shared_fits)

    def ruleta():
        r = random.random() * total_fitness
        acum = 0.0
        for i, ind in enumerate(poblacion):
            acum += shared_fits[i]
            if acum >= r:
                return ind
        return poblacion[-1]

    # Elegir 2 padres
    padre1 = ruleta()
    padre2 = ruleta()
    return padre1, padre2

# --------------------------------------------------------------------------------
# Operadores de Cruza y Mutación
# --------------------------------------------------------------------------------
def cruzar(padre1, padre2):
    """Cruce de 1 punto."""
    if random.random() < PROB_CRUZA:
        punto = random.randint(1, LONGITUD_CROMOSOMA - 1)
        left_p1, right_p1 = padre1[:punto], padre1[punto:]
        left_p2, right_p2 = padre2[:punto], padre2[punto:]
        hijo1 = left_p1 + right_p2
        hijo2 = left_p2 + right_p1
        return hijo1, hijo2
    else:
        return padre1, padre2

def mutar(cromosoma):
    """Mutación bit a bit con PROB_MUTACION."""
    crom_list = list(cromosoma)
    for i in range(LONGITUD_CROMOSOMA):
        if random.random() < PROB_MUTACION:
            crom_list[i] = '1' if crom_list[i] == '0' else '0'
    return ''.join(crom_list)

# --------------------------------------------------------------------------------
# Mejores individuos (ordenados por fitness original, no compartido)
# --------------------------------------------------------------------------------
def mejores_individuos(poblacion, n=5):
    """Retorna los n mejores individuos según fitness original."""
    return sorted(poblacion, key=fitness_original, reverse=True)[:n]

# --------------------------------------------------------------------------------
# ALGORITMO GENÉTICO MULTIMODAL
# --------------------------------------------------------------------------------
def algoritmo_genetico_multimodal():
    # 1. Generar población inicial
    poblacion = [generar_cromosoma() for _ in range(TAMANO_POBLACION)]

    for gen in range(GENERACIONES):
        nueva_poblacion = []
        # 2. Generar descendencia
        while len(nueva_poblacion) < TAMANO_POBLACION:
            padre1, padre2 = seleccionar_ruleta(poblacion)
            hijo1, hijo2 = cruzar(padre1, padre2)
            hijo1 = mutar(hijo1)
            hijo2 = mutar(hijo2)
            nueva_poblacion.append(hijo1)
            if len(nueva_poblacion) < TAMANO_POBLACION:
                nueva_poblacion.append(hijo2)

        poblacion = nueva_poblacion

        # 3. Imprimir top de la generación (puede ser un vistazo de diversidad)
        top = mejores_individuos(poblacion, n=3)
        top_info = ", ".join(
            f"x={decodificar(ind)} (f={funcion_objetivo(decodificar(ind)):.2f})"
            for ind in top
        )
        print(f"Generación {gen+1:02d} | Top 3: {top_info}")

    # 4. Resultado final
    print("\n=== Población final (Top 5) ===")
    top5 = mejores_individuos(poblacion, n=5)
    for ind in top5:
        x_val = decodificar(ind)
        print(f"Cromosoma: {ind}, x={x_val}, f(x)={funcion_objetivo(x_val):.4f}")

# --------------------------------------------------------------------------------
# EJECUCIÓN
# --------------------------------------------------------------------------------
if __name__ == "__main__":
    algoritmo_genetico_multimodal()

'''
Con este algoritmo multimodal verás que no necesariamente obtendrás 
un solo “Mejor Cromosoma” al final, sino varios individuos en la 
población final con valores distintos de 
𝑥
x pero con fitness similar, indicando que el GA ha mantenido 
nichos en múltiples picos de la función. De esta forma, obtienes 
una búsqueda global más amplia y varias soluciones que pueden ser 
óptimas o cercanas al óptimo.
'''