import numpy as np

class Map():
    """
    Representing a map which contains walls, a starting point and a target.
    """

    def __init__(self, max_acceleration, filename=""):
        """
        Creates a map.

        max_acceleration: the maximum acceleration allowed on the map
        filename: if given loads the map directly
        """
        self.map = list()
        self.start = np.array([0, 0])
        self.target = np.array([0, 0])
        self.size = np.array([0, 0])
        self.max_acceleration = int(max_acceleration)
        if filename:
            self.load(filename)

    def __repr__(self):
        return "Dimensions: {}, {} Walls: {}".format(self.size[0], self.size[1], self.map)

    def add_line(self, p, q):
        """
        Adds a line from p to q.

        p: line point
        q: line point
        """
        self.map.append((p, q))

    def load(self, filename):
        """
        Loads a map from a file.

        filename: the filename of the map file
        """
        for line in open(filename):
            split_line = line.split()
            # if line contains any data
            if split_line:
                if line[0] == "#":
                    pass
                elif split_line[0].lower() == "w":
                    # update dimensions
                    self.size[0] = max(self.size[0], int(split_line[1]))
                    self.size[0] = max(self.size[0], int(split_line[3]))
                    self.size[1] = max(self.size[1], int(split_line[2]))
                    self.size[1] = max(self.size[1], int(split_line[4]))

                    p = np.array([int(split_line[1]), int(split_line[2])])
                    q = np.array([int(split_line[3]), int(split_line[4])])
                    self.add_line(p, q)
                elif split_line[0].lower() == "s":
                        self.start = np.array([int(split_line[1]), int(split_line[2])])
                elif split_line[0].lower() == "t":
                        self.target = np.array([int(split_line[1]), int(split_line[2])])
                else:
                    raise Exception("Unsupported character at the beginning of line: " + line)
