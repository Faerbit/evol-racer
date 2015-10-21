from collections import namedtuple
from map import Map, Point
from intersect import do_intersect
from graphics import save_svg

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


    def accelerate(self, vector, check=True, _last_run=False):
        """
        Accelerate into the given direction.

        vector: acceleration vector
        check: if set the methods checks if further acceleration is
               possible/necessary
        _last_run: internal parameter
        """
        self.acceleration_vectors.append(vector)
        self.velocity_vector = Vector(self.velocity_vector.x + vector.x,
                                      self.velocity_vector.y + vector.y)
        new_position = Point(self.positions[-1].x + self.velocity_vector.x,
                             self.positions[-1].y + self.velocity_vector.y)
        self.positions.append(new_position)
        if check:
            if _last_run:
                return False
            elif self.positions[-1] == self.map.target:
                # accelerate(brake) one last time because the car must stop at the target
                brake_vector = Vector(-vector.x, -vector.y)
                self.accelerate(brake_vector, _last_run=True)
            elif self.check_collisions(len(self.positions) - 1):
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
