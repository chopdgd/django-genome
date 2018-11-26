#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-genome
------------

Tests for `django-genome` models module.
"""
from django.test import TestCase

from model_mommy import mommy

from . import fixtures


class TestGenome(TestCase):

    def setUp(self):
        self.instance = fixtures.Genome()

    def test_str(self):
        assert str(self.instance) == 'label'


class TestChromosome(TestCase):

    def setUp(self):
        self.instance = fixtures.Chromosome()

    def test_str(self):
        assert str(self.instance) == 'LABEL'


class TestCytoBand(TestCase):

    def setUp(self):
        self.instance = fixtures.CytoBand()

    def test_str(self):
        assert str(self.instance) == 'label'

    def test_locus(self):
        assert self.instance.locus == 'chrLABEL:1-1'


class TestGene(TestCase):

    def setUp(self):
        self.instance = fixtures.Gene()

    def test_str(self):
        assert str(self.instance) == 'SYMBOL'

    def test_build_urls(self):
        assert self.instance.build_urls('url=', None) is None
        assert self.instance.build_urls('url=', '1,2') == ['url=1', 'url=2']

    def test_ensembl_urls(self):
        assert self.instance.ensembl_urls == [
            'http://www.ensembl.org/Homo_sapiens/Gene/Summary?g=not_curated_ensembl',
            'http://www.ensembl.org/Homo_sapiens/Gene/Summary?g=not_curated_ensembl',
        ]

    def test_refseq_urls(self):
        assert self.instance.refseq_urls == [
            'https://www.ncbi.nlm.nih.gov/gene/?term=not_curated_refseq',
            'https://www.ncbi.nlm.nih.gov/gene/?term=not_curated_refseq',
        ]

    def test_omim_urls(self):
        assert self.instance.omim_urls == [
            'https://www.omim.org/entry/not_curated_omim',
            'https://www.omim.org/entry/not_curated_omim',
        ]

    def test_uniprot_urls(self):
        assert self.instance.uniprot_urls is None

    def test_mgi_urls(self):
        assert self.instance.mgi_urls == [
            'http://www.informatics.jax.org/marker/MGI:not_curated_mouse_genome_database',
        ]

    def test_rgd_urls(self):
        assert self.instance.rgd_urls == [
            'http://rgd.mcw.edu/rgdweb/report/gene/main.html?id=not_curated_rat_genome_database',
        ]

    def test_ensembl_gene_id(self):
        assert self.instance.ensembl_gene_id == 'ensembl'

        # NOTE: These case where ensembl is blank
        ensembl_blank = mommy.make('genome.Gene', ensembl="", not_curated_ensembl='nc1,nc3')
        assert ensembl_blank.ensembl_gene_id == 'nc1'


class TestGeneSynonym(TestCase):

    def setUp(self):
        self.instance = fixtures.GeneSynonym()

    def test_str(self):
        assert str(self.instance) == 'label'


class TestTranscript(TestCase):

    def setUp(self):
        self.instance = fixtures.Transcript()

    def test_str(self):
        assert str(self.instance) == 'label'


class TestExon(TestCase):

    def setUp(self):
        self.instance = fixtures.Exon()

    def test_str(self):
        assert str(self.instance) == '1'


class TestGeneList(TestCase):

    def setUp(self):
        self.instance = fixtures.GeneList()

    def test_str(self):
        assert str(self.instance) == 'GeneList'
