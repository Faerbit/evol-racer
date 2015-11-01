from unittest import TestCase
from intersect import do_intersect, on_segment, orientation
import numpy as np

class TestIntersect(TestCase):

    def test_intersect_1(self):
        p = (np.array([ 1,  1]), np.array([10,  1]))
        q = (np.array([ 1,  2]), np.array([10,  2]))
        self.assertFalse(do_intersect(p, q))

    def test_intersect_2(self):
        p = (np.array([10,  0]), np.array([ 0, 10]))
        q = (np.array([ 0,  0]), np.array([10,  2]))
        self.assertTrue(do_intersect(p, q))

    def test_intersect_3(self):
        p = (np.array([-5,  5]), np.array([ 0,  0]))
        q = (np.array([ 1,  1]), np.array([10, 10]))
        self.assertFalse(do_intersect(p, q))

    def test_on_segment_1(self):
        p1 = np.array([1, 2])
        p2 = np.array([1, 2])
        p3 = np.array([1, 2])
        self.assertTrue(on_segment(p1, p2, p3))

    def test_on_segment_2(self):
        p1 = np.array([1, 2])
        p2 = np.array([2, 3])
        p3 = np.array([1, 3])
        self.assertFalse(on_segment(p1, p2, p3))

    def test_on_segment_3(self):
        p1 = np.array([-1, -2])
        p2 = np.array([ 2,  3])
        p3 = np.array([ 1,  3])
        self.assertFalse(on_segment(p1, p2, p3))

    def test_on_segment_4(self):
        p1 = np.array([-1, 3])
        p2 = np.array([ 1, 3])
        p3 = np.array([ 5, 3])
        self.assertTrue(on_segment(p1, p2, p3))

    def test_orientation_1(self):
        p1 = np.array([1, 2])
        p2 = np.array([1, 2])
        p3 = np.array([1, 2])
        self.assertEqual(orientation(p1, p2, p3), 0)

    def test_orientation_2(self):
        p1 = np.array([-1, 3])
        p2 = np.array([ 1, 3])
        p3 = np.array([ 5, 3])
        self.assertEqual(orientation(p1, p2, p3), 0)

    def test_orientation_3(self):
        p1 = np.array([-1, -2])
        p2 = np.array([ 2,  3])
        p3 = np.array([ 1,  3])
        self.assertEqual(orientation(p1, p2, p3), 2)

    def test_orientation_4(self):
        p1 = np.array([-1, -2])
        p2 = np.array([ 1,  3])
        p3 = np.array([ 2,  3])
        self.assertEqual(orientation(p1, p2, p3), 1)

    def test_orientation_5(self):
        p1 = np.array([1, 2])
        p2 = np.array([2, 3])
        p3 = np.array([1, 3])
        self.assertEqual(orientation(p1, p2, p3), 2)

    def test_orientation_6(self):
        p1 = np.array([1, 2])
        p2 = np.array([1, 3])
        p3 = np.array([2, 3])
        self.assertEqual(orientation(p1, p2, p3), 1)
