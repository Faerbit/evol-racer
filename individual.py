import numpy as np
from random import uniform as random

class Indivdual():

    def __init__(self, track, min, max, middle_nodes=8):
        self.track = track
        self.middle_nodes = middle_nodes
        self.min = min
        self.max = max
        self.input_matrix = self.generate_random_matrix(8, 8, min, max)
        self.output_matrix = self.generate_random_matrix(8, 2, min, max)
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
                string += str(random(min, max)) + " "
            string = string[:-1] + "; "
        string = string [:-2]
        return np.matrix(string)


    def get_input_vector(self):
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
        ret_array = np.array([distance_left, distance_up, distance_right, distance_down,
            target_distance_x, target_distance_y, x_velocity, y_velocity])
        return ret_array
