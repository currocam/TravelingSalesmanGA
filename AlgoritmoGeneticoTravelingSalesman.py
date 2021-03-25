import numpy as np
import random
import pandas as pd
from matplotlib import pyplot as plt
from geopy import distance
from geopy.geocoders import Nominatim
from celluloid import Camera
import seaborn as sns
import numpy.random as npr
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


class Ciudad:
    """Una clase que representa una ciudad del problema

    Parámetros
    ----------
    lat : float
        Latitud de la ciudad.
    lon : float
        Longitud de la ciudad..
    nombre : str
        Nombre de la ciudad.

    Atributos
    ----------
    lat : float
    lon : float
    nombre : str

    Métodos
    -------
    distancia(self, ciudad2):
        Devuelve la distancia entre dos ciudades.

    """

    def __init__(self, lat, lon, nombre):
        self.lat = lat
        self.lon = lon
        self.nombre = nombre

    def distancia(self, ciudad2):
        x1y1 = (self.lat, self.lon)
        x2y2 = (ciudad2.lat, ciudad2.lon)
        dist = distance.distance(x1y1, x2y2).km
        return dist


class Ruta:
    """Una clase que representa una posible ruta.

    Parámetros
    ----------
    itinerario : list
        Lista con las Ciudades que conforman la ruta.

    Atributos
    ----------
    dist : float
        Distancia total de la ruta en km.
    fitness : float
        Inverso de la distancia.
    itinerario: list

    Métodos
    -------
    trayecto(self):
        Devuelve una lista con los nombres de las ciudades que conforman la ruta.

    """

    def __init__(self, itinerario):

        self.itinerario = itinerario
        self.dist = 0
        for i, v in enumerate(self.itinerario):
            if i + 1 == len(self.itinerario):
                break
            origen = v
            destino = self.itinerario[i + 1]
            self.dist += origen.distancia(destino)
        try:
            self.fitness = 1 / self.dist
        except ZeroDivisionError:
            self.fitness = None
            print("La distancia de la ruta es incorrecta")

    def trayecto(self):
        list = []
        for city in self.itinerario:
            list.append(city.nombre)
        return list


def geolocalizar(nombre_ciudad):
    """Localiza una ciudad dada y devuelve su dirección y sus coordendas.

    Parámetros
    ----------
    nombre_ciudad : str
        Nombre de la ciudad introducida.

    Devuelve
    -------
    coordenadas: list
    direccion: str
        Par de coordenadas y dirección de la ciudad.

    """
    geolocator = Nominatim(user_agent="Salesman", timeout=10)
    localizacion = geolocator.geocode(nombre_ciudad)
    coordenadas = (localizacion.latitude, localizacion.longitude)
    direccion = localizacion.address
    return (coordenadas, direccion)


def geolocalizarCiudades(lista_ciudades: list):
    """Para una lista con nombres de ciudades devuelve una fila de DataFrame.

    Parámetros
    ----------
    lista_ciudades : list
        Lista de nombres de ciudades.

    Devuelve
    -------
    df_Fila: pandas.DataFrame
        Fila de un DataFrame que incluye el nombre de la ciudad, el par de coordenadas, la dirección completa de la ciudad y una instancia de la clase Ciudad.

    """
    rows = []
    for i in lista_ciudades:
        coord, direccion = geolocalizar(i)
        rows.append([i, coord, direccion, Ciudad(*coord, i)])
    df_Fila = pd.DataFrame(
        rows,
        columns=[
            "Ciudad",
            "Coordenadas",
            "Direccion",
            "ObjetoCiudad"])
    return df_Fila


def generarDataFrameCiudades(lista_ciudades: list, Mostrar=True):
    """Genera el DataFrame completo para todas las ciudades del problema.

    Parámetros
    ----------
    lista_ciudades : list
        Lista de nombres de ciudades.
    Mostrar : bool
        Si Mostrar==True se imprime en la terminal información sobre las ciudades que se recogen.

    Devuelve
    -------
    df_ciudades: pandas.DataFrame
        DataFrame de todas las ciudades que incluye el nombre de la ciudad, el par de coordenadas, la dirección completa de la ciudad y una instancia de la clase Ciudad.

    """
    df_ciudades = geolocalizarCiudades(lista_ciudades)
    if Mostrar:
        for i in range(df_ciudades.shape[0]):
            print(
                "Se han añadido las coordendas de la localidad: {0}".format(
                    df_ciudades.iloc[i]['Direccion']))
    return df_ciudades


