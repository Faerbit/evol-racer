#!/usr/bin/python3

from map import Map
from population import Population
from graphics import save_svg

def main():
    map = Map("test.map")
    population = Population(map, 100, 10, 20)
    for i in range(50):
        filename = "test_{:03d}.svg".format(i)
        save_svg(filename, map, population.tracks)
        population.evolve()


if __name__ == "__main__":
    main()
