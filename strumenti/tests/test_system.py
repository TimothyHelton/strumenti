#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""system.py Unit Tests

..moduleauthor:: Timothy Helton <timothy.j.helton@gmail.com>
"""

from contextlib import redirect_stdout
import io
import os
import os.path as osp
import pytest
import shutil
import subprocess
import numpy as np
from strumenti import system


lines = ['a\tb\tc\td\n', '\n', '1\t2\t3\t4\n', '5\t6\t7\t8\n']


@pytest.fixture(scope='session')
def fixture_get_header():
    with open('test.txt', 'w') as f:
        f.write(''.join(lines))

    with open('test_no_header.txt', 'w') as f:
        f.write(''.join(lines[2:]))


@pytest.mark.usefixtures('fixture_get_header')
@pytest.mark.parametrize('name, skip, expected', [
    ('test.txt', 0, ['a', 'b', 'c', 'd']),
    ('test.txt', 2, ['1', '2', '3', '4']),
    ('test.txt', '2', ['1', '2', '3', '4']),
    ])
def test__get_header(name, skip, expected):
    assert system.get_header(name, skip) == expected


def test__flatten_empty():
    with pytest.raises(TypeError):
        system.flatten()


@pytest.mark.parametrize('matrix, expected', [
    ([[1, 2, 3], [4, 5, 6], [7., 8., 9.]], [1, 2, 3, 4, 5, 6, 7, 8, 9]),
    ([['this'], ['is'], ['a'], ['test']], ['this', 'is', 'a', 'test']),
    ([[1, 2, 3], 4, 'test'], [1, 2, 3, 4, 'test']),
    ([[1, 2, 3], [], [7, 8, 9]], [1, 2, 3, 7, 8, 9]),
    ([(1, 2, 3), (4, 5, 6), (7, 8, 9)], [1, 2, 3, 4, 5, 6, 7, 8, 9]),
    ])
def test__flatten(matrix, expected):
    assert system.flatten(matrix) == expected


@pytest.fixture(scope='session')
def load_lines_setup():
    file_name = 'test.txt'
    with open(file_name, 'w') as f:
        f.write('line one\n')
        f.write('line two\n')
        f.write('line three\n')
    return file_name


@pytest.mark.usefixtures('load_lines_setup')
@pytest.mark.parametrize('path, all_lines, first_n_lines, expected', [
    ('test.txt', True, 0, ['line one\n', 'line two\n', 'line three\n']),
    ('test.txt', False, 0, 'line one\nline two\nline three\n'),
    ('test.txt', False, 2, ['line one\n', 'line two\n']),
])
def test__load_file(path, all_lines, first_n_lines, expected):
    actual = system.load_file(path, all_lines, first_n_lines)
    assert actual == expected


@pytest.fixture()
def load_record_setup():
    with open('test.txt', 'w') as f:
        f.write(''.join(lines))

    with open('test_no_header.txt', 'w') as f:
        f.write(''.join(lines[2:]))


@pytest.mark.usefixtures('load_record_setup')
@pytest.mark.parametrize(('path, header, skip, cols, names, formats,'
                          'a_key, a_expect, d_key, d_expect'), [
    ('test.txt', 0, 2, ('all',), None, ('f8', ),
     'a', np.array([1.0, 5.0]), 'd', np.array([4.0, 8.0])),
    ('test.txt', 0, 2, (0, 3), None, ('f8', ),
     'a', np.array([1.0, 5.0]), 'd', np.array([4.0, 8.0])),
    ('test.txt', 0, 2, ('all',), None, ('f8', 'i4', 'f8', 'i4'),
     'a', np.array([1.0, 5.0]), 'd', np.array([4, 8])),
    ('test_no_header.txt', None, 0, (0, 3), None, ('f8', ),
     '0', np.array([1.0, 5.0]), '3', np.array([4.0, 8.0])),
    ('test_no_header.txt', None, 0, ('all', ), ('one', 'two', 'three', 'four'),
     ('f8', ), 'one', np.array([1.0, 5.0]), 'four', np.array([4.0, 8.0])),
])
def test__load_records(path, header, skip, cols, names, formats,
                       a_key, a_expect, d_key, d_expect):
    output = system.load_records(path, header, skip, cols, names, formats)
    assert np.all(output[a_key] == a_expect)
    assert np.all(output[d_key] == d_expect)


@pytest.fixture()
def preserve_cwd_setup(request):
    original_dir = os.getcwd()
    working_dir = osp.join(original_dir, 'junk')
    file_name = 'junk.txt'

    os.makedirs(working_dir, exist_ok=True)

    def teardown():
        shutil.rmtree(working_dir)
    request.addfinalizer(teardown)
    return {'original_dir': original_dir, 'working_dir': working_dir,
            'file_name': file_name}


def test__preserve_cwd(preserve_cwd_setup):

    @system.preserve_cwd(preserve_cwd_setup['working_dir'])
    def test():
        with open(preserve_cwd_setup['file_name'], 'w') as f:
            f.close()

    test()
    assert osp.isfile(osp.join(preserve_cwd_setup['working_dir'],
                               preserve_cwd_setup['file_name']))
    assert os.getcwd() == preserve_cwd_setup['original_dir']


def test__status():

    @system.status()
    def print_num():
        print('1, 2, 3')

    f = io.StringIO()
    with redirect_stdout(f):
        print_num()

    assert (f.getvalue().split()[:-3] ==
            ['Execute:', 'print_num', '1,', '2,', '3', 'Completed:',
             'print_num'])


@pytest.fixture(scope='function')
def unzip_setup(request):
    file_name = 'junk.txt'
    with open(file_name, 'w') as f:
        f.write('Test file')
    subprocess.call(['gzip', file_name])

    def teardown():
        os.remove(file_name)
    request.addfinalizer(teardown)
    return file_name


def test__unzip(unzip_setup):
    system.unzip_file('{}.gz'.format(unzip_setup))
    with open(unzip_setup, 'r') as f:
        text = f.read()
    assert 'Test file' == text


class TestOSWalkDir:

    @pytest.fixture(autouse=True)
    def setup(self, request, tmpdir):
        tmpdir.chdir()

        self.main_dir = osp.join(os.getcwd(), 'test_walk_dir')
        self.extra_dir = osp.join(self.main_dir, 'extra')

        os.makedirs(self.extra_dir, exist_ok=True)

        @system.preserve_cwd(self.main_dir)
        def make_files_1():
            with open('main.png', 'w') as f:
                f.write('.png file in main directory.')
            with open('main.jpeg', 'w') as f:
                f.write('.jpeg file in main directory.')

        @system.preserve_cwd(self.extra_dir)
        def make_files_2():
            with open('extra.png', 'w') as f:
                f.write('.png file in extra directory.')
            with open('extra.inp', 'w') as f:
                f.write('.inp file in extra directory.')

        os.chdir(self.main_dir)
        make_files_1()
        make_files_2()

        def teardown():
            tmpdir.chdir()
            shutil.rmtree(self.main_dir)
        request.addfinalizer(teardown)

    def test__no_files_to_find(self):
        assert system.walk_dir('.txt') == []

    def test__find_main_dir_only(self):
        assert system.walk_dir('.jpeg') == [osp.join(self.main_dir,
                                                     'main.jpeg')]

    def test__find_extra_dir_only(self):
        assert (system.walk_dir('.inp') ==
                [osp.join(self.main_dir, self.extra_dir, 'extra.inp')])

    def test__find_both_dirs(self):
        assert (system.walk_dir('.png') ==
                [osp.join(self.main_dir, self.extra_dir, 'extra.png'),
                 osp.join(self.main_dir, 'main.png')])


@pytest.fixture(scope='function')
def zip_setup(request):
    file_name = 'junk.txt'
    with open(file_name, 'w') as f:
        f.write('Test file')

    def teardown():
        try:
            os.remove(file_name)
        except FileNotFoundError:
            os.remove('{}.gz'.format(file_name))
    request.addfinalizer(teardown)
    return file_name


def test__zip_file(zip_setup):
    system.zip_file(zip_setup)
    subprocess.call(['gunzip', '{}.gz'.format(zip_setup)])
    with open(zip_setup, 'r') as f:
        text = f.read()
    assert 'Test file' == text
