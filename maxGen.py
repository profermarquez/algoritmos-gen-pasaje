'''
Explicación breve del Algoritmo
Codificación (Genotipo)
Representamos cada solución: Representamos cada solución como una cadena binaria de 5 bits (por ejemplo, 10110), ya que 
2 elevado a 5 = 32

Decodificación (Fenotipo)
La cadena binaria se convierte a un número decimal para poder evaluar 
𝑓(𝑥)= Xcuadrada

Función de Fitness
Dado un valor 

Generación de Población Inicial
Creamos varias cadenas de 5 bits de forma aleatoria para iniciar la “población”.

Selección
Elegimos los individuos más aptos (de mayor fitness) como padres para la siguiente generación.

Cruza (Crossover)
Mezclamos partes de bits de dos padres para producir nuevos hijos.

Mutación
Con una baja probabilidad, se cambia uno o más bits en un cromosoma para introducir variabilidad.

Iteración
Se repite selección, cruza y mutación por varias generaciones. Esperamos que, con el tiempo, aparezca un cromosoma que represente el valor de 

'''

import random

# ---------------------------------------------------------------------------------
# Parámetros del algoritmo
# ---------------------------------------------------------------------------------
LONGITUD_CROMOSOMA = 5    # 5 bits para representar x en [0, 31]
TAMANO_POBLACION = 10     # Número de individuos en la población
PROB_CRUZA = 0.8          # Probabilidad de cruza
PROB_MUTACION = 0.01      # Probabilidad de mutación
GENERACIONES = 20         # Cuántas iteraciones (generaciones) realizará el GA

# ---------------------------------------------------------------------------------
# Funciones de codificación y decodificación
# ---------------------------------------------------------------------------------
def generar_cromosoma():
    """
    Genera un cromosoma aleatorio de 5 bits (cadena de 0s y 1s).
    """
    return ''.join(random.choice(['0', '1']) for _ in range(LONGITUD_CROMOSOMA))

def decodificar_cromosoma(cromosoma):
    """
    Convierte la cadena binaria (genotipo) a un número entero (fenotipo).
    """
    return int(cromosoma, 2)

# ---------------------------------------------------------------------------------
# Función de aptitud (fitness)
# ---------------------------------------------------------------------------------
def fitness(cromosoma):
    """
    Calcula f(x) = x^2 para el cromosoma decodificado.
    Mientras mayor sea este valor, más "apto" es el cromosoma.
    """
    x = decodificar_cromosoma(cromosoma)
    return x * x

# ---------------------------------------------------------------------------------
# Creación de población inicial
# ---------------------------------------------------------------------------------
def crear_poblacion_inicial():
    """
    Crea la población inicial de TAMANO_POBLACION cromosomas aleatorios.
    """
    return [generar_cromosoma() for _ in range(TAMANO_POBLACION)]

# ---------------------------------------------------------------------------------
# Operador de selección
# ---------------------------------------------------------------------------------
def seleccionar(poblacion):
    """
    Selecciona dos padres de la población usando selección por torneo simple:
    - Se eligen 'n' individuos al azar y se escoge el de mayor fitness.
    - Se repite dos veces para obtener dos padres.
    """
    # Tamaño del torneo (puede ajustarse)
    torneo_size = 3

    def torneo():
        # Elige 'torneo_size' individuos al azar
        candidatos = random.sample(poblacion, torneo_size)
        # Devuelve el que tenga mayor fitness
        return max(candidatos, key=fitness)

    padre1 = torneo()
    padre2 = torneo()
    return padre1, padre2

# ---------------------------------------------------------------------------------
# Operador de cruza (crossover)
# ---------------------------------------------------------------------------------
def cruzar(padre1, padre2):
    if random.random() < PROB_CRUZA:
        punto_cruce = random.randint(1, LONGITUD_CROMOSOMA - 1)
        
        # Partes de cada padre
        left_p1  = padre1[:punto_cruce]
        right_p1 = padre1[punto_cruce:]
        left_p2  = padre2[:punto_cruce]
        right_p2 = padre2[punto_cruce:]
        
        # Combinar para obtener hijos de 5 bits
        hijo1 = left_p1 + right_p2  # Padre1 izquierda + Padre2 derecha
        hijo2 = left_p2 + right_p1  # Padre2 izquierda + Padre1 derecha
        
        return hijo1, hijo2
    else:
        # Sin cruza, devolvemos tal cual
        return padre1, padre2

# ---------------------------------------------------------------------------------
# Operador de mutación
# ---------------------------------------------------------------------------------
def mutar(cromosoma):
    """
    Con probabilidad PROB_MUTACION, voltea bits del cromosoma.
    """
    cromosoma_list = list(cromosoma)
    for i in range(LONGITUD_CROMOSOMA):
        if random.random() < PROB_MUTACION:
            cromosoma_list[i] = '1' if cromosoma_list[i] == '0' else '0'
    return ''.join(cromosoma_list)

# ---------------------------------------------------------------------------------
# Búsqueda del mejor individuo en la población
# ---------------------------------------------------------------------------------
def mejor_individuo(poblacion):
    """
    Retorna el cromosoma con el mejor valor de fitness en la población.
    """
    return max(poblacion, key=fitness)

# ---------------------------------------------------------------------------------
# Función principal que corre el Algoritmo Genético
# ---------------------------------------------------------------------------------
def algoritmo_genetico():
    # 1. Crear población inicial
    poblacion = crear_poblacion_inicial()

    for gen in range(GENERACIONES):
        nueva_poblacion = []

        # 2. Generar nueva población usando selección, cruza y mutación
        while len(nueva_poblacion) < TAMANO_POBLACION:
            padre1, padre2 = seleccionar(poblacion)
            hijo1, hijo2 = cruzar(padre1, padre2)
            hijo1 = mutar(hijo1)
            hijo2 = mutar(hijo2)
            nueva_poblacion.append(hijo1)
            if len(nueva_poblacion) < TAMANO_POBLACION:
                nueva_poblacion.append(hijo2)

        # 3. Reemplazar la población anterior por la nueva
        poblacion = nueva_poblacion

        # 4. Revisar el mejor de la generación
        mejor = mejor_individuo(poblacion)
        print(f"Generación {gen+1}: Mejor Cromosoma = {mejor}, Valor = {decodificar_cromosoma(mejor)}, Fitness = {fitness(mejor)}")

    # 5. Resultado final
    mejor_final = mejor_individuo(poblacion)
    x_optimo = decodificar_cromosoma(mejor_final)
    print("\n=== RESULTADO FINAL ===")
    print(f"Mejor Cromosoma: {mejor_final}")
    print(f"Mejor x: {x_optimo}")
    print(f"Fitness: {fitness(mejor_final)}")


if __name__ == "__main__":
    algoritmo_genetico()
