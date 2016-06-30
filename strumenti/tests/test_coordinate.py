#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Module with unit tests for coordinate.

.. moduleauthor:: Timothy Helton <timothy.j.helton@gmail.com>
"""

import numpy as np
import pytest
from strumenti import coordinate


__version__ = '1.0.2'


class SampleData:

    cart2d_single = np.array([[3, 4]])
    cart2d_multi = np. array([[3, 4], [6, 7]])
    cart3d_single = np.array([[3, 4, 5]])
    cart3d_multi = np.array([[3, 4, 5], [6, 7, 8]])

    pol_single_radian = np.array([[3, np.pi / 6]])
    pol_single_degree = np.array([[3, 30]])
    pol_multi_radian = np.array([[3, np.pi / 6], [6, np.pi / 3]])
    pol_multi_degree = np.array([[3, 30], [6, 60]])

    cyl_single_radian = np.c_[pol_single_radian, [5]]
    cyl_single_degree = np.c_[pol_single_degree, [5]]
    cyl_multi_radian = np.c_[pol_multi_radian, [5, 8]]
    cyl_multi_degree = np.c_[pol_multi_degree, [5, 8]]

    sphere_single_3d_radian = np.array([[3, np.pi / 6, np.pi / 9]])
    sphere_single_3d_degree = np.array([[3, 30, 20]])
    sphere_multi_3d_radian = np.array([[3, np.pi / 6, np.pi / 9],
                                       [6, np.pi / 3, np.pi / 4]])
    sphere_multi_3d_degree = np.array([[3, 30, 20], [6, 60, 45]])

    empty = np.arange(0)


class TestElementDimension(SampleData):

    def test__empty(self):
        with pytest.raises(SystemExit):
            coordinate.element_dimension(self.empty, 2)

    def test__wrong_values(self):
        with pytest.raises(SystemExit):
            coordinate.element_dimension(self.cart3d_multi, 2)

    def test__int_values(self):
        assert coordinate.element_dimension(self.cart2d_multi, 2) == 2

    def test__list_values(self):
        assert coordinate.element_dimension(self.cart2d_multi, [2, 3]) == 2


class TestCart2Pol(SampleData):

    def test__empty(self):
        with pytest.raises(SystemExit):
            coordinate.cart2pol(self.empty)

    def test__2d_single(self):
        assert np.allclose(coordinate.cart2pol(self.cart2d_single),
                           [[5, 0.9272952]])

    def test__2d_single_degree(self):
        assert np.allclose(coordinate.cart2pol(self.cart2d_single, True),
                           np.array([[5, 53.1301023]]))

    def test__2d_multi(self):
        assert np.allclose(coordinate.cart2pol(self.cart2d_multi),
                           np.array([[5, 0.9272952], [9.2195444, 0.8621700]]))

    def test__2d_multi_degree(self):
        assert np.allclose(coordinate.cart2pol(self.cart2d_multi, True),
                           np.array([[5, 53.1301023], [9.2195444, 49.3987053]]))

    def test__3d_single(self):
        assert np.allclose(coordinate.cart2pol(self.cart3d_single),
                           np.array([[5, 0.9272952, 5]]))

    def test__3d_single_degree(self):
        assert np.allclose(coordinate.cart2pol(self.cart3d_single, True),
                           np.array([[5, 53.1301023, 5]]))

    def test__3d_multi(self):
        assert np.allclose(coordinate.cart2pol(self.cart3d_multi),
                           np.array([[5, 0.9272952, 5],
                                     [9.2195444, 0.8621700, 8]]))

    def test__3d_multi_degree(self):
        assert np.allclose(coordinate.cart2pol(self.cart3d_multi, True),
                           np.array([[5, 53.1301023, 5],
                                     [9.2195444, 49.3987053, 8]]))


class TestCart2sphere(SampleData):

    def test__empty(self):
        with pytest.raises(SystemExit):
            coordinate.cart2sphere(self.empty)

    def test__3d_single(self):
        assert np.allclose(coordinate.cart2sphere(self.cart3d_single),
                           np.array([[7.0710678, 0.9272952, 0.7853981]]))

    def test__3d_single_degree(self):
        assert np.allclose(coordinate.cart2sphere(self.cart3d_single, True),
                           np.array([[7.0710678, 53.1301023, 45]]))

    def test__3d_multi(self):
        assert np.allclose(coordinate.cart2sphere(self.cart3d_multi),
                           np.array([[7.0710678, 0.9272952, 0.7853981],
                                     [12.2065556, 0.8621700, 0.8561033]]))

    def test__3d_multi_degree(self):
        assert np.allclose(coordinate.cart2sphere(self.cart3d_multi, True),
                           np.array([[7.0710678, 53.1301023, 45],
                                     [12.2065556, 49.3987053, 49.0511101]]))


class TestPol2Cart(SampleData):

    def test__empty(self):
        with pytest.raises(SystemExit):
            coordinate.pol2cart(self.empty)

    def test__polar_3d_single(self):
        assert np.allclose(coordinate.pol2cart(self.pol_single_radian),
                           np.array([[2.5980762, 1.5]]))

    def test__polar_3d_single_degree(self):
        assert np.allclose(coordinate.pol2cart(self.pol_single_degree, True),
                           np.array([[2.5980762, 1.5]]))

    def test__polar_3d_multi(self):
        assert np.allclose(coordinate.pol2cart(self.pol_multi_radian),
                           np.array([[2.5980762, 1.5], [3, 5.1961524]]))

    def test__polar_3d_multi_degree(self):
        assert np.allclose(coordinate.pol2cart(self.pol_multi_degree, True),
                           np.array([[2.5980762, 1.5], [3, 5.1961524]]))

    def test__cylindrical_3d_single(self):
        assert np.allclose(coordinate.pol2cart(self.cyl_single_radian),
                           np.array([[2.5980762, 1.5, 5]]))

    def test__cylindrical_3d_single_degree(self):
        assert np.allclose(coordinate.pol2cart(self.cyl_single_degree, True),
                           np.array([[2.5980762, 1.5, 5]]))

    def test__cylindrical_3d_multi(self):
        assert np.allclose(coordinate.pol2cart(self.cyl_multi_radian),
                           np.array([[2.5980762, 1.5, 5], [3, 5.1961524, 8]]))

    def test__cylindrical_3d_multi_degree(self):
        assert np.allclose(coordinate.pol2cart(self.cyl_multi_degree, True),
                           np.array([[2.5980762, 1.5, 5], [3, 5.1961524, 8]]))


class TestSphere2Cart(SampleData):

    def test__empty(self):
        with pytest.raises(SystemExit):
            coordinate.sphere2cart(self.empty)

    def test__3d_single(self):
        assert np.allclose(coordinate.sphere2cart(self.sphere_single_3d_radian),
                           np.array([[0.8885943, 0.5130302, 2.8190778]]))

    def test__3d_single_degree(self):
        assert np.allclose(coordinate.sphere2cart(self.sphere_single_3d_degree,
                                                  True),
                           np.array([[0.8885943, 0.5130302, 2.8190778]]))

    def test__3d_multi(self):
        assert np.allclose(coordinate.sphere2cart(self.sphere_multi_3d_radian),
                           np.array([[0.8885943, 0.5130302, 2.8190778],
                                     [2.1213203, 3.6742346, 4.2426406]]))

    def test__3d_multi_degree(self):
        assert np.allclose(coordinate.sphere2cart(self.sphere_multi_3d_degree,
                                                  True),
                           np.array([[0.8885943, 0.5130302, 2.8190778],
                                     [2.1213203, 3.6742346, 4.2426406]]))
