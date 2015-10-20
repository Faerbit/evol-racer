# coding: utf-8

# Original code from http://lethain.com/genetic-algorithms-cool-name-damn-simple/

from random import randint, random
from operator import add
from functools import reduce
from math import sin, cos, pi, sqrt
from track import Track, Vector

class Population():
    """ A population of tracks."""

    def individual(self):
        """"Creates a member of the population."""
        track = Track()
        work = True
        while work:
            # choose angle
            angle = random() * 2 * pi
            # choose length
            length = random() * self.max_acceleration
            x = int(round(sin(angle) * length))
            y = int(round(cos(angle) * length))
            acceleration_vector = Vector(x, y)
            work = track.accelerate(acceleration_vector):


    def __init__(self, count, max_acceleration, collision_penalty):
        """
        Creates a number of individuals (i.e. a population).

        count: the number of individuals in the population
        """
        self.collision_penalty = collision_penalty
        self.max_acceleration = max_acceleration
        self.tracks = []
        for i in range(count):
            self.tracks.append(self.individual())


    def fitness(self, individual, target):
        """
        Determine the fitness of an individual. Lower is better.

        individual: the individual to evaluate
        target: the target on the map
        """
        distance_x = float(individual.positions[-1].x - target.x)
        distance_y = float(individual.positions[-1].y - target.y)
        distance = sqrt(distance_x * distance_x + distance_y * distance_y)
        length = len(individual.positions)
        collision_penalty = 0
        if individuals.collision:
            collision_penalty = self.collision_penalty
        return distance + length + collision_penalty


    def grade(population):
        """Find average fitness for a population."""
        sum = 0
        for track in population:
            fitness, _ = track
            sum += fitness
        return sum/len(population)



    def evolve(target, retain=0.2, random_select=0.05, mutate=0.01):
        graded = [ (fitness(x, target), x) for x in tracks ]
        graded = [ x[1] for x in sorted(graded) ]
        retain_length = int(len(graded)*retain)
        parents = graded[:retain_length]

        # randomly add other individuals to promote genetic diversity
        for individual in graded[retain_length:]:
            if random_select > random():
                parents.append(individual)

        # mutate some individuals
        for individual in parents:
            if mutate > random():
                pos_to_mutate = randint(0, len(individual.acceleration_vectors) - 1)
                # choose angle
                angle = random() * 2 * pi
                # choose length
                length = random() * self.max_acceleration
                x = int(round(sin(angle) * length))
                y = int(round(cos(angle) * length))
                acceleration_vector = Vector(x, y)
                individual.acceleration_vectors[pos_to_mutate] = acceleration_vector

        # crossover parents to create children
        parents_length = len(parents)
        desired_length = len(population) - parents_length
        children = []
        for i in range(desired_length):
            male = randint(0, parents_length - 1)
            female = randint(0, parents_length - 1)
            if male != female:
                male = parents[male]
                female = parents[female]
                half = int(len(male) / 2)
                child = Track()
                child.acceleration_vectors = male.acceleration_vectors[:half] +
                    female.acceleration_vectors[half:]
                for i in range(acceleration_vectors):
                    child.accelerate(i)
                children.append(child)

        parents.extend(children)


def main():
    target      = 371
    p_count     = 100
    i_length    = 5
    i_min       = 0
    i_max       = 100
    p = population(p_count, i_length, i_min, i_max)
    fitness_history = [grade(p,target),]
    for i in range(100):
        p = evolve(p, target)
        fitness_history.append(grade(p, target))
        if grade(p, target) == 0:
            break

    print(str(len(fitness_history)) + " generations were needed:")
    for datum in fitness_history:
        print(datum)
    print(p)


if __name__ == "__main__":
    main()
