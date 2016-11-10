#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Test Fixtures

.. moduleauthor:: Timothy Helton <timothy.j.helton@gmail.com>
"""

import logging

import chromalog
import pytest


@pytest.fixture()
def patch_logger(monkeypatch):
    def mock_colorizing_formatter(*args, **kwargs):
        return logging.Formatter()

    def mock_colorizing_stream_handler(*args, **kwargs):
        return logging.StreamHandler()

    monkeypatch.setattr(chromalog.log, 'ColorizingFormatter',
                        mock_colorizing_formatter)
    monkeypatch.setattr(chromalog.log, 'ColorizingStreamHandler',
                        mock_colorizing_stream_handler)
