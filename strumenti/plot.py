#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Plotting Module

Functions for performing tasks related to matplotlib pyplot library.

.. moduleauthor:: Timothy Helton <timothy.j.helton@gmail.com>
"""

import os.path as osp
import matplotlib.pyplot as plt


def axis_title(title, units=None):
    """Create string for axis title with units italicized.

    :param str title: title of axis
    :param str units: units of axis (default: None)
    :returns: formatted axis title
    :rtype: str
    """
    title = title.title()
    if units:
        return '{} ({})'.format(title, r'$\mathit{{{}}}$'.format(units))
    else:
        return '{}'.format(title)


def save_plot(name=None, **kwargs):
    """Save or display a matplotlib figure.

    :param str name: name of image file (default: None)
    :param kwargs: key word arguments for pyplot.savefig function
    """
    if name:
        name = osp.realpath(name)
        plt.savefig(name, **kwargs)
    else:
        plt.show()
