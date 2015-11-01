from map import Map
from intersect import do_intersect
from graphics import save_svg
from random import random
import numpy as np

class Track():
    """Represents a track a car could take across the map."""

    def __init__(self, map):
        """
        Creates a track.

        map: the map on which the track should be
        """
        self.map = map
        self.velocity_vector = np.array([0,0])
        self.acceleration_vectors = [np.array([0,0])]
        self.positions = [map.start]
        self.collision = False

    def __repr__(self):
        return str(self.acceleration_vectors)

    def limit_vector(self, vector):
        """Limits the vector if longer than max_acceleration."""
        length = np.linalg.norm(vector)
        if length > self.map.max_acceleration:
            limited_vector = vector * (1/length) * self.map.max_acceleration
            limited_vector = np.array([int(limited_vector[0]), int(limited_vector[1])])
            return limited_vector
        else:
            return vector


    def brake_vector(self):
        """Calulates a break vector."""
        return Vector(-self.velocity_vector.x, -self.velocity_vector.y)


    def distance(self):
        """
        Calculates the euclidean distance
        from the last position to the target.
        """
        vector = self.positions[-1] - self.map.start
        return np.linalg.norm(vector)



    def accelerate(self, vector):
        """
        Accelerate into the given direction.

        vector: acceleration vector

        Returns True if acceleration was succesful and further acceleration
        will be possible. Returns false otherwise.
        """
        vector = self.limit_vector(vector)
        self.acceleration_vectors.append(vector)
        self.velocity_vector += vector
        new_position = self.positions[-1] + self.velocity_vector
        self.positions.append(new_position)
        if self.check_collisions(len(self.positions) - 1):
            self.collision = True
            return False
        elif self.distance() == 0 and self.velocity_vector == np.array([0, 0]):
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