def llamarCiudades(lista_ciudades: list, df_ciudades):
    """Para una lista de nombres de ciudades devuelve una lista equivalente con las instancias de la clase Ciudad correspondientes.

    Parámetros
    ----------
    lista_ciudades : list
        Lista de nombres de ciudades
    df_ciudades : pandas.DataFrame
        DataFrame generado con la función generarDataFrameCiudades(),

    Devuelve
    -------
    ciudades: list
        Lista con instancias de la clase Ciudad

    """
    ciudades = []
    for i in lista_ciudades:
        city = df_ciudades[df_ciudades['Ciudad']
                           == i]['ObjetoCiudad'].values[0]
        ciudades.append(city)
    return ciudades


def crearRuta(ciudades):
    """Genera una instancia de la clase Ruta aleatoria que pasa por todas las ciudades.

    Parámetros
    ----------
    ciudades: list
        Lista con instancias de la clase Ciudad
    Devuelve
    -------
    ruta: AlgoritmoGeneticoTravelingSalesman.Ruta
        Instancia de la clase Ruta.

    """
    ruta = Ruta(random.sample(ciudades, len(ciudades)))
    return ruta


def generarDataFrameRuta(ruta):
    """Para una instancia de la clase Ruta devuelve una fila de DataFrame.

    Parámetros
    ----------
    ruta : AlgoritmoGeneticoTravelingSalesman.Ruta
        Instancia de la clase Ruta.

    Devuelve
    -------
    df_Fila: pandas.DataFrame
        Fila de un DataFrame con la información correspondiente a una Ruta.

    """
    rows = []
    rows.append(
        {
            'Itinerario': ruta.trayecto(),
            'Fitness': ruta.fitness,
            'Ciudad': ruta
        })

    df_Fila = pd.DataFrame(rows, columns=["Itinerario", "Fitness", "Ciudad"])
    return df_Fila


def IniciarPoblacion(n, ciudades):
    """Genera una población de rutas para una lista de ciudades .

    Parámetros
    ----------
    n : int
        Número de rutas que conformarán la población.
    ciudades: list
        Lista con instancias de la clase Ciudad

    Devuelve
    -------
    df_pop: pandas.DataFrame
        DataFrame con toda la información de una población de rutas
    """
    df_pop = pd.DataFrame()
    for i in range(n):
        ruta = crearRuta(ciudades)
        data = generarDataFrameRuta(ruta)
        df_pop = df_pop.append(data)
    df_pop = df_pop.sort_values(by='Fitness', ascending=False)
    return df_pop


def FitnessProportionateSelecion(df_pop):
    """Selecciona un individuo (osea, una ruta) mediante selección por una selección proporcional al fitness.
    Parámetros
    ----------
    df_pop: pandas.DataFrame
        DataFrame con toda la información de una población de rutas
    Devuelve
    -------
    winner: pandas.core.series.Series
        Fila del DataFrame correspondiente al individuo escogido por selección por torneo.

    """
    n = df_pop.shape[0]
    max = sum([row.Fitness for index, row in df_pop.iterrows()])
    selection_probs = [row.Fitness / max for index, row in df_pop.iterrows()]
    index = npr.choice(range(n), p=selection_probs)
    winner = df_pop.loc[index]
    return winner


def seleccionarIndividuoTorneo(df_pop, k):
    """Selecciona un individuo (osea, una ruta) mediante selección por torneos. Se enfrentan k individuos escogidos al azar y el de mayor aptitud es devuelto.

    Parámetros
    ----------
    df_pop: pandas.DataFrame
        DataFrame con toda la información de una población de rutas
    k: int
        Número de pretendientes que se enfrentarán en torneo para reproducirse. Si k=0, entonces se seleccionan de forma proporcional al Fitness.

    Devuelve
    -------
    winner: pandas.core.series.Series
        Fila del DataFrame correspondiente al individuo escogido por selección por torneo.

    """
    pretendientes = df_pop.sample(n=k)
    # selección por torneo determinista, se selecciona al mejor individuo con
    # p=1
    index = pretendientes['Fitness'].argmax()
    winner = df_pop.loc[index]
    return winner


