#! /usr/bin/env python

"""plot.py Unit Tests

..moduleauthor:: Timothy Helton <timothy.j.helton@gmail.com>
"""

import os
import os.path as osp
import pytest
import matplotlib.pyplot as plt
from strumenti import plot


def test__axis_title_empty_arguments():
    with pytest.raises(TypeError):
        plot.axis_title()


@pytest.mark.parametrize('title, units, expected', [
    ('test', 'm^2/s_5', 'Test ($\mathit{m^2/s_5}$)'),
    ('test', None, 'Test'),
    ])
def test__axis_title(title, units, expected):
    assert plot.axis_title(title, units) == expected


@pytest.fixture()
def plot_setup(request):
    file_name = 'test_image.png'

    fig = plt.figure(figsize=(15, 10), facecolor='white')
    fig.suptitle('Test Figure', fontsize='25', fontweight='bold')
    ax = plt.subplot2grid((1, 1), (0, 0), rowspan=1, colspan=1)
    ax.scatter([0, 1, 2, 3], [0, 10, 20, 30], color='black', marker='o')

    def teardown():
        try:
            os.remove(file_name)
        except OSError:
            pass
    request.addfinalizer(teardown)

    return file_name


def test__save_plot_no_save(plot_setup):
    plt.ion()
    plot.save_plot()
    assert not osp.exists(plot_setup)


def test__save_plot_default(plot_setup):
    plot.save_plot(plot_setup)
    assert osp.exists(plot_setup)


def test__save_plot_savefig_argument(plot_setup):
    plot.save_plot(plot_setup, edgecolor='b', transparent=True)
    assert osp.exists(plot_setup)
