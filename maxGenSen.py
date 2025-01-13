'''
Propondremos una función con varios máximos locales, de modo que el 
algoritmo genético tenga que “explorar” y “explotar” el espacio de búsqueda antes de converger a la mejor solución.
la funcion va a ser f(x)= xSen aX
donde a es un número entero en el rango [0, 255],

De esta manera, la función tendrá múltiples picos (máximos locales) 
a lo largo de [0, 255]. Con un rango de 256 valores, es más difícil 
“adivinar” directamente dónde está el máximo. Un algoritmo genético 
es ideal para ubicar ese valor de 
a que produce el máximo global en lugar de perderse en alguno de los
 máximos locales.
'''
import random
import math

# -------------------------------------------------------------
# PARÁMETROS DEL ALGORITMO GENÉTICO
# -------------------------------------------------------------
LONGITUD_CROMOSOMA = 8      # 8 bits para representar x en [0..255]
TAMANO_POBLACION = 20       # Número de individuos en la población
PROB_CRUZA = 0.7            # Probabilidad de cruza
PROB_MUTACION = 0.02        # Probabilidad de mutación
GENERACIONES = 50           # Número de generaciones

# Parámetro de la función f(x)
ALPHA = (4.0 * math.pi) / 256.0  # 4π/256 (≈ 0.049087)

# -------------------------------------------------------------
# FUNCIÓN DE AYUDA
# -------------------------------------------------------------
def generar_cromosoma():
    """ Genera un cromosoma aleatorio de 8 bits (cadena de 0s y 1s). """
    return ''.join(random.choice(['0', '1']) for _ in range(LONGITUD_CROMOSOMA))

def decodificar(cromosoma):
    """ Convierte la cadena binaria a número entero. """
    return int(cromosoma, 2)

def fitness(cromosoma):
    """
    Función a maximizar: f(x) = x * sin(ALPHA * x)
    Mayor sea el valor => mejor.
    """
    x = decodificar(cromosoma)
    return x * math.sin(ALPHA * x)

def crear_poblacion_inicial():
    """ Crea la población inicial de cromosomas aleatorios. """
    return [generar_cromosoma() for _ in range(TAMANO_POBLACION)]

def seleccionar(poblacion):
    """
    Selección por torneo: se eligen N individuos al azar
    y se queda el de mayor fitness. Se repite 2 veces.
    """
    torneo_size = 3
    def torneo():
        candidatos = random.sample(poblacion, torneo_size)
        return max(candidatos, key=fitness)
    return torneo(), torneo()

def cruzar(padre1, padre2):
    """ Cruce de un punto. """
    if random.random() < PROB_CRUZA:
        punto_cruce = random.randint(1, LONGITUD_CROMOSOMA - 1)
        left_p1 = padre1[:punto_cruce]
        right_p1 = padre1[punto_cruce:]
        left_p2 = padre2[:punto_cruce]
        right_p2 = padre2[punto_cruce:]
        hijo1 = left_p1 + right_p2
        hijo2 = left_p2 + right_p1
        return hijo1, hijo2
    else:
        return padre1, padre2

def mutar(cromosoma):
    """ Con probabilidad PROB_MUTACION se cambia un bit. """
    cromosoma_list = list(cromosoma)
    for i in range(LONGITUD_CROMOSOMA):
        if random.random() < PROB_MUTACION:
            cromosoma_list[i] = '1' if cromosoma_list[i] == '0' else '0'
    return ''.join(cromosoma_list)

def mejor_individuo(poblacion):
    """ Retorna el individuo con mejor fitness de toda la población. """
    return max(poblacion, key=fitness)

# -------------------------------------------------------------
# ALGORITMO GENÉTICO
# -------------------------------------------------------------
def algoritmo_genetico():
    poblacion = crear_poblacion_inicial()
    
    for gen in range(GENERACIONES):
        nueva_poblacion = []
        
        while len(nueva_poblacion) < TAMANO_POBLACION:
            padre1, padre2 = seleccionar(poblacion)
            hijo1, hijo2 = cruzar(padre1, padre2)
            hijo1 = mutar(hijo1)
            hijo2 = mutar(hijo2)
            nueva_poblacion.append(hijo1)
            if len(nueva_poblacion) < TAMANO_POBLACION:
                nueva_poblacion.append(hijo2)
        
        poblacion = nueva_poblacion
        
        # Ver el mejor individuo de esta generación
        best = mejor_individuo(poblacion)
        x_value = decodificar(best)
        print(f"Gen {gen+1:02d} | Mejor: {best}, x={x_value}, fitness={fitness(best):.4f}")

    # Resultado final
    mejor_final = mejor_individuo(poblacion)
    x_optimo = decodificar(mejor_final)
    print("\n=== RESULTADO FINAL ===")
    print(f"Mejor Cromosoma: {mejor_final}")
    print(f"Mejor x: {x_optimo}")
    print(f"Fitness: {fitness(mejor_final):.4f}")

if __name__ == "__main__":
    algoritmo_genetico()

'''
Cuando hablamos de “varios picos” (máximos locales), nos referimos a
que la función no es monótonamente creciente o decreciente en el 
rango, sino que presenta varios puntos en los que puede alcanzar
valores altos. Sin embargo, un algoritmo genético estándar 
(sin técnicas especiales de nicho o de mantenimiento de diversidad)
tiende a concentrarse en un solo óptimo (el mejor o uno de los 
mejores), convergiendo hacia él y “olvidando” los demás picos.
 Por eso, al final, el GA imprime solo una mejor solución.
'''