def seleccionarProgenitores(df_pop, k):
    """Selecciona el par de progenitores de acorde a los dos métodos disponibles.

    Parameters
    ----------
    df_pop: pandas.DataFrame
        DataFrame con toda la información de una población de rutas
    k: int
        Número de pretendientes que se enfrentarán en torneo para reproducirse. Si k=0, entonces se seleccionan de forma proporcional al Fitness.
    """
    if k == 0:
        parent1 = FitnessProportionateSelecion(df_pop)
        parent2 = FitnessProportionateSelecion(df_pop)
        return parent1, parent2
    else:
        parent1 = seleccionarIndividuoTorneo(df_pop, k)
        parent2 = seleccionarIndividuoTorneo(df_pop, k)
        return parent1, parent2


def crossover(parent1, parent2, df_ciudades):
    """Cruza dos individuos de forma ordenada para devolver  descendiente que combina las características de los progenitores.

    Parámetros
    ----------
    parent1 : pandas.DataFrame
        Fila del DataFrame de la población que corresponde al individuo 1 que se desea cruzar.
    parent2 : pandas.DataFrame
        Fila del DataFrame de la población que corresponde al individuo 2 que se desea cruzar..
    df_ciudades : pandas.DataFrame
        DataFrame generado con la función generarDataFrameCiudades()

    Devuelve
    -------
    Ruta(F1): AlgoritmoGeneticoTravelingSalesman.Ruta
        Instancia de la clase Ruta resultante del cruzamiento de ambos progenitores.

    """
    P1 = []
    P2 = []
    gen1 = random.randint(0, len(parent1.Itinerario) - 1)
    gen2 = random.randint(0, len(parent1.Itinerario) - 1)
    start = min(gen1, gen2)
    end = max(gen1, gen2)
    for i in range(start, end):  # La recombinación que se realiza es ordenada,
        P1.append(parent1.Itinerario[i])
    P2 = [item for item in parent2.Itinerario if item not in P1]
    F1 = llamarCiudades(P1 + P2, df_ciudades)
    return Ruta(F1)


def mutate(ruta, tasaMutacion, df_ciudades):
    """Produce mutación (intercambia genes, osea ciudades, de posición en la ruta) en un individuo.

    Parámetros
    ----------
    ruta: AlgoritmoGeneticoTravelingSalesman.Ruta
        Instancia de la clase Ruta que se desea mutar.
    tasaMutacion : float
        Probabilidad de que se produzca una mutación para cada uno de los genes del individuo.
    df_ciudades : pandas.DataFrame
        DataFrame generado con la función generarDataFrameCiudades()

    Devuelve
    -------
    Ruta(IndMutado)
        Instancia de la clase Ruta resultante del proceso de mutación aleatorio.

    """
    trayecto = ruta.trayecto()
    for pos1, city in enumerate(trayecto):
        if(random.random() < tasaMutacion):
            pos2 = random.randint(0, len(trayecto) - 1)
            trayecto[pos1], trayecto[pos2] = trayecto[pos2], trayecto[pos1]
    IndMutado = llamarCiudades(trayecto, df_ciudades)
    return Ruta(IndMutado)


def cruzamientoPoblacion(
        df_pop,
        df_ciudades,
        n_elite=20,
        tasaMutacion=0.1,
        k=5):
    """Genera a partir de una población la siguiente generación simulando cruzamiento y mutación. Se incluye "elitismo", es decir, una parte de la población más apta pasa directamente a la siguiente generación.

    Parámetros
    ----------
    df_pop: pandas.DataFrame
        DataFrame con toda la información de una población de rutas
    df_ciudades : pandas.DataFrame
        DataFrame generado con la función generarDataFrameCiudades()
    n_elite : int
        Los n-elite individuos más aptos pasarán directamente a la siguiente generación
    tasaMutacion : float
        Probabilidad de que se produzca una mutación para cada uno de los genes del individuo.
    k: int
        Número de pretendientes que se enfrentarán en torneo para reproducirse. Si k=0, entonces se seleccionan de forma proporcional al Fitness.

    Devuelve
    -------
    newdf: pandas.DataFrame
        DataFrame con toda la información de la siguiente generación.

    """
    n = df_pop.shape[0] - n_elite
    if n_elite == 0:
        newdf = df_pop[0:0]
    else:
        newdf = df_pop.head(n_elite)  # Aquí se introduce el elitismo
    for i in range(n):
        parent1, parent2 = seleccionarProgenitores(df_pop, k)
        rutaHija = crossover(parent1, parent2, df_ciudades)
        rutaHijaMutada = mutate(rutaHija, tasaMutacion, df_ciudades)
        data = generarDataFrameRuta(rutaHijaMutada)
        newdf = newdf.append(data)
        newdf = newdf.sort_values(by='Fitness', ascending=False)
    return newdf
