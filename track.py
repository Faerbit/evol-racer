from map import Map
from intersect import do_intersect, intersect_point
from graphics import save_svg
from random import random
import numpy as np

class Track():
    """Represents a track a car could take across the map."""

    def __init__(self, map, limit_to_ints=True):
        """
        Creates a track.

        map: the map on which the track should be
        """
        self.map = map
        self.limit_to_ints = limit_to_ints
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
            if self.limit_to_ints:
                limited_vector = np.array([int(limited_vector[0]), int(limited_vector[1])])
            return limited_vector
        else:
            return vector

    def distance(self):
        """
        Calculates the euclidean distance
        from the last position to the target.
        """
        vector = self.positions[-1] - self.map.target
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
        elif self.distance() == 0 and np.array_equal(self.velocity_vector, np.array([0, 0])):
            return False
        else:
            return True


    def check_collisions(self, from_position_index=1, verbose=False):
        """
        Check if track collides with map.

        from_position_index: check only position from this index
        verbose: verbosity flag
        """
        if from_position_index >= len(self.positions):
            raise Exception("from_position_index: Index out of range")
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

    def check_distance_to_wall(self, direction):
        """
        Returns the distance to the wall in the given direction.
        direction: vector in the given direciton,
            must be at least of unit length
        """
        if np.linalg.norm(direction) < 1:
            raise Exception("Direction vector must be at least of unit length")
        # is long enough in any case
        direction = (self.positions[-1],
                self.positions[-1] + (self.map.size[0] + self.map.size[1]) * direction)

        # is large enough in any case
        distance = self.map.size[0] + self.map.size[1]
        for wall in self.map.map:
            if do_intersect(direction, wall):
                point = intersect_point(direction, wall)
                new_distance = np.linalg.norm(self.positions[-1] - point)
                distance = min(distance, new_distance)
        return distance
