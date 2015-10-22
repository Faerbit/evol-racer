# Based on code from http://lethain.com/genetic-algorithms-cool-name-damn-simple/

from random import randint, random
from operator import add
from functools import reduce
from math import sin, cos, pi, sqrt
from track import Track, Vector
from map import Point
from operator import itemgetter

class Population():
    """ A population of tracks."""

    def individual(self):
        """"Creates a member of the population."""
        track = Track(self.map)
        while track.accelerate(self.random_vector()):
            pass
        return track

    def random_vector(self):
        """Returns a vector of random lenght and direction."""
        vector = Vector(0, 0)
        while vector == Vector(0, 0):
            # choose angle
            angle = random() * 2 * pi
            # choose length
            length = random() * self.map.max_acceleration
            x = int(sin(angle) * length)
            y = int(cos(angle) * length)
            vector = Vector(x, y)
        return vector

    def __init__(self, map, population_size, distance_factor,
                 collision_penalty, retain_percentage, random_select_chance,
                 mutate_chance):
        """
        Creates a number of individuals (i.e. a population).

        map: the map on which the tracks should take place
        population_size: the number of individuals in the population
        distance_factor: a weight for the fitness function
        collision_penalty: fitness function penalty for collisions
        retain_percentage: how much of the population
                           should be retained during evolution
        random_select_chance: how many bad individuals should live on anyway
        mutate_chance: chance for randomly mutating some individuals
        """
        self.map = map
        self.distance_factor = float(distance_factor)
        self.collision_penalty = float(collision_penalty)
        self.retain_percentage = float(retain_percentage)
        self.random_select_chance = float(random_select_chance)
        self.mutate_chance = float(mutate_chance)
        self.tracks = []
        for i in range(int(population_size)):
            self.tracks.append(self.individual())


    def fitness(self, individual):
        """
        Determine the fitness of an individual. Lower is better.

        individual: the individual to evaluate
        """
        # calculate euclidean distance
        distance_x = float(individual.positions[-1].x - self.map.target.x)
        distance_y = float(individual.positions[-1].y - self.map.target.y)
        distance = sqrt(distance_x * distance_x + distance_y * distance_y)
        # weight distance
        distance *= self.distance_factor
        length = len(individual.positions)
        collision_penalty = 0
        if individual.collision:
            collision_penalty = self.collision_penalty
        return distance + length + collision_penalty


    def grade(self, population):
        """
        Find average fitness for the population.

        population: graded population tuples
        """
        sum = 0
        for fitness, _ in population:
            sum += fitness
        return sum/len(population)


    def evolve(self):
        """Evolves the population."""
        graded = [ (self.fitness(x), x) for x in self.tracks ]
        grade = self.grade(graded)
        graded = [ x[1] for x in sorted(graded, key=itemgetter(0)) ]
        retain_length = int(len(graded)*self.retain_percentage)
        parents = graded[:retain_length]

        # randomly add other individuals to promote genetic diversity
        for individual in graded[retain_length:]:
            if self.random_select_chance > random():
                parents.append(individual)

        # mutate some individuals
        for i, _ in enumerate(parents):
            if self.mutate_chance > random():
                pos_to_mutate = randint(0, len(parents[i].positions) - 1)
                mutated_positions = parents[i].positions
                point_x = randint(0, self.map.size_x)
                point_y = randint(0, self.map.size_y)
                mutated_positions[pos_to_mutate] = Point(point_x, point_y)
                mutated_individual = Track(self.map)
                for position in mutated_positions:
                    # calculate the acceleration vector to the next position
                    accelerate_vector_x = (-mutated_individual.positions[-1].x
                        - mutated_individual.velocity_vector.x + position.x)
                    accelerate_vector_y = (-mutated_individual.positions[-1].y
                        - mutated_individual.velocity_vector.y + position.y)
                    if not mutated_individual.accelerate(
                            Vector(accelerate_vector_x, accelerate_vector_y)):
                        break
                parents[i] = mutated_individual


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
            half_male = int(len(male.positions) / 2)
            half_female = int(len(female.positions) / 2)
            child_positions = (male.positions[:half_male] +
                female.positions[half_female:] )
            child = Track(self.map)
            for position in child_positions:
                # calculate the acceleration vector to the next position
                accelerate_vector_x = (-child.positions[-1].x
                    - child.velocity_vector.x + position.x)
                accelerate_vector_y = (-child.positions[-1].y
                    - child.velocity_vector.y + position.y)
                if not child.accelerate(
                    Vector(accelerate_vector_x, accelerate_vector_y)):
                    break
            children.append(child)

        parents.extend(children)
        self.tracks = parents
        return grade
