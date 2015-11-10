from unittest import TestCase
from track import Track
from map import Map
import numpy as np
from numpy.testing import assert_array_almost_equal as assertArrayEqual
from numpy.testing import assert_almost_equal as assertAlmostEqual
from tests.mocks import mock_open

map_data = ("w 0 0 0 100\n"
            "w 0 100 100 100\n"
            "w 100 100 100 0\n"
            "w 100 0 0 0\n"
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

    def test_limit_vector_limits_vector_int(self):
        unlimited_vector = np.array([10, 3])
        limited_vector = np.array([9, 2])
        assertArrayEqual(self.track.limit_vector(unlimited_vector), limited_vector)

    def test_limit_vector_limits_vector_float(self):
        self.track = Track(self.map, False)
        unlimited_vector = np.array([10, 3])
        limited_vector = np.array([9.57826285, 2.87347885])
        assertArrayEqual(self.track.limit_vector(unlimited_vector), limited_vector)

    def test_limit_vector_does_not_limit_short_enough_vectors(self):
        vector = np.array([2,3])
        assertArrayEqual(self.track.limit_vector(vector), vector)

    def test_accelerate_1(self):
        accel_vector = np.array([2,3])
        self.track.accelerate(accel_vector)
        new_pos = np.array([22, 33])
        assertArrayEqual(self.track.positions[-1], new_pos)

    def test_accelerate_2(self):
        accel_vector = np.array([2,3])
        self.track.accelerate(accel_vector)
        accel_vector = np.array([3,2])
        self.track.accelerate(accel_vector)
        new_pos = np.array([27, 38])
        assertArrayEqual(self.track.positions[-1], new_pos)

    def test_accelerate_2(self):
        accel_vector = np.array([2,3])
        self.track.accelerate(accel_vector)
        accel_vector = np.array([3,2])
        self.track.accelerate(accel_vector)
        accel_vector = np.array([-5,-5])
        self.track.accelerate(accel_vector)
        new_pos = np.array([27, 38])
        assertArrayEqual(self.track.positions[-1], new_pos)

    def test_accelerate_acceleration_vectors(self):
        new_accel_vector = np.array([2,3])
        self.track.accelerate(new_accel_vector)
        old_accel_vector = np.array([0, 0])
        assertArrayEqual(self.track.acceleration_vectors, [old_accel_vector, new_accel_vector])

    def test_accelerate_returns_true_if_succesful(self):
        vector = np.array([2,3])
        self.assertTrue(self.track.accelerate(vector))

    def test_distance(self):
        self.assertEqual(self.track.distance, 60)

    def test_distance_after_accel(self):
        accel_vector = np.array([2,3])
        self.track.accelerate(accel_vector)
        assertAlmostEqual(self.track.distance, 58.0775343829)

    def test_collided(self):
        accel_vector = np.array([-10, 0])
        self.track.accelerate(accel_vector)
        self.track.accelerate(accel_vector)
        self.assertTrue(self.track.collision)

    def test_accelerate_returns_false_if_not_succesful(self):
        accel_vector = np.array([-10, 0])
        self.track.accelerate(accel_vector)
        self.assertFalse(self.track.accelerate(accel_vector))

    def test_accelerate_returns_false_if_at_target(self):
        accel_vector = np.array([10, 0])
        self.track.accelerate(accel_vector)
        accel_vector = np.array([0, 0])
        for i in range(5):
            self.track.accelerate(-accel_vector)
        accel_vector = np.array([-10, 0])
        self.assertFalse(self.track.accelerate(accel_vector))

    def test_check_collisions(self):
        accel_vector = np.array([-10, 0])
        self.track.accelerate(accel_vector)
        accel_vector = np.array([  0, 0])
        self.track.accelerate(accel_vector)
        self.assertTrue(self.track.check_collisions())

    def test_check_collisions_index_viable(self):
        with self.assertRaises(Exception):
            self.track.check_collisions(2)

    def test_check_collisions_index_viable(self):
        with self.assertRaises(Exception):
            self.track.check_collisions(1)

    def test_check_collisions_with_index(self):
        accel_vector = np.array([-10, 0])
        self.track.accelerate(accel_vector)
        accel_vector = np.array([  0, 0])
        self.track.accelerate(accel_vector)
        accel_vector = np.array([ 10, 0])
        self.track.accelerate(accel_vector)
        self.track.accelerate(accel_vector)
        accel_vector = np.array([  0, 0])
        self.track.accelerate(accel_vector)
        self.assertFalse(self.track.check_collisions(5))

    def test_distance_to_wall_1(self):
        self.assertEqual(self.track.check_distance_to_wall(np.array([-1,  0])), 20)

    def test_distance_to_wall_2(self):
        self.assertEqual(self.track.check_distance_to_wall(np.array([ 1,  0])), 80)

    def test_distance_to_wall_3(self):
        self.assertEqual(self.track.check_distance_to_wall(np.array([ 0,  1])), 70)

    def test_distance_to_wall_4(self):
        self.assertEqual(self.track.check_distance_to_wall(np.array([ 0, -1])), 30)

    def test_distance_to_wall_5(self):
        self.track.accelerate(np.array([10, 0]))
        self.assertEqual(self.track.check_distance_to_wall(np.array([-1,  0])), 30)

    def test_distance_to_wall_6(self):
        self.assertAlmostEqual(self.track.check_distance_to_wall(
            np.array([ 0.71,  0.71])), 98.994949366)

    def test_distance_to_wall_too_short_direction_vector(self):
        with self.assertRaises(Exception):
            self.track.check_distance_to_wall(np.array([0.1, 0.1]))

    def test_length_1(self):
        self.assertEqual(self.track.length, 1)

    def test_length_2(self):
        self.track.accelerate(np.array([0, 1]))
        self.assertEqual(self.track.length, 2)

    def test_length_3(self):
        self.track.accelerate(np.array([0, 1]))
        self.track.accelerate(np.array([0, 1]))
        self.assertEqual(self.track.length, 3)

    def test_target_vector_1(self):
        assertArrayEqual(self.track.target_vector, np.array([60, 0]))

    def test_target_vector_2(self):
        self.track.accelerate(np.array([0, 1]))
        assertArrayEqual(self.track.target_vector, np.array([60, -1]))

    def test_target_vector_3(self):
        self.track.accelerate(np.array([-5, 5]))
        assertArrayEqual(self.track.target_vector, np.array([65, -5]))
