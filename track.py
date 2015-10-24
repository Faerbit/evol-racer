from collections import namedtuple
from map import Map, Point
from intersect import do_intersect
from graphics import save_svg
from math import sqrt
from random import random

Vector = namedtuple("Vector", ["x", "y"])


class Track():
    """Represents a track a car could take across the map."""

    def __init__(self, map):
        """
        Creates a track.

        map: the map on which the track should be
        """
        self.map = map
        self.velocity_vector = Vector(0, 0)
        self.acceleration_vectors = [Vector(0,0)]
        self.positions = [map.start]
        self.collision = False

    def __repr__(self):
        return str(self.acceleration_vectors)

    def limit_vector(self, vector):
        """Limits the vector if longer than max_acceleration."""
        length = sqrt(vector.x * vector.x + vector.y * vector.y)
        if length > self.map.max_acceleration:
            vector_x = int(vector.x * 1/length *
                           self.map.max_acceleration)
            vector_y = int(vector.y * 1/length *
                           self.map.max_acceleration)
            return Vector(vector_x, vector_y)
        else:
            return vector


    def brake_vector(self):
        """Calulates a break vector."""
        return Vector(-self.velocity_vector.x, -self.velocity_vector.y)


    def distance(self):
        """
        Calcualtes the euclidean distance
        from the last position to the target.
        """
        dist_x = self.positions[-1].x - self.map.target.x
        dist_y = self.positions[-1].y - self.map.target.y
        return sqrt(dist_x * dist_x + dist_y * dist_y)



    def accelerate(self, vector, check=True, random_braking=True, generating=False, _braking=False):
        """
        Accelerate into the given direction.

        vector: acceleration vector
        check: if set the function checks if further acceleration is
            possible/necessary
        random_braking: if set the function randomly breaks the nearer
            the track gets to the target
        generating: if set the function will reset the track if it collides
        _braking: internal parameter
        """
        vector = self.limit_vector(vector)
        self.acceleration_vectors.append(vector)
        self.velocity_vector = Vector(self.velocity_vector.x + vector.x,
                                      self.velocity_vector.y + vector.y)
        new_position = Point(self.positions[-1].x + self.velocity_vector.x,
                             self.positions[-1].y + self.velocity_vector.y)
        self.positions.append(new_position)
        if check:
            if _braking:
                if self.velocity_vector == Vector(0, 0):
                    return False
                else:
                    self.accelerate(self.brake_vector(), _braking=True)
            # brake if near enough to the target
            elif (self.distance() < self.map.max_acceleration * 2.5) and random_braking:
                if ((-1/(self.map.max_acceleration * 2.5)) * self.distance() + 1) > random():
                    self.accelerate(self.brake_vector(), _braking=True)
                else:
                    return True
            elif self.check_collisions(len(self.positions) - 1):
                if generating:
                    self.__init__(self.map)
                    return True
                else:
                    self.collision = True
                    return False
            else:
                return True


    def check_collisions(self, from_position_index=1, verbose=False):
        """
        Check if track collides with map.

        from_position_index: check only position from this index
        verbose: verbosity flag
        """
        for i in range(from_position_index, len(self.positions)):
            for wall in self.map.map:
                if do_intersect((self.positions[i-1], self.positions[i]),
                                 wall):
                    if verbose:
                        print("Collision detected.")
                    return True

        if verbose:
            print("No collision detected.")
        return False


    def approximate_positions(self, positions):
        """
        Tries to accelerate in such a way to reach the given positions.
        """
        for position in positions:
            # calculate the acceleration vector to the next position
            accelerate_vector_x = (-self.positions[-1].x
                - self.velocity_vector.x + position.x)
            accelerate_vector_y = (-self.positions[-1].y
                - self.velocity_vector.y + position.y)
            if not self.accelerate(
                Vector(accelerate_vector_x, accelerate_vector_y)):
                break
