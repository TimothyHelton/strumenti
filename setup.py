#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from codecs import open
import os.path as osp
from setuptools import setup, find_packages
import strumenti


here = osp.abspath(osp.dirname(__file__))
with open(osp.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
        name='strumenti',
        version='1.0.0',
        description='Common tools univerially applicable to Python packages.',
        author='Timothy Helton',
        author_email='timothy.j.helton@gmail.com',
        classifiers=[
            'Programming Language :: Python :: 3',
            'Natural Language :: English',
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Operating System :: OS Independent',
            'Intended Audience :: Developers',
            ],
        keywords='common tools',
        packages=find_packages(exclude=['docs', 'tests*']),
        install_requires=[
            'matplotlib',
            'numpy',
            'Pint',
            'psycopg2',
            'pytest',
            'termcolor',
            ],
        package_dir={'strumenti': 'strumenti'},
        include_package_data=True,
    )


if __name__ == '__main__':
    pass
