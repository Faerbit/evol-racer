# Code adapted from http://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
from enum import Enum
from collections import namedtuple
import timeit
from random import randint
from statistics import mean, stdev, pstdev

Point = namedtuple("Point", ["x", "y"])

class Orientation(Enum):
    colinear            = 0
    clockwise           = 1
    counterclockwise    = 2

def on_segment(p, q, r):
    """
    Given three colinear points p, q, r,
    the function checks if point q lies on line segment pr
    """

    if (q.x <= max(p.x, r.x) and q.x >= min(p.x, r.x) and
            q.y <= max(p.y, r.y) and q.y >= min(p.y, r.y)):
        return True
    else:
        return False

def orientation(p, q, r):
    """
    To find orientation of ordered triplet(p, q, r).
    The function returns following enum values (see Orientation class):
    0 --> p, q and r are colinear
    1 --> clockwise
    2 --> counterclockwise

    See 10th slides from following link for derivation of the formula
    http://www.dcs.gla.ac.uk/~pat/52233/slides/Geometry1x1.pdf
    """
    value = ((q.y - p.y) * (r.x - q.x) -
             (q.x - p.x) * (r.y - q.y))

    if value == 0:
        return Orientation.colinear
    elif value > 0:
        return Orientation.clockwise
    else:
        return Orientation.counterclockwise

def do_intersect(p1, p2, q1, q2):
    """ Returns true if line p1p2 and line q1q2 intersect. """

    o1 = orientation(p1, p2, q1)
    o2 = orientation(p1, p2, q2)
    o3 = orientation(q1, q2, p1)
    o4 = orientation(q1, q2, p2)

    # General case
    if (o1 != o2 and o3 != o4):
        return True

    # Special Cases
    # p1, p2 and q1 are colinear and q1 lies on line p1p2
    if (o1 == Orientation.colinear and on_segment(p1, q1, p2)):
        return True

    # p1, p2 and q2 are colinear and q2 lies on line p1p2
    if (o2 == Orientation.colinear and on_segment(p1, q2, p2)):
        return True

    # q1, q2 and p1 are colinear and p1 lies on line q1q2
    if (o3 == Orientation.colinear and on_segment(q1, p1, q2)):
        return True

    # q1, q2 and p2 are colinear and p2 lies on line q1q2
    if (o4 == Orientation.colinear and on_segment(q1, p2, q2)):
        return True

    # Lines don't intersect
    return False

def do_verbose_intersect(p1, p2, q1, q2):
    """ Prints result of do_intersect. """

    if do_intersect(p1, p2, q1, q2):
        print("Yes!")
        return True
    else:
        print("No!")
        return False

def setup_benchmark():
    """ Generates random points for benchmark purposes. """
    global benchmark_points
    # Generate points
    min = 0
    max = 100
    n = 2000000
    benchmark_points = list()
    for i in range(n):
        p1 = Point(randint(min, max), randint(min, max))
        p2 = Point(randint(min, max), randint(min, max))
        q1 = Point(randint(min, max), randint(min, max))
        q2 = Point(randint(min, max), randint(min, max))
        benchmark_points.append((p1, p2, q1, q2))

def benchmark():
    for lines in benchmark_points:
        do_intersect(lines[0], lines[1], lines[2], lines[3])

def main():
    """ Benchmark """
    setup_benchmark()
    results = (timeit.Timer("benchmark()", setup="from __main__ import benchmark").repeat(10, 1))
    print("Minimum: " + str(min(results)))
    print("Average: " + str(mean(results)))
    print("Population standard deviation: " + str(pstdev(results)))

if __name__ == "__main__":
    main()
