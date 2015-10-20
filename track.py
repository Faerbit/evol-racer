from collections import namedtuple
from map import Map, Point
from intersect import do_intersect
from graphics import save_svg

Vector = namedtuple("Vector", ["x", "y"])


class Track():
    """ Represents a track a car could take across the map. """

    def __init__(self, map):
        self.map = map
        self.velocity_vector = Vector(0, 0)
        self.acceleration_vectors = [Vector(0,0)]
        self.positions = [map.start]
        self.collision = False


    def accelerate(self, vector, check=True, last_run=False):
        """ Accelerate into the given direction. """
        self.acceleration_vectors.append(vector)
        self.velocity_vector = Vector(self.velocity_vector.x + vector.x,
                                      self.velocity_vector.y + vector.y)
        new_position = Point(self.positions[-1].x + self.velocity_vector.x,
                             self.positions[-1].y + self.velocity_vector.y)
        self.positions.append(new_position)
        if check:
            if last_run:
                return False
            elif self.positions[-1] == map.target:
                # accelerate one last time because the car must stop at the target
                self.accelerate(self, Vector(0,0), last_run=True)
            elif self.check_collisions(self, len(self.positions) - 1):
                self.collision = True
                return False
            else:
                return True


    def check_collisions(self, from_position_index=1, verbose=False):
        """ Check if track collides with map. """
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


def main():
    map = Map()
    map.load("test.map")
    track = Track(map)
    for i in range(3):
        track.accelerate(Vector(10, i))
        print(track.positions)
        track.check_collisions(verbose=True)
        filename = "test_{:03d}.svg".format(i)
        save_svg(filename, map, [track.positions])



if __name__ == "__main__":
    main()
