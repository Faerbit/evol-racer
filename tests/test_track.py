from unittest import TestCase
from track import Track
from map import Map
import numpy as np
from numpy.testing import assert_array_almost_equal as assertArrayEqual
from tests.mocks import mock_open

map_data = ("w 0 0 0 100\n"
            "w 0 100 100 100\n"
            "w 100 100 100 0\n"
            "w 100 0 0 0\n"
            "w 50 20 50 70\n"
            "s 20 30\n"
            "t 80 30\n")

class TestTrack(TestCase):

    @classmethod
    def setUpClass(cls):
        with mock_open(map_data):
            cls.map = Map(10, "map")

    def setUp(self):
        self.track = Track(self.map)

    def test_starts_not_moving(self):
        vector = np.array([0,0])
        assertArrayEqual(self.track.velocity_vector, vector)

    def test_starts_not_accelerating(self):
        vector = np.array([0,0])
        assertArrayEqual(self.track.acceleration_vectors[-1], vector)

    def test_starts_at_start(self):
        assertArrayEqual(self.track.positions[-1], self.map.start)

    def test_starts_not_colliding(self):
        self.assertEqual(self.track.collision, False)

    def test_limit_vector_limits_vector(self):
        unlimited_vector = np.array([10, 3])
        limited_vector = np.array([9, 2])
        assertArrayEqual(self.track.limit_vector(unlimited_vector), limited_vector)

    def test_limit_vector_does_not_limit_short_enough_vectors(self):
        vector = np.array([2,3])
        assertArrayEqual(self.track.limit_vector(vector), vector)

    def test_accelerate_1(self):
        vector = np.array([2,3])
        self.track.accelerate(vector)
        assertArrayEqual(self.track.positions[-1], vector)

    def test_accelerate_returns_true_if_succesful(self):
        vector = np.array([2,3])
        self.assertEqual(self.track.accelerate(vector), True)

    def test_distance(self):
        self.assertEqual(self.track.distance(), 60)

    def test_check_collisons(self):
        self.assertTrue(False)
