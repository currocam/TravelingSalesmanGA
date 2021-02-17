import numpy as np
import random
import pandas as pd
from matplotlib import pyplot as plt
from geopy import distance
from geopy.geocoders import Nominatim
from celluloid import Camera
import seaborn as sns


class Ciudad:
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

    Parameters
    ----------
    nombre_ciudad : str
        Nombre de la ciudad introducida.

    Returns
    -------
    coordenadas: list
    direccion: str
        Par de coordenadas y dirección de la ciudad.

    """
    geolocator = Nominatim(user_agent="Salesman")
    localizacion = geolocator.geocode(nombre_ciudad)
    coordenadas = (localizacion.latitude, localizacion.longitude)
    direccion = localizacion.address
    return (coordenadas, direccion)


def geolocalizarCiudades(lista_ciudades: list):
    """Para una lista con nombres de ciudades devuelve una fila de DataFrame.

    Parameters
    ----------
    lista_ciudades : list
        Lista de nombres de ciudades.

    Returns
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

    Parameters
    ----------
    lista_ciudades : list
        Lista de nombres de ciudades.
    Mostrar : bool
        Si Mostrar==True se imprime en la terminal información sobre las ciudades que se recogen.

    Returns
    -------
    df_ciudades: pandas.DataFrame
        DataFrame de todas las ciudades que incluye el nombre de la ciudad, el par de coordenadas, la dirección completa de la ciudad y una instancia de la clase Ciudad.

    """
    df_ciudades = geolocalizarCiudades(lista_ciudades)
    if Mostrar:
        for i in range(df_ciudades.shape[0]):
            print(
                "Se han añadido las coordendas de la localidad: {0} \n".format(
                    df_ciudades.iloc[i]['Direccion']))
    return df_ciudades


def llamarCiudades(lista_ciudades: list, df_ciudades):
    """Para una lista de nombres de ciudades devuelve una lista equivalente con las instancias de la clase Ciudad correspondientes.

    Parameters
    ----------
    lista_ciudades : list
        Lista de nombres de ciudades
    df_ciudades : pandas.DataFrame
        DataFrame generado con la función generarDataFrameCiudades(),

    Returns
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

    Parameters
    ----------
    ciudades: list
        Lista con instancias de la clase Ciudad
    Returns
    -------
    ruta: AlgoritmoGeneticoTravelingSalesman.Ruta
        Instancia de la clase Ruta.

    """
    ruta = Ruta(random.sample(ciudades, len(ciudades)))
    return ruta


def generarDataFrameRuta(ruta):
    """Para una instancia de la clase Ruta devuelve una fila de DataFrame.

    Parameters
    ----------
    ruta : AlgoritmoGeneticoTravelingSalesman.Ruta
        Instancia de la clase Ruta.

    Returns
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

    Parameters
    ----------
    n : int
        Número de rutas que conformarán la población.
    ciudades: list
        Lista con instancias de la clase Ciudad

    Returns
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


def seleccionarIndividuoTorneo(df_pop):
    """Selecciona un individuo (osea, una ruta) mediante selección por torneos. Se enfrentan 2 individuos escogidos al azar y el de mayor aptitud es devuelto.

    Parameters
    ----------
    df_pop: pandas.DataFrame
        DataFrame con toda la información de una población de rutas

    Returns
    -------
    winner: pandas.core.series.Series
        Fila del DataFrame correspondiente al individuo escogido por selección por torneo.

    """
    n = df_pop.shape[0]
    fighter_1 = df_pop.iloc[random.randint(0, n - 1)]
    fighter_2 = df_pop.iloc[random.randint(0, n - 1)]

    # selección por torneo determinista, se selecciona al mejor individuo con
    # p=1
    if fighter_1.Fitness >= fighter_2.Fitness:
        winner = fighter_1
    else:
        winner = fighter_2
    return winner


def crossover(parent1, parent2, df_ciudades):
    """Cruza dos individuos de forma ordenada para devolver  descendiente que combina las características de los progenitores.

    Parameters
    ----------
    parent1 : pandas.DataFrame
        Fila del DataFrame de la población que corresponde al individuo 1 que se desea cruzar.
    parent2 : pandas.DataFrame
        Fila del DataFrame de la población que corresponde al individuo 2 que se desea cruzar..
    df_ciudades : pandas.DataFrame
        DataFrame generado con la función generarDataFrameCiudades()

    Returns
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

    Parameters
    ----------
    ruta: AlgoritmoGeneticoTravelingSalesman.Ruta
        Instancia de la clase Ruta que se desea mutar.
    tasaMutacion : float
        Probabilidad de que se produzca una mutación para cada uno de los genes del individuo.
    df_ciudades : pandas.DataFrame
        DataFrame generado con la función generarDataFrameCiudades()

    Returns
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
        tasaMutacion=0.1):
    """Genera a partir de una población la siguiente generación simulando cruzamiento y mutación. Se incluye "elitismo", es decir, una parte de la población más apta pasa directamente a la siguiente generación.

    Parameters
    ----------
    df_pop: pandas.DataFrame
        DataFrame con toda la información de una población de rutas
    df_ciudades : pandas.DataFrame
        DataFrame generado con la función generarDataFrameCiudades()
    n_elite : int
        Los n-elite individuos más aptos pasarán directamente a la siguiente generación
    tasaMutacion : float
        Probabilidad de que se produzca una mutación para cada uno de los genes del individuo.

    Returns
    -------
    newdf: pandas.DataFrame
        DataFrame con toda la información de la siguiente generación.

    """
    n = df_pop.shape[0] - n_elite
    newdf = df_pop.head(n_elite)  # Aquí se introduce el elitismo
    df_pop = df_pop.iloc[n_elite:]
    for i in range(n):
        parent1 = seleccionarIndividuoTorneo(df_pop)
        parent2 = seleccionarIndividuoTorneo(df_pop)
        rutaHija = crossover(parent1, parent2, df_ciudades)
        rutaHijaMutada = mutate(rutaHija, tasaMutacion, df_ciudades)
        data = generarDataFrameRuta(rutaHijaMutada)
        newdf = newdf.append(data)
        newdf = newdf.sort_values(by='Fitness', ascending=False)
    return newdf
