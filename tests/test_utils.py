#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test django-genome
------------
Tests for `django-genome` utils module.
"""

import pytest

from genome import utils


@pytest.mark.parametrize('chromosome, expected', [
    ('chr1', '1'),
    ('1', '1'),
    ('1p10.1', '1'),
    ('1q10.1', '1'),
    ('dasfa', None),
])
def test_reformat_chromosome(chromosome, expected):
    assert utils.reformat_chromosome(chromosome) == expected


@pytest.mark.parametrize('chromosome, expected', [
    ('1', 1),
    ('X', 23),
    ('Y', 24),
    ('M', 25),
    ('MT', 25),
])
def test_chromosome_number(chromosome, expected):
    assert utils.chromosome_number(chromosome) == expected
