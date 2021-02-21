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
    n_elite = 20  # Los n-elite individuos más aptos pasarán directamente a la siguiente generación
    # Probabilidad de que se produzca una mutación para cada uno de los genes
    # del individuo.
    tasaMutacion = 0.01
    n_generaciones = 5  # Número de generaciones que se van a generar
    df_ciudades = GA.generarDataFrameCiudades(lista_ciudades)
    ciudades = GA.llamarCiudades(lista_ciudades, df_ciudades)
    print("\n Se comienza a generar la población\n",  end='\r')
    df = GA.IniciarPoblacion(n_pop, ciudades)
    i = 1
    print("\n Se ha generado la población parental con éxito. \n",  end='\r')
    evolucion = []
    while i <= n_generaciones:
        df = GA.cruzamientoPoblacion(df, df_ciudades, n_elite, tasaMutacion)
        print("Generación F{0} creada con éxito".format(i),  end='\r')
        i += 1
        evolucion.append(1 / df.iloc[0:50]["Fitness"])
    print("\n")
    print("Se ha terminado el proceso\n")
    print(df.iloc[0]['Itinerario'])
    print(
        "Con una distancia de {} kilometros".format(
            1 / df.iloc[0]['Fitness']))
