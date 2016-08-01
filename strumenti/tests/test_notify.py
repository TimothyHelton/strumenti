#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""notify.py Unit Tests

..moduleauthor:: Timothy Helton <timothy.j.helton@gmail.com>
"""

import pytest
from strumenti import notify


@pytest.mark.parametrize('qty, expected', [
    (5.8, '*****\n'),
    (10, '**********\n'),
    ('10', '**********\n'),
    (80, '*' * 80 + '\n'),
    ])
def test__astrix_line(qty, expected):
    assert notify.astrix_line(qty) == expected


def test__notify_center_empty():
    with pytest.raises(TypeError):
        notify.center()


@pytest.mark.parametrize('stmt, fill, width, expected', [
    ('one', '=', 7, '\n= one ='),
    ('one two', '=', 11, '\n= one two =')
    ])
def test__center(stmt, fill, width, expected):
    assert notify.center(stmt, fill, width) == expected


def test__header_empty():
    with pytest.raises(TypeError):
        notify.header()


@pytest.mark.parametrize('stmt, expected', [
    ('test', '*' * 80 + '\n' * 3 + 'test\n')
    ])
def test_header(stmt, expected):
    assert notify.header(stmt) == expected


def test__footer_empty():
    with pytest.raises(TypeError):
        notify.footer()


@pytest.mark.parametrize('stmt, expected', [
    ('test', '\n' * 2 + 'test\n' + '*' * 80 + '\n')
    ])
def test__footer(stmt, expected):
    assert notify.footer(stmt) == expected


@pytest.mark.parametrize('qty, expected', [
    (2, '\n' * 2),
    ('10', '\n' * 10),
    (10.0, '\n' * 10),
    (10, '\n' * 10),
    ])
def test__section_break(qty, expected):
    assert notify.section_break(qty) == expected


def test__status_empty():
    with pytest.raises(TypeError):
        notify.status()


@pytest.mark.parametrize('stmt, fill, width, expected', [
    ('one', '-', 7, '- One -'),
    ('one two', '-', 11, '- One Two -'),
    ])
def test__notify(stmt, fill, width, expected):
    assert notify.status(stmt, fill, width).strip() == expected


def test__warn_empty():
    with pytest.raises(TypeError):
        notify.warn()


# pytest parametrize does not work with termcolor output
def test__warn_one_word():
    actual = notify.warn('one').strip()
    assert actual == ('!' * 21 + ' \x1b[5m\x1b[31mONE\x1b[0m ' + '!' * 21)


def test__warn_two_word():
    actual = notify.warn('one two').strip()
    assert actual == '!' * 19 + ' \x1b[5m\x1b[31mONE TWO\x1b[0m ' + '!' * 19
