#!/usr/bin/python
import AlgoritmoGeneticoTravelingSalesman as GA
import sys
from celluloid import Camera
import seaborn as sns
from matplotlib import pyplot as plt
import folium

global fig
global ax
global camera


def fotograma(df):
    """Genera un fotograma de la animación.

    """
    plot = sns.distplot(1 / df.iloc[:]["Fitness"], color='red')
    ax.set(xlabel='Distancia (km)', ylabel='')
    ax.text(0.9, 1.01, "Generación F" + str(i), transform=ax.transAxes)
    mejorRuta = "Mejor ruta: -"
    for ciudad in df.iloc[0]["Itinerario"]:
        mejorRuta = mejorRuta + ciudad[:3] + "-"
    ax.text(0, 1.08, mejorRuta, transform=ax.transAxes)
    camera.snap()


if __name__ == "__main__":
    """
    Ejemplo de uso para buscar la mejor ruta entre una serie de ciudades:

    python TravelingSalesmanSolver.py Sevilla Cadiz Malaga Granada Marchena "Puerto Real" "Cuevas de San Marcos"


    """
    lista_ciudades = sys.argv[1:]
    n_pop = 100  # tamaño de la población
    n_elite = 3  # Los n-elite individuos más aptos pasarán directamente a la siguiente generación
    # Probabilidad de que se produzca una mutación para cada uno de los genes
    # del individuo.
    tasaMutacion = 0.01
    n_generaciones = 100  # Número de generaciones que se van a generar
    k = 10  # Número de pretendientes que se enfrentarán en torneo para reproducirse. Si k=0, entonces se seleccionan de forma proporcional al Fitness.
    df_ciudades = GA.generarDataFrameCiudades(lista_ciudades)
    ciudades = GA.llamarCiudades(lista_ciudades, df_ciudades)
    print("\n Se comienza a generar la población\n", end='\r')
    df = GA.IniciarPoblacion(n_pop, ciudades)
    i = 1
    print("\n Se ha generado la población parental con éxito. \n", end='\r')
    # generamos figura para la animación
    fig, ax = plt.subplots(figsize=(9, 6))
    camera = Camera(fig)
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
        fotograma(df)
        i += 1
    print("\n")
    print("Se ha terminado el proceso\n")
    print("-".join(mejorRuta['Itinerario']))
    print(
        "Con una distancia de {} kilometros".format(
            1 / mejorRuta['Fitness']))
    animation = camera.animate()
    animation.save('animation2.gif')

    # generamos html con ruta final
    x = []
    y = []
    itinerario = mejorRuta["Itinerario"]
    for ciudad in itinerario:
        ciudad = df_ciudades.loc[df_ciudades["Ciudad"]
                                 == ciudad]['ObjetoCiudad']
        x.append(ciudad.iloc[0].lat)
        y.append(ciudad.iloc[0].lon)

    points = list(zip(x, y))
    mp = folium.Map(
        width=800,
        height=500,
        tiles='CartoDB positron',
        zoom_start=15)
    for point in points:
        folium.Marker(location=point).add_to(mp)
    folium.PolyLine(points, color="red", weight=2.5, opacity=1).add_to(mp)
    title_html = '''
             <h3 align="left" style="font-size:28px"><b>{}</b></h3>
             '''.format("Mejor ruta encontrada")
    mp.get_root().html.add_child(folium.Element(title_html))
    ruta_html = '''
             <p align="left" style="font-size:14px"><b>{}</b><p>
             '''.format('-'.join(mejorRuta['Itinerario']))
    mp.get_root().html.add_child(folium.Element(ruta_html))
    dist_html = '''
             <p align="left" style="font-size:14px"><b>Distancia {}km</b><p>
             '''.format(1 / mejorRuta['Fitness'])
    mp.get_root().html.add_child(folium.Element(dist_html))
    condiciones_html = '''
             <p align="left" style="font-size:14px"><b>Tamaño de la población {0}, n-elite {1}, tasa de mutación {2}, número de generaciones {3} y número de pretendientes {4}. La mejor ruta se alcanzó en la generación {5}. </b><p>
             '''.format(n_pop, n_elite, tasaMutacion, n_generaciones, k, generacionMejorRuta)
    mp.get_root().html.add_child(folium.Element(condiciones_html))
    mp.save('Ruta.html')
