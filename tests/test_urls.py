#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test django-genome
------------
Tests for `django-genome` urls module.
"""
from django.urls import resolve, reverse

from test_plus.test import TestCase

from . import fixtures


class TestGenomeURLs(TestCase):
    """Test URL patterns for Genes."""

    def test_list_reverse(self):
        """genome:genome-list should reverse to /genomes/."""
        self.assertEqual(reverse('genome:genome-list'), '/genomes/')

    def test_list_resolve(self):
        """/genomes/ should resolve to genome:genome-list."""
        self.assertEqual(resolve('/genomes/').view_name, 'genome:genome-list')

    def test_detail_reverse(self):
        """genome:genome-detail should reverse to /genomes/hg19/."""
        self.assertEqual(
            reverse('genome:genome-detail', kwargs={'label': 'hg19'}),
            '/genomes/hg19/'
        )

    def test_detail_resolve(self):
        """/genomes/hg19/ should resolve to genome:genome-detail."""
        self.assertEqual(resolve('/genomes/hg19/').view_name, 'genome:genome-detail')


class TestChromosomeURLs(TestCase):
    """Test URL patterns for Chromosomes."""

    def test_list_reverse(self):
        """genome:chromosome-list should reverse to /chromosomes/."""
        self.assertEqual(reverse('genome:chromosome-list'), '/chromosomes/')

    def test_list_resolve(self):
        """/chromosomes/ should resolve to genome:chromosomes-list."""
        self.assertEqual(resolve('/chromosomes/').view_name, 'genome:chromosome-list')

    def test_detail_reverse(self):
        """genome:chromosome-detail should reverse to /chromosomes/chr1/."""
        self.assertEqual(
            reverse('genome:chromosome-detail', kwargs={'label': 'chr1'}),
            '/chromosomes/chr1/'
        )

    def test_detail_resolve(self):
        """/chromsomes/chr1/ should resolve to genome:chromsome-detail."""
        self.assertEqual(resolve('/chromosomes/chr1/').view_name, 'genome:chromosome-detail')


class TestGeneURLs(TestCase):
    """Test URL patterns for Genes."""

    def test_list_reverse(self):
        """genome:gene-list should reverse to /genes/."""
        self.assertEqual(reverse('genome:gene-list'), '/genes/')

    def test_list_resolve(self):
        """/genes/ should resolve to genome:gene-list."""
        self.assertEqual(resolve('/genes/').view_name, 'genome:gene-list')

    def test_detail_reverse(self):
        """genome:gene-detail should reverse to /genes/symbol/."""
        self.assertEqual(
            reverse('genome:gene-detail', kwargs={'symbol__iexact': 'symbol'}),
            '/genes/symbol/'
        )

    def test_detail_resolve(self):
        """/genes/symbol/ should resolve to genome:gene-detail."""
        self.assertEqual(resolve('/genes/symbol/').view_name, 'genome:gene-detail')


class TestTranscriptURLs(TestCase):
    """Test URL patterns for Transcripts."""

    def test_list_reverse(self):
        """genome:transcript-list should reverse to /transcripts/."""
        self.assertEqual(reverse('genome:transcript-list'), '/transcripts/')

    def test_list_resolve(self):
        """/transcripts/ should resolve to genome:transcript-list."""
        self.assertEqual(resolve('/transcripts/').view_name, 'genome:transcript-list')

    def test_detail_reverse(self):
        """genome:transcript-detail should reverse to /transcripts/label/."""
        self.assertEqual(
            reverse('genome:transcript-detail', kwargs={'label': 'label'}),
            '/transcripts/label/'
        )

    def test_detail_resolve(self):
        """/transcripts/label/ should resolve to genome:transcript-detail."""
        self.assertEqual(resolve('/transcripts/label/').view_name, 'genome:transcript-detail')


class TestExonURLs(TestCase):
    """Test URL patterns for Exons."""

    def test_list_reverse(self):
        """genome:exon-list should reverse to /exons/."""
        self.assertEqual(reverse('genome:exon-list'), '/exons/')

    def test_list_resolve(self):
        """/exons/ should resolve to genome:exon-list."""
        self.assertEqual(resolve('/exons/').view_name, 'genome:exon-list')

    def test_detail_reverse(self):
        """genome:exon-detail should reverse to /exons/1/."""
        self.assertEqual(
            reverse('genome:exon-detail', kwargs={'pk': 1}),
            '/exons/1/'
        )

    def test_detail_resolve(self):
        """/exons/label/ should resolve to genome:exon-detail."""
        self.assertEqual(resolve('/exons/1/').view_name, 'genome:exon-detail')
