#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test django-genome
------------
Tests for `django-genome` filters module.
"""

from django.test import TestCase

from genome import filters, models

from . import fixtures


class TestTranscriptFilter(TestCase):

    def setUp(self):
        fixtures.Transcript()

    def test_filter_gene_symbol(self):
        """Test Transcript gene filter."""
        f = filters.TranscriptFilter(
            {'gene_symbol': 'Symbol'},
            queryset=models.Transcript.objects.all()
        )
        result = list(f.qs)

        assert len(result) == 1
        assert result[0].id == 1
