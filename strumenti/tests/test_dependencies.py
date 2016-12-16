#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""

.. moduleauthor:: Timothy Helton <timothy.j.helton@gmail.com>
"""
import os.path as osp

from pip.operations import freeze


def pip_freeze():
    path = osp.join('..', '..', 'requirements.txt')
    packages = freeze.freeze()
    with open(osp.realpath(path), 'w') as f:
        f.write('\n'.join(list(packages)))
