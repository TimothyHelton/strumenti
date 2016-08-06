#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Operating System Module

Functions for performing tasks related to the operating system.

.. moduleauthor:: Timothy Helton <timothy.j.helton@gmail.com>
"""

import datetime as dt
import gzip
import os
import shutil
import numpy as np
import wrapt
import strumenti.notify as notify


def get_header(path, header_row=0):
    """Extract header from the requested file.

    .. note: To select the first row of the file enter header_row=0.

    :param str path: path to file
    :param int header_row: row of file that contains the header information
    :returns: header names for each column
    :rtype: tuple
    """
    header_row = int(header_row)
    head = load_file(path, all_lines=False, first_n_lines=header_row + 1)
    return head[header_row].split()


def flatten(matrix):
    """Flatten a matrix (list of lists) into a single list.

    :param list matrix: a list of lists to be flattened
    :returns: all values of matrix in a single list
    :rtype: list
    """
    matrix = [list(x) if isinstance(x, tuple) else
              [x] if not isinstance(x, list) else x for x in matrix]
    return [x for row in matrix for x in row]


def load_file(path, all_lines=True, first_n_lines=0):
    """Load ascii file into memory.

    .. note:: If argument "all_lines" is True then the entire file will be \
        returned with each line as an item in a list and argument \
        "first_n_lines" will be ignored.

    :param str path: path to file to load
    :param bool all_lines: load file as a list of lines if True or a single \
        string if False (default: True)
    :param int first_n_lines: n number of lines to read starting at the \
        beginning of the file (default: 0)
    :returns: ascii text contained within file
    :rtype: str or list

    **Example**:

        * Return the first line of a file example.txt

    ::

        load_file('example.txt', all_lines=False, first_n_lines=1)
    """
    with open(path, 'r') as f:
        if all_lines:
            return f.readlines()
        elif first_n_lines:
            return [f.readline() for _ in range(0, first_n_lines)]
        else:
            return f.read()


def load_records(path, header_row=None, skip_rows=0, cols=('all',), names=None,
                 formats=('f8', )):
    """Load ascii file into an array with fields and records.

    .. note:: Counting of the file rows begins with zero (first row = 0).

    :param str path: path to file to load
    :param int header_row: row of file that contains the column headers \
        (default: None)
    :param int skip_rows: number of header rows to skip at beginning of file \
        (default: 0)
    :param tuple cols: tuple of columns to be loaded as records \
        (default: 'all' will load all columns)
    :param tuple names: names to be assigned to each column
    :param tuple formats: format to be assigned to each column
    :returns: record array of the contents of the requested file
    :rtype: ndarray
    """
    if cols[0] == 'all':
        cols = range(len(get_header(path, header_row=0)))

    if len(formats) != len(cols):
        notify.warn('Formats redefined to match requested number of columns.')
        formats = (formats[0],) * len(cols)

    if isinstance(header_row, int):
        header = get_header(path, header_row=header_row)
        header = [header[x] for x in cols]
    elif not header_row and names:
        header = names
    else:
        header = [str(x) for x in cols]

    return np.loadtxt(path, skiprows=skip_rows, usecols=cols,
                      dtype={'names': header, 'formats': formats})


def preserve_cwd(working_dir):
    """Decorator: Return to the current working directory after function call.

    :param str working_dir: path to working directory
    """
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        original_dir = os.getcwd()
        os.chdir(working_dir)

        try:
            return wrapped(*args, *kwargs)
        finally:
            os.chdir(original_dir)

    return wrapper


def status():
    """Decorator: Provide execution and completion status to terminal."""
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        print('\nExecute: {}'.format(wrapped.__name__))
        start = dt.datetime.now()
        try:
            return wrapped(*args, **kwargs)
        finally:
            finish = dt.datetime.now()
            run_time = finish - start
            print('Completed: {}\t(runtime: {})'.format(wrapped.__name__,
                                                        run_time))

    return wrapper


def unzip_file(path):
    """Decompress read file using gzip.

    :param str path: path to file to be unzipped
    """
    with gzip.open(path, 'rb') as f_in, open(path.rstrip('.gz'), 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

    os.remove(path)


def walk_dir(search):
    """Walk the dir system looking for files that contain the search string.

    .. note:: Search will begin in the current directory.

    :param str search: string of characters to look for in the file names
    :returns: paths to files that matched the search string
    :rtype: list
    """
    output = []
    for root, _, files in os.walk(os.getcwd()):
        for f in files:
            if search in f:
                output.append(os.path.join(root, f))

    return sorted(output)


def zip_file(path):
    """Compress read file using zip.

    :param str path: path to file to be zipped
    """
    with open(path, 'rb') as f_in, \
            gzip.open('{}.gz'.format(path), 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

    os.remove(path)
