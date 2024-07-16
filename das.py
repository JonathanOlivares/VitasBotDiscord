import time
import datetime
# from settings.lang import Language


class Language:
    def __init__(self, language: str): 
        self._added_at = datetime.datetime.now()
        self.language = language
    def get_added_at(self):
        return self._added_at


# Definir una función para crear un diccionario de tamaño n
def crear_diccionario(n):
    return {f"dasda{i}dadsd{i*5}": Language("i") for i in range(n)}

# Definir una función para buscar un elemento en un diccionario y medir el tiempo
def buscar_elemento(diccionario, elemento):
    return diccionario[f"dasda{elemento}dadsd{elemento*5}"]

def ordenar_diccionario(diccionario: dict[str, Language]):
    return sorted(diccionario.values(), key=lambda x: x.get_added_at())
# Realizar la prueba para diferentes tamaños de diccionario
tamaños_diccionario = [500, 1000, 1500, 200000]

for size in tamaños_diccionario:
    # Crear el diccionario
    diccionario = crear_diccionario(size)
    
    # Definir el elemento a buscar
    # Buscamos el elemento en la mitad del diccionario
    # Medir el tiempo de búsqueda

        # elemento_a_buscar = (size // 2 + i+1)

    inicio = time.time()
    a = ordenar_diccionario(diccionario)
    fin = time.time()

    tiempo_busqueda = fin - inicio
    print(f"El tiempo de ordenar el diccionario de {size} elementos es: {tiempo_busqueda} segundos\n")
    # print(a)
        # Imprimir los resultados
      #  print(f"Tiempo de búsqueda {i+1} en un diccionario de {size} elementos. Buscando {elemento_a_buscar}: {tiempo_busqueda} segundos")
     #   suma+= tiempo_busquedac
    #print(f"Promedio de tiempo de búsqueda en un diccionario de {size} elementos: {suma/10} segundos")
    print("\n")
