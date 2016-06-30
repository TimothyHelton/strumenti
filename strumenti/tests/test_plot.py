#! /usr/bin/env python

"""plot.py Unit Tests

..moduleauthor:: Timothy Helton <timothy.j.helton@gmail.com>
"""

import os
import os.path as osp
import pytest
import matplotlib.pyplot as plt
from strumenti import plot

__version__ = '1.0.1'


class TestAxisTitle:

    def test__axis_title_empty_arguments(self):
        with pytest.raises(TypeError):
            plot.axis_title()

    def test__axis_title_normal_operation_with_latex_characters(self):
        assert plot.axis_title('test', 'm^2/s_5') == 'Test ($\mathit{m^2/s_5}$)'

    def test__axis_title_no_units(self):
        assert plot.axis_title('test') == 'Test'


file_name = 'test_image.png'


@pytest.fixture(scope='session')
def setup_save_plot(request):
    fig = plt.figure(figsize=(15, 10), facecolor='white')
    fig.suptitle('Test Figure', fontsize='25', fontweight='bold')
    ax = plt.subplot2grid((1, 1), (0, 0), rowspan=1, colspan=1)
    ax.scatter([0, 1, 2, 3], [0, 10, 20, 30], color='black', marker='o')

    def teardown():
        remove_save_plot()
    request.addfinalizer(teardown)


@pytest.fixture()
def remove_save_plot():
    try:
        os.remove(file_name)
    except OSError:
        pass


@pytest.mark.usefixtures('setup_save_plot')
class TestSavePlot:

    def test__save_plot_no_save(self, remove_save_plot):
        plt.ion()
        plot.save_plot()
        assert not osp.exists(file_name)

    def test__save_plot_default(self):
        plot.save_plot(file_name)
        assert osp.exists(file_name)

    def test__save_plot_savefig_argument(self):
        plot.save_plot(file_name, edgecolor='b', transparent=True)
        assert osp.exists(file_name)
