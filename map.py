import svgwrite
from svgwrite.shapes import Line
from functools import reduce
from collections import namedtuple
from itertools import chain

Point = namedtuple("Point", ["x", "y"])

class Map():
    """
    Representing map which contains walls, a starting point and a target.
    """

    def __init__(self):
        self.map = list()
        self.start = Point(0, 0)
        self.target = Point(0, 0)

    def __repr__(self):
        return str(self.map)

    def add_line(self, p, q):
        """ Adds a line from (p1, p2) to (q1, q2). """
        self.map.append((p, q))

    def load(self, filename):
        """ Loads a map from a file. """
        for line in open(filename):
            split_line = line.split()
            if split_line[0].lower() == "w":
                p = Point(int(split_line[1]), int(split_line[2]))
                q = Point(int(split_line[3]), int(split_line[4]))
                self.add_line(p, q)
            elif split_line[0].lower() == "s":
                    self.start = Point(int(split_line[1]), int(split_line[2]))
            elif split_line[0].lower() == "t":
                    self.target = Point(int(split_line[1]), int(split_line[2]))
            else:
                raise Exception("Unsupported character at the beginning of line: " + line)


    def save_svg(self, filename, offset=5):
        """ Saves a graphical representation of the map to a SVG file. """
        svg = svgwrite.Drawing(filename)
        # get dimensions
        max_x = 0
        max_y = 0
        for line in self.map:
            max_x = max(max_x, max(line[0].x, line[1].x))
            max_y = max(max_y, max(line[0].y, line[1].y))
        # background
        svg.add(svg.rect((0,0), (max_x+2*offset, max_y+2*offset), fill="white"))
        walls = svg.add(svg.g(id="walls", stroke="red"))
        for line in self.map:
            p = (line[0][0] + offset, line[0][1] + offset)
            q = (line[1][0] + offset, line[1][1] + offset)
            walls.add(svg.line(p, q))
        start_x, start_y = self.start
        svg.add(svg.circle((start_x + offset, start_y + offset), 2, fill="green"))
        target_x, target_y = self.target
        svg.add(svg.circle((target_x + offset, target_y + offset), 2, fill="blue"))
        svg.save()

def main():
    _map = Map()
    _map.load("test.map")
    _map.save_svg("test.svg")


if __name__ == "__main__":
    main()
