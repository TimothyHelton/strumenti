#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Module with unit tests for coordinate.

.. moduleauthor:: Timothy Helton <timothy.j.helton@gmail.com>
"""

import numpy as np
import pytest
from strumenti import coordinate


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


def test__element_dimension_empty():
    with pytest.raises(SystemExit):
        coordinate.element_dimension(empty, 2)


def test__element_dimension_wrong_values():
    with pytest.raises(SystemExit):
        coordinate.element_dimension(cart3d_multi, 2)


@pytest.mark.parametrize('array, dim, expected', [
    (cart2d_multi, 2, 2),
    (cart2d_multi, [2, 3], 2)
    ])
def test__element_dimension(array, dim, expected):
    assert coordinate.element_dimension(array, dim) == expected


def test__cart2pol_empty():
    with pytest.raises(SystemExit):
        coordinate.cart2pol(empty)


@pytest.mark.parametrize('pts, deg, expected', [
    (cart2d_single, False, [[5, 0.9272952]]),
    (cart2d_single, True, [[5, 53.1301023]]),
    (cart2d_multi, False, [[5, 0.9272952], [9.2195444, 0.8621700]]),
    (cart2d_multi, True, [[5, 53.1301023], [9.2195444, 49.3987053]]),
    (cart3d_single, False, [[5, 0.9272952, 5]]),
    (cart3d_single, True, [[5, 53.1301023, 5]]),
    (cart3d_multi, False, [[5, 0.9272952, 5], [9.2195444, 0.8621700, 8]]),
    (cart3d_multi, True, [[5, 53.1301023, 5], [9.2195444, 49.3987053, 8]]),
    ])
def test__cart2pol(pts, deg, expected):
    assert np.allclose(coordinate.cart2pol(pts, deg), expected)


def test__cart2sphere_empty():
    with pytest.raises(SystemExit):
        coordinate.cart2sphere(empty)


@pytest.mark.parametrize('pts, deg, expected', [
    (cart3d_single, False, [[7.0710678, 0.9272952, 0.7853981]]),
    (cart3d_single, True, [[7.0710678, 53.1301023, 45]]),
    (cart3d_multi, False, [[7.0710678, 0.9272952, 0.7853981],
                           [12.2065556, 0.8621700, 0.8561033]]),
    (cart3d_multi, True, [[7.0710678, 53.1301023, 45],
                          [12.2065556, 49.3987053, 49.0511101]]),
    ])
def test__cart2sphere(pts, deg, expected):
    assert np.allclose(coordinate.cart2sphere(pts, deg), expected)


def test__pol2cart_empty():
    with pytest.raises(SystemExit):
        coordinate.pol2cart(empty)


@pytest.mark.parametrize('pts, deg, expected', [
    (pol_single_radian, False, [[2.5980762, 1.5]]),
    (pol_single_degree, True, [[2.5980762, 1.5]]),
    (pol_multi_radian, False, [[2.5980762, 1.5], [3, 5.1961524]]),
    (pol_multi_degree, True, [[2.5980762, 1.5], [3, 5.1961524]]),
    (cyl_single_radian, False, [[2.5980762, 1.5, 5]]),
    (cyl_single_degree, True, [[2.5980762, 1.5, 5]]),
    (cyl_multi_radian, False, [[2.5980762, 1.5, 5], [3, 5.1961524, 8]]),
    (cyl_multi_degree, True, [[2.5980762, 1.5, 5], [3, 5.1961524, 8]]),
    ])
def test_pol2cart(pts, deg, expected):
    assert np.allclose(coordinate.pol2cart(pts, deg), expected)


def test__sphere2cart_empty():
    with pytest.raises(SystemExit):
        coordinate.sphere2cart(empty)


@pytest.mark.parametrize('pts, deg, expected', [
    (sphere_single_3d_radian, False, [[0.8885943, 0.5130302, 2.8190778]]),
    (sphere_single_3d_degree, True, [[0.8885943, 0.5130302, 2.8190778]]),
    (sphere_multi_3d_radian, False, [[0.8885943, 0.5130302, 2.8190778],
                                     [2.1213203, 3.6742346, 4.2426406]]),
    (sphere_multi_3d_degree, True, [[0.8885943, 0.5130302, 2.8190778],
                                    [2.1213203, 3.6742346, 4.2426406]]),
    ])
def test__sphere2cart(pts, deg, expected):
    assert np.allclose(coordinate.sphere2cart(pts, deg), expected)
