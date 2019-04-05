import unittest

import helpers
import numpy as np

class TestHelpers(unittest.TestCase):
    """ Poprawnosc"""
    def test_poprawnosc_100_vol(self):
        a=np.array([[1,1],[1,1]])
        b=np.array([[1,1],[1,1]])
        self.assertEqual(1.0,helpers.poprawnoscWyniku(a,b))
    def test_poprawnosc_0_vol(self):
        a = np.array([[1, 1], [0, 1]])
        b = np.array([[0,0],[1,0]])
        self.assertEqual(0.0, helpers.poprawnoscWyniku(a, b))
    def test_poprawnosc_50_vol(self):
        a = np.array([[1, 0], [1, 1]])
        b = np.array([[1, 0], [0, 0]])
        self.assertEqual(0.5, helpers.poprawnoscWyniku(a, b))
    def test_poprawnosc_33_vol(self):
        a = np.array([[1, 1,0], [1, 1,0]])
        b = np.array([[1,0, 1], [1, 0,1]])
        self.assertEqual(1/3, helpers.poprawnoscWyniku(a, b))
    def test_poprawnosc_error(self):
        a = np.array([[1, 1,0], [1, 1,0]])
        b = np.array([[1,0], [1, 0]])
        with self.assertRaises(ValueError):
            helpers.poprawnoscWyniku(a, b)
    def test_podzial_4x4_3(self):
        a=np.array([[1,2,3,4],[5,6,7,8],[9,0,11,12],[13,14,15,16]])
        b=[[[1, 2, 3], [5, 6, 7], [9, 0, 11]], [[2, 3, 4], [6, 7, 8], [0, 11, 12]], [[5, 6, 7], [9, 0, 11], [13, 14, 15]], [[6, 7, 8], [0, 11, 12], [14, 15, 16]]]
        self.assertEqual(b,helpers.podzialNaCzesci(a,3))
if __name__ == '__main__':
    unittest.main()