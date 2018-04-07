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


class TestChromosomeURLs(TestCase):
    """Test URL patterns for Genes."""

    def setUp(self):
        self.instance = fixtures.Chromosome()

    def test_list_reverse(self):
        """genome:chromosome-list should reverse to /chromosomes/."""
        self.assertEqual(reverse('genome:chromosome-list'), '/chromosomes/')

    def test_list_resolve(self):
        """/chromosomes/ should resolve to genome:chromosomes-list."""
        self.assertEqual(resolve('/chromosomes/').view_name, 'genome:chromosome-list')


class TestGeneURLs(TestCase):
    """Test URL patterns for Genes."""

    def setUp(self):
        self.instance = fixtures.Gene()

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


# class TestCrossReferenceURLs(TestCase):
#     """Test URL patterns for HPO Term Cross References."""
#
#     def setUp(self):
#         self.instance = fixtures.CrossReference()
#
#     def test_list_reverse(self):
#         """hpo_terms:crossreference-list should reverse to /hpo-xrefs/."""
#         self.assertEqual(reverse('hpo_terms:crossreference-list'), '/hpo-xrefs/')
#
#     def test_list_resolve(self):
#         """/hpo-xrefs/ should resolve to hpo_terms:crossreference-list."""
#         self.assertEqual(resolve('/hpo-xrefs/').view_name, 'hpo_terms:crossreference-list')
#
#     def test_detail_reverse(self):
#         """hpo_terms:crossreference-detail should reverse to /hpo-xrefs/1/."""
#         self.assertEqual(
#             reverse('hpo_terms:crossreference-detail', kwargs={'pk': 1}),
#             '/hpo-xrefs/1/'
#         )
#
#     def test_detail_resolve(self):
#         """/hpo-xrefs/1/ should resolve to hpo_terms:crossreference-detail."""
#         self.assertEqual(resolve('/hpo-xrefs/1/').view_name, 'hpo_terms:crossreference-detail')
#
#
# class TestDiseaseURLs(TestCase):
#     """Test URL patterns for Diseases."""
#
#     def setUp(self):
#         self.instance = fixtures.Disease()
#
#     def test_list_reverse(self):
#         """hpo_terms:disease-list should reverse to /diseases/."""
#         self.assertEqual(reverse('hpo_terms:disease-list'), '/diseases/')
#
#     def test_list_resolve(self):
#         """/diseases/ should resolve to hpo_terms:disease-list."""
#         self.assertEqual(resolve('/diseases/').view_name, 'hpo_terms:disease-list')
#
#     def test_detail_reverse(self):
#         """hpo_terms:disease-detail should reverse to /diseases/1/."""
#         self.assertEqual(
#             reverse('hpo_terms:disease-detail', kwargs={'pk': 1}),
#             '/diseases/1/'
#         )
#
#     def test_detail_resolve(self):
#         """/diseases/1/ should resolve to hpo_terms:disease-detail."""
#         self.assertEqual(resolve('/diseases/1/').view_name, 'hpo_terms:disease-detail')
