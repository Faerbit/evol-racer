from unittest import TestCase
from individual import Indivdual
from track import Track
from map import Map
import numpy as np
from numpy.testing import assert_array_almost_equal as assertArrayEqual
from tests.mocks import mock_open

map_data = ("w 0 0 0 100\n"
            "w 0 100 100 100\n"
            "w 100 100 100 0\n"
            "w 100 0 0 0\n"
            "s 20 30\n"
            "t 80 30\n")

class IndividualTests(TestCase):

    @classmethod
    def setUpClass(cls):
        with mock_open(map_data):
            cls.map = Map(10, "map")

    def setUp(self):
        self.track = Track(self.map)
        self.individual = Indivdual(self.track, 0, 10)

    def test_init_track(self):
        self.assertEqual(self.individual.track, self.track)

    def test_init_middle_nodes(self):
        self.assertEqual(self.individual.middle_nodes, 8)

    def test_init_min(self):
        self.assertEqual(self.individual.min, 0)

    def test_init_max(self):
        self.assertEqual(self.individual.max, 10)

    def test_init_input_matrix(self):
        self.assertEqual(self.individual.input_matrix.shape, (8, 8))

    def test_init_output_matrix(self):
        self.assertEqual(self.individual.output_matrix.shape, (8, 2))

    def test_init_complete_matrix(self):
        self.assertEqual(self.individual.complete_matrix.shape, (8, 2))

    def test_generate_matrix_1(self):
        matrix = self.individual.generate_random_matrix(2, 3, 0, 5)
        self.assertEqual(matrix.shape, (2, 3))

    def test_generate_matrix_2(self):
        matrix = self.individual.generate_random_matrix(8, 5, -5, 25)
        self.assertEqual(matrix.shape, (8, 5))

    def test_generate_matrix_3(self):
        matrix = self.individual.generate_random_matrix(10, 10, -50, 50)
        for i in range(10):
            for j in range(10):
                self.assertEqual(type(matrix.item(i, j)), float)
                self.assertTrue(-50 <= matrix.item(i, j) <= 50)

    def test_input_vector_1(self):
        assertArrayEqual(self.individual.get_input_vector(),
                np.array([20, 70, 80, 30, 60, 0, 0, 0]))

    def test_input_vector_2(self):
        self.individual.track.accelerate(np.array([10, 0]))
        assertArrayEqual(self.individual.get_input_vector(),
                np.array([30, 70, 70, 30, 50, 0, 10, 0]))

    def test_input_vector_3(self):
        self.individual.track.accelerate(np.array([5, -5]))
        assertArrayEqual(self.individual.get_input_vector(),
                np.array([25, 75, 75, 25, 55, 5, 5, -5]))
