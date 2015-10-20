from collections import namedtuple
from map import Map, Point
from intersect import do_intersect

Vector = namedtuple("Vector", ["x", "y"])


class Track():
    """ Represents a track a car could take across the map. """

    def __init__(self, map):
        self.map = map
        self.velocity_vectors = [Vector(0, 0)]
        self.acceleration_vectors = [Vector(0,0)]
        self.positions = [map.start]


    def accelerate(self, vector):
        """ Accelerate into the given direction. """
        self.acceleration_vectors.append(vector)
        new_velocity_vector = Vector(self.velocity_vectors[-1].x + vector.x,
                                     self.velocity_vectors[-1].y + vector.y)
        self.velocity_vectors.append(new_velocity_vector)
        new_position = Point(self.positions[-1].x + new_velocity_vector.x,
                             self.positions[-1].y + new_velocity_vector.y)
        self.positions.append(new_position)

    def check_collisions(self, from_position_index=1):
        """ Check if track collides with map. """
        for i in range(from_position_index, len(self.positions)):
            for wall in self.map.map:
                if do_intersect((self.positions[i-1], self.positions[i]),
                                 wall):
                    return True

        return False


def main():
    map = Map()
    map.load("test.map")
    track = Track(map)
    track.accelerate(Vector(100, 0))
    print(track.positions)
    if track.check_collisions():
        print("Collision detected.")
    else:
        print("No collision detected.")



if __name__ == "__main__":
    main()
