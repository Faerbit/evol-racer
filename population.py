# Original code from http://lethain.com/genetic-algorithms-cool-name-damn-simple/

from random import randint, random
from operator import add
from functools import reduce
from math import sin, cos, pi, sqrt
from track import Track, Vector
from operator import itemgetter

class Population():
    """ A population of tracks."""

    def individual(self):
        """"Creates a member of the population."""
        track = Track(self.map)
        work = True
        while work:
            # choose angle
            angle = random() * 2 * pi
            # choose length
            length = random() * self.max_acceleration
            x = int(round(sin(angle) * length))
            y = int(round(cos(angle) * length))
            acceleration_vector = Vector(x, y)
            work = track.accelerate(acceleration_vector)
        return track


    def __init__(self, map, count, max_acceleration, collision_penalty):
        """
        Creates a number of individuals (i.e. a population).

        count: the number of individuals in the population
        """
        self.map = map
        self.collision_penalty = collision_penalty
        self.max_acceleration = max_acceleration
        self.tracks = []
        for i in range(count):
            self.tracks.append(self.individual())


    def fitness(self, individual):
        """
        Determine the fitness of an individual. Lower is better.

        individual: the individual to evaluate
        """
        distance_x = float(individual.positions[-1].x - self.map.target.x)
        distance_y = float(individual.positions[-1].y - self.map.target.y)
        distance = sqrt(distance_x * distance_x + distance_y * distance_y)
        length = len(individual.positions)
        collision_penalty = 0
        if individual.collision:
            collision_penalty = self.collision_penalty
        return distance + length + collision_penalty


    def grade(self, population):
        """Find average fitness for a population."""
        sum = 0
        for track in population:
            fitness, _ = track
            sum += fitness
        return sum/len(population)



    def evolve(self, retain=0.2, random_select=0.05, mutate=0.01):
        graded = [ (self.fitness(x), x) for x in self.tracks ]
        graded = [ x[1] for x in sorted(graded, key=itemgetter(0)) ]
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
        desired_length = len(self.tracks) - parents_length
        children = []
        for i in range(desired_length):
            male = 0
            female = 0
            while male == female:
                male = randint(0, parents_length - 1)
                female = randint(0, parents_length - 1)
            male = parents[male]
            female = parents[female]
            half_male = int(len(male.acceleration_vectors) / 2)
            half_female = int(len(female.acceleration_vectors) / 2)
            child = Track(self.map)
            child.acceleration_vectors = (male.acceleration_vectors[:half_male] +
                female.acceleration_vectors[half_female:] )
            for i, vector in enumerate(child.acceleration_vectors):
                working = child.accelerate(vector)
                if not working:
                    child.acceleration_vectors = child.acceleration_vectors[:i]
                    break
            children.append(child)

        parents.extend(children)
        self.tracks = parents


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
