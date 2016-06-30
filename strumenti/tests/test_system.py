#! /usr/bin/env python

"""notify.py Unit Tests

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

__version__ = '1.0.1'


@pytest.fixture(scope='session')
def fixture_get_header():
    lines = ['a\tb\tc\td\n', '\n', '1\t2\t3\t4\n', '5\t6\t7\t8\n']

    with open('test.txt', 'w') as f:
        f.write(''.join(lines))

    with open('test_no_header.txt', 'w') as f:
        f.write(''.join(lines[2:]))


@pytest.mark.usefixtures('fixture_get_header')
class TestGetHeader:

    def test__header_row_defaults(self):
        assert system.get_header('test.txt') == ['a', 'b', 'c', 'd']

    def test__header_row_2_row(self):
        assert system.get_header('test.txt', 2) == ['1', '2', '3', '4']

    def test__header_row_2_row_string_input(self):
        assert system.get_header('test.txt', '2') == ['1', '2', '3', '4']


class TestFlatten:

    def test__flatten_empty(self):
        with pytest.raises(TypeError):
            system.flatten()

    def test__flatten_lists_ints_floats(self):
        assert (system.flatten([[1, 2, 3], [4, 5, 6], [7., 8., 9.]]) ==
                [1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test__flatten_lists_string(self):
        assert (system.flatten([['this'], ['is'], ['a'], ['test']]) ==
                ['this', 'is', 'a', 'test'])

    def test__flatten_list_int_string(self):
        assert system.flatten([[1, 2, 3], 4, 'test']) == [1, 2, 3, 4, 'test']

    def test__flatten_lists_empty(self):
        assert system.flatten([[1, 2, 3], [], [7, 8, 9]]) == [1, 2, 3, 7, 8, 9]

    def test__flatten_tuples_floats(self):
        assert (system.flatten([(1, 2, 3), (4, 5, 6), (7, 8, 9)]) ==
                [1, 2, 3, 4, 5, 6, 7, 8, 9])


@pytest.yield_fixture(scope='session')
def fixture_load_file():
    file_name = 'test.txt'
    with open(file_name, 'w') as f:
        f.write('line one\n')
        f.write('line two\n')
        f.write('line three\n')

    yield file_name


class TestOSLoadFile:

    def test__load_file_lines(self, fixture_load_file):
        assert (system.load_file(fixture_load_file) ==
                ['line one\n', 'line two\n', 'line three\n'])

    def test__load_file_str(self, fixture_load_file):
        assert (system.load_file(fixture_load_file, all_lines=False) ==
                'line one\nline two\nline three\n')

    def test__load_file_first_n_lines(self, fixture_load_file):
        assert (system.load_file(fixture_load_file, all_lines=False,
                                 first_n_lines=2) ==
                ['line one\n', 'line two\n'])


@pytest.yield_fixture(scope='session')
def fixture_load_records():
    lines = ['a\tb\tc\td\n', '\n', '1\t2\t3\t4\n', '5\t6\t7\t8\n']

    test_file = 'test.txt'
    with open(test_file, 'w') as f:
        f.write(''.join(lines))

    test_no_header_file = 'test_no_header.txt'
    with open(test_no_header_file, 'w') as f:
        f.write(''.join(lines[2:]))

    yield test_file, test_no_header_file

    try:
        os.remove('test.txt')
        os.remove('test_no_header.txt')
    except FileNotFoundError:
        pass


@pytest.mark.usefixtures('fixture_load_records')
class TestOSLoadRecords:

    def test__load_records_header_all_columns(self):
        output = system.load_records('test.txt', header_row=0, skip_rows=2)

        assert np.all(output['a'] == np.array([1.0, 5.0]))
        assert np.all(output['d'] == np.array([4.0, 8.0]))

    def test__load_records_header_some_columns(self):
        output = system.load_records('test.txt', header_row=0, skip_rows=2,
                                     cols=(0, 3))
        assert np.all(output['a'] == np.array([1.0, 5.0]))
        assert np.all(output['d'] == np.array([4.0, 8.0]))

    def test__load_records_header_all_columns_define_formats(self):
        output = system.load_records('test.txt', header_row=0, skip_rows=2,
                                     formats=('f8', 'i4', 'f8', 'i4'))
        assert np.all(output['a'] == np.array([1.0, 5.0]))
        assert np.all(output['d'] == np.array([4, 8]))

    def test__load_records_no_header(self):
        output = system.load_records('test_no_header.txt', cols=(0, 3))
        assert np.all(output['0'] == np.array([1.0, 5.0]))
        assert np.all(output['3'] == np.array([4.0, 8.0]))


@pytest.yield_fixture()
def fixture_preserve_cwd():
    original_dir = os.getcwd()
    working_dir = osp.join(original_dir, 'junk')
    file_name = 'junk.txt'

    os.makedirs(working_dir, exist_ok=True)

    yield original_dir, working_dir, file_name

    shutil.rmtree(working_dir)


class TestPreserveCWD:

    def test__file_creation(self, fixture_preserve_cwd):

        @system.preserve_cwd(fixture_preserve_cwd[1])
        def test():
            with open(fixture_preserve_cwd[2], 'w') as f:
                f.close()

        test()
        assert osp.isfile(osp.join(fixture_preserve_cwd[1],
                                   fixture_preserve_cwd[2]))
        assert os.getcwd() == fixture_preserve_cwd[0]


class TestStatus:

    def test__normal_operation(self):

        @system.status()
        def print_num():
            print('1, 2, 3')

        f = io.StringIO()
        with redirect_stdout(f):
            print_num()

        assert (f.getvalue().split()[:-3] ==
                ['Execute:', 'print_num', '1,', '2,', '3', 'Completed:',
                 'print_num'])


@pytest.yield_fixture()
def fixture_unzip_file():
    file_name = 'junk.txt'
    with open(file_name, 'w') as f:
        f.write('Test file')
    subprocess.call(['gzip', file_name])

    yield file_name

    os.remove(file_name)


class TestOSUnzipFile:

    def test__normal_operation(self, fixture_unzip_file):
        system.unzip_file('{}.gz'.format(fixture_unzip_file))
        with open(fixture_unzip_file, 'r') as f:
            text = f.read()
        assert 'Test file' == text


@pytest.yield_fixture(scope='session')
def fixture_walk_dir(tmpdir_factory):
    main_dir = str(tmpdir_factory.mktemp('test_walk_dir', numbered=False))
    extra_dir = osp.join(main_dir, 'extra')

    os.makedirs(extra_dir, exist_ok=True)

    @system.preserve_cwd(main_dir)
    def make_files_1():
        with open('main.png', 'w') as f:
            f.write('.png file in main directory.')
        with open('main.jpeg', 'w') as f:
            f.write('.jpeg file in main directory.')

    @system.preserve_cwd(extra_dir)
    def make_files_2():
        with open('extra.png', 'w') as f:
            f.write('.png file in extra directory.')
        with open('extra.inp', 'w') as f:
            f.write('.inp file in extra directory.')

    os.chdir(main_dir)
    make_files_1()
    make_files_2()

    yield main_dir, extra_dir

    shutil.rmtree(main_dir)


class TestOSWalkDir:

    def test__no_files_to_find(self, fixture_walk_dir):
        assert system.walk_dir('.txt') == []

    def test__find_main_dir_only(self, fixture_walk_dir):
        assert system.walk_dir('.jpeg') == [osp.join(fixture_walk_dir[0],
                                                     'main.jpeg')]

    def test__find_extra_dir_only(self, fixture_walk_dir):
        assert (system.walk_dir('.inp') ==
                [osp.join(fixture_walk_dir[0], fixture_walk_dir[1],
                          'extra.inp')])

    def test__find_both_dirs(self, fixture_walk_dir):
        assert (system.walk_dir('.png') ==
                [osp.join(fixture_walk_dir[0], fixture_walk_dir[1],
                          'extra.png'),
                 osp.join(fixture_walk_dir[0], 'main.png')])


@pytest.yield_fixture(scope='function')
def fixture_os_zip_file():
    file_name = 'junk.txt'
    with open(file_name, 'w') as f:
        f.write('Test file')

    yield file_name

    try:
        os.remove(file_name)
    except OSError:
        os.remove('{}.gz'.format(file_name))


class TestOSZipFile:

    def test__normal_operation(self, fixture_os_zip_file):
        file_name = fixture_os_zip_file
        system.zip_file(file_name)
        subprocess.call(['gunzip', '{}.gz'.format(file_name)])
        with open(file_name, 'r') as f:
            text = f.read()
        assert 'Test file' == text
