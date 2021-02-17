#TravelingSalesmanGA
This python script allows you to implement a genetic algorithm to the [Traveling Salesman Problem](https://en.wikipedia.org/wiki/Travelling_salesman_problem) for a bunch of cities. It was created with educational purposes.

## General info
The script work as follows:
1. Geolocation of the group of cities of interest with the [geopy library](https://github.com/geopy/geopy)
2. Start an initial generation (generate random routes)
3. Calculate population fitness
4. Mating pool (Deterministic tournament selection and the Elitism Strategy)
5. Crossover and mutation over the population
6. Generate next population and repeat steps 3-5
## Technologies
* Python 3.8.5

## Example of use
To run the algorithm for a list of cities in the terminal and save an animated graph:

```
$ cd ../TravelingSalesmanGA
$ python TravelingSalesmanSolverAnimation.py Sevilla Cadiz Malaga Granada Marchena Madrid Alicante Valladolid Badalona Burgos Getafe Badajoz Salamanca Algeciras Carmona Antequera Lorca Murcia Grazalema Adra Huelva Zufre Bormujos

```
That will return after a while the best route found and an animated graph, hopefully, similar to this:

![](animation.gif)

In order to just get the best route use:

```
$ cd ../TravelingSalesmanGA
$ python TravelingSalesmanSolver.py Sevilla Cadiz Malaga Granada Marchena Madrid Alicante Valladolid Badalona Burgos Getafe Badajoz Salamanca Algeciras Carmona Antequera Lorca Murcia Grazalema Adra Huelva Zufre Bormujos

```
