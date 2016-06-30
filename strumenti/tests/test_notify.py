#! /usr/bin/env python

"""notify.py Unit Tests

..moduleauthor:: Timothy Helton <timothy.j.helton@gmail.com>
"""

import pytest
from strumenti import notify


__version__ = '1.0.1'


class TestAstrixLine:

    def test__float(self):
        assert notify.astrix_line(5.8) == '*****\n'

    def test__int(self):
        assert notify.astrix_line(10) == '**********\n'

    def test__str(self):
        assert notify.astrix_line('10') == '**********\n'

    def test__defaults(self):
        assert notify.astrix_line() == '*' * 80 + '\n'


class TestNotifyCenter:

    def test__center_empty(self):
        with pytest.raises(TypeError):
            notify.center()

    def test__center_one_word(self):
        assert notify.center('one', width=7) == '\n= one ='

    def test__center_two_word(self):
        assert notify.center('one two', width=11) == '\n= one two ='


class TestNotifyHeader:

    def test__header_empty(self):
        with pytest.raises(TypeError):
            notify.header()

    def test__header_notify_module(self):
        assert notify.header('test') == '*' * 80 + '\n' * 3 + 'test\n'


class TestNotifyFooter:

    def test__footer_empty(self):
        with pytest.raises(TypeError):
            notify.footer()

    def test__footer_notify_module(self):
        assert notify.footer('test') == '\n' * 2 + 'test\n' + '*' * 80 + '\n'


class TestNotifySectionBreak:

    def test__section_break_defaults(self):
        assert notify.section_break() == '\n' * 2

    def test__section_break_string(self):
        assert notify.section_break('10') == '\n' * 10

    def test__section_break_float(self):
        assert notify.section_break(10.0) == '\n' * 10

    def test__section_break_int(self):
        assert notify.section_break(10) == '\n' * 10


class TestNotifyStatus:

    def test__status_empty(self):
        with pytest.raises(TypeError):
            notify.status()

    def test__status_one_word(self):
        assert notify.status('one', width=7).strip() == '- One -'

    def test__status_two_word(self):
        assert notify.status('one two', width=11).strip() == '- One Two -'


class TestNotifyWarn:

    def test__warn_empty(self):
        with pytest.raises(TypeError):
            notify.warn()

    def test__warn_one_word(self):
        assert notify.warn('one').strip() == ('!' * 21 +
                                              ' \x1b[5m\x1b[31mONE\x1b[0m ' +
                                              '!' * 21)

    def test__warn_two_word(self):
        actual = notify.warn('one two').strip()
        assert actual == '!' * 19 + ' \x1b[5m\x1b[31mONE TWO\x1b[0m ' + '!' * 19
