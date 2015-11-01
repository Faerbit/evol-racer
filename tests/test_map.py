from unittest import TestCase
from map import Map
import numpy as np
from numpy.testing import assert_array_almost_equal as assertArrayEqual
from tests.mocks import mock_open

class TestMap(TestCase):

    def setUp(self):
        self.map = Map(10)

    def test_init_1(self):
        self.assertEqual(self.map.map, list())

    def test_init_2(self):
        assertArrayEqual(self.map.start, np.array([0, 0]))

    def test_init_3(self):
        assertArrayEqual(self.map.target, np.array([0, 0]))

    def test_init_4(self):
        assertArrayEqual(self.map.size, np.array([0, 0]))

    def test_init_5(self):
        self.assertEqual(self.map.max_acceleration, 10)

    def test_init_loads_file(self):
        with mock_open("W 1 1 2 2"):
            map = Map(10, "map")
        self.assertEqual(map.map, "")


    def test_add_line(self):
        p = np.array([1, 2])
        q = np.array([2, 3])
        self.map.add_line(p, q)
        self.assertEqual(self.map.map, [(p,q)])
