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

__version__ = '1.0.2'


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


class TestOSLoadFile:

    @pytest.fixture(autouse=True)
    def setup(self, request):
        self.file_name = 'test.txt'
        with open(self.file_name, 'w') as f:
            f.write('line one\n')
            f.write('line two\n')
            f.write('line three\n')

        def teardown():
            os.remove(self.file_name)
        request.addfinalizer(teardown)

    def test__load_file_lines(self):
        assert (system.load_file(self.file_name) ==
                ['line one\n', 'line two\n', 'line three\n'])

    def test__load_file_str(self):
        assert (system.load_file(self.file_name, all_lines=False) ==
                'line one\nline two\nline three\n')

    def test__load_file_first_n_lines(self):
        assert (system.load_file(self.file_name, all_lines=False,
                                 first_n_lines=2) ==
                ['line one\n', 'line two\n'])


class TestOSLoadRecords:

    @pytest.fixture(autouse=True)
    def setup(self, request):
        lines = ['a\tb\tc\td\n', '\n', '1\t2\t3\t4\n', '5\t6\t7\t8\n']

        self.test_file = 'test.txt'
        with open(self.test_file, 'w') as f:
            f.write(''.join(lines))

        self.test_no_header_file = 'test_no_header.txt'
        with open(self.test_no_header_file, 'w') as f:
            f.write(''.join(lines[2:]))

        def teardown():
            try:
                os.remove('test.txt')
                os.remove('test_no_header.txt')
            except FileNotFoundError:
                pass
        request.addfinalizer(teardown)

    def test__load_records_header_all_columns(self):
        output = system.load_records(self.test_file, header_row=0, skip_rows=2)
        assert np.all(output['a'] == np.array([1.0, 5.0]))
        assert np.all(output['d'] == np.array([4.0, 8.0]))

    def test__load_records_header_some_columns(self):
        output = system.load_records(self.test_file, header_row=0, skip_rows=2,
                                     cols=(0, 3))
        assert np.all(output['a'] == np.array([1.0, 5.0]))
        assert np.all(output['d'] == np.array([4.0, 8.0]))

    def test__load_records_header_all_columns_define_formats(self):
        output = system.load_records(self.test_file, header_row=0, skip_rows=2,
                                     formats=('f8', 'i4', 'f8', 'i4'))
        assert np.all(output['a'] == np.array([1.0, 5.0]))
        assert np.all(output['d'] == np.array([4, 8]))

    def test__load_records_no_header(self):
        output = system.load_records(self.test_no_header_file, cols=(0, 3))
        assert np.all(output['0'] == np.array([1.0, 5.0]))
        assert np.all(output['3'] == np.array([4.0, 8.0]))


class TestPreserveCWD:

    @pytest.fixture(autouse=True)
    def setup(self, request):
        self.original_dir = os.getcwd()
        self.working_dir = osp.join(self.original_dir, 'junk')
        self.file_name = 'junk.txt'

        os.makedirs(self.working_dir, exist_ok=True)

        def teardown():
            shutil.rmtree(self.working_dir)
        request.addfinalizer(teardown)

    def test__file_creation(self, ):

        @system.preserve_cwd(self.working_dir)
        def test():
            with open(self.file_name, 'w') as f:
                f.close()

        test()
        assert osp.isfile(osp.join(self.working_dir, self.file_name))
        assert os.getcwd() == self.original_dir


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


class TestOSUnzipFile:

    @pytest.fixture(autouse=True)
    def setup(self, request):
        self.file_name = 'junk.txt'
        with open(self.file_name, 'w') as f:
            f.write('Test file')
        subprocess.call(['gzip', self.file_name])

        def teardown():
            os.remove(self.file_name)
        request.addfinalizer(teardown)

    def test__normal_operation(self):
        system.unzip_file('{}.gz'.format(self.file_name))
        with open(self.file_name, 'r') as f:
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


class TestOSZipFile:

    @pytest.fixture(autouse=True)
    def setup(self, request):
        self.file_name = 'junk.txt'
        with open(self.file_name, 'w') as f:
            f.write('Test file')

        def teardown():
            try:
                os.remove(self.file_name)
            except OSError:
                os.remove('{}.gz'.format(self.file_name))
        request.addfinalizer(teardown)

    def test__normal_operation(self):
        system.zip_file(self.file_name)
        subprocess.call(['gunzip', '{}.gz'.format(self.file_name)])
        with open(self.file_name, 'r') as f:
            text = f.read()
        assert 'Test file' == text
