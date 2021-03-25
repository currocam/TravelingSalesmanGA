#!/usr/bin/python
import AlgoritmoGeneticoTravelingSalesman as GA
import sys

if __name__ == "__main__":
    """
    Ejemplo de uso para buscar la mejor ruta entre una serie de ciudades:

    python TravelingSalesmanSolver.py Sevilla Cadiz Malaga Granada Marchena "Puerto Real" "Cuevas de San Marcos"


    """
    lista_ciudades = sys.argv[1:]
    n_pop = 100  # tamaño de la población
    n_elite = 0  # Los n-elite individuos más aptos pasarán directamente a la siguiente generación
    # Probabilidad de que se produzca una mutación para cada uno de los genes
    # del individuo.
    tasaMutacion = 0.1
    n_generaciones = 5  # Número de generaciones que se van a generar
    k = 0  # Número de pretendientes que se enfrentarán en torneo para reproducirse. Si k=0, entonces se seleccionan de forma proporcional al Fitness.
    df_ciudades = GA.generarDataFrameCiudades(lista_ciudades)
    ciudades = GA.llamarCiudades(lista_ciudades, df_ciudades)
    print("\n Se comienza a generar la población\n", end='\r')
    df = GA.IniciarPoblacion(n_pop, ciudades)
    i = 1
    print("\n Se ha generado la población parental con éxito. \n", end='\r')
    df = df.reset_index(drop=True)
    mejorRuta = df.iloc[0]
    generacionMejorRuta = i
    while i <= n_generaciones:
        df = GA.cruzamientoPoblacion(df, df_ciudades, n_elite, tasaMutacion, k)
        df = df.reset_index(drop=True)
        nuevaRuta = df.iloc[0]
        if 1 / mejorRuta['Fitness'] > 1 / nuevaRuta['Fitness']:
            mejorRuta = nuevaRuta
        generacionMejorRuta = i
        print("Generación F{0} creada con éxito.".format(i), end='\r')
        i += 1
    print("\n")
    print("Se ha terminado el proceso\n")
    print("-".join(mejorRuta['Itinerario']))
    print(
        "Con una distancia de {} kilometros".format(
            1 / mejorRuta['Fitness']))
    condiciones_str = "\n Tamaño de la población {0}, n-elite {1}, tasa de mutación {2}, número de generaciones {3} y número de pretendientes {4}. La mejor ruta se alcanzó en la generación {5}.".format(
        n_pop, n_elite, tasaMutacion, n_generaciones, k, generacionMejorRuta)
    print(condiciones_str)
