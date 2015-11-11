import numpy as np
from random import uniform
from random import randint
from copy import deepcopy

class Individual():
    """Represents a neural net belonging to a track."""

    def __init__(self, track, min, max, middle_nodes=8):
        self.track = track
        self.middle_nodes = middle_nodes
        self.min = min
        self.max = max
        self.input_matrix = self.generate_random_matrix(8, middle_nodes, min, max)
        self.output_matrix = self.generate_random_matrix(middle_nodes, 2, min, max)
        self.complete_matrix = self.input_matrix * self.output_matrix

    def generate_random_matrix(self, rows, columns, min, max):
        """
        Returns a random matrix

        rows: how many rows the matrix should have
        column: how many column the matrix should have
        min: lower end for the random entries
        max: upper end for the random entries
        """
        string = ""
        for i in range(rows):
            for j in range(columns):
                string += str(uniform(min, max)) + " "
            string = string[:-1] + "; "
        string = string [:-2]
        return np.matrix(string)


    def _get_input_vector(self):
        """
        Returns the input vector for the neural net

        The vector contains the following entries in this order:
        distance to wall in direction (-1, 0)
        distance to wall in direction ( 0, 1)
        distance to wall in direction ( 1, 0)
        distance to wall in direction ( 0,-1)
        distance to target in x direction
        distance to target in y direction
        x velocity
        y velocity
        """
        distance_left  = self.track.check_distance_to_wall(np.array([-1, 0]))
        distance_up    = self.track.check_distance_to_wall(np.array([ 0, 1]))
        distance_right = self.track.check_distance_to_wall(np.array([ 1, 0]))
        distance_down  = self.track.check_distance_to_wall(np.array([ 0,-1]))
        target_vector = self.track.target_vector
        target_distance_x = target_vector[0]
        target_distance_y = target_vector[1]
        x_velocity = self.track.velocity_vector[0]
        y_velocity = self.track.velocity_vector[1]
        ret_array = np.array([distance_left, distance_up, distance_right,
            distance_down, target_distance_x, target_distance_y, x_velocity,
            y_velocity])
        return ret_array

    def timestep(self):
        """
        Takes a timestep.

        Evaluates the inputs and accelerates the track with the output.
        """
        output = self._get_input_vector() * self.complete_matrix
        self.track.accelerate(output)

    def mutate(self):
        """
        Mutates certain factors in the input and output matrices.
        """
        rows, cols = self.input_matrix.shape
        x = randint(0, rows - 1)
        y = randint(0, cols - 1)
        self.input_matrix[x, y] = uniform(self.min, self.max)
        rows, cols = self.output_matrix.shape
        x = randint(0, rows - 1)
        y = randint(0, cols - 1)
        self.output_matrix[x, y] = uniform(self.min, self.max)
        self.complete_matrix = self.input_matrix * self.output_matrix

    def birth(self, mother):
        """
        Returns a new individual which has half of this instance
        and half of the mother instance.
        """
        child = deepcopy(self)
        child.input_matrix = 0.5 * self.input_matrix + 0.5 * mother.input_matrix
        child.output_matrix = 0.5 * self.output_matrix + 0.5 * mother.output_matrix
        child.complete_matrix = child.input_matrix * child.output_matrix
        return child
