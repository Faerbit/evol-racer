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
        p = np.array([1, 1])
        q = np.array([2, 2])
        assertArrayEqual(map.map, [(p, q)])

    def test_add_line(self):
        p = np.array([1, 2])
        q = np.array([2, 3])
        self.map.add_line(p, q)
        self.assertEqual(self.map.map, [(p,q)])

    def test_load_comment(self):
        with mock_open("#W 1 1 2 2"):
            self.map.load("map")
        self.assertEqual(self.map.map, [])

    def test_load_empty_line(self):
        with mock_open("\n"):
            self.map.load("map")
        self.assertEqual(self.map.map, [])

    def test_load_line(self):
        with mock_open("W 1 1 2 2"):
            self.map.load("map")
        p = np.array([1, 1])
        q = np.array([2, 2])
        assertArrayEqual(self.map.map, [(p, q)])

    def test_load_start(self):
        with mock_open("S 1 2"):
            self.map.load("map")
        s = np.array([1, 2])
        assertArrayEqual(self.map.start, s)

    def test_load_target(self):
        with mock_open("T 2 1"):
            self.map.load("map")
        t = np.array([2, 1])
        assertArrayEqual(self.map.target, t)

    def test_load_max_size_x(self):
        with mock_open("W 10 1000 20 0"):
            self.map.load("map")
        self.assertEqual(self.map.size[0], 20)

    def test_load_max_size_y(self):
        with mock_open("W 10 10 2000 200"):
            self.map.load("map")
        self.assertEqual(self.map.size[1], 200)

    def test_load_exception(self):
        with mock_open("asdf"):
            with self.assertRaises(Exception):
                self.map.load("map")
