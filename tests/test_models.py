#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-genome
------------

Tests for `django-genome` models module.
"""

import pytest

from .fixtures import (
    Genome,
    Chromosome,
    CytoBand,
    Gene,
    GeneSynonym,
    Transcript,
    Exon,
)


@pytest.mark.django_db
class TestGenome(object):

    def test_str(self, Genome):
        assert str(Genome) == 'label'

    def test_attributes(self, Genome):
        assert Genome.label == 'label'
        assert Genome.description_url == 'https://www.google.com'


@pytest.mark.django_db
class TestChromosome(object):

    def test_str(self, Chromosome):
        assert str(Chromosome) == 'LABEL'

    def test_attributes(self, Chromosome):
        assert Chromosome.label == 'LABEL'
        assert Chromosome.genome.id == 1
        assert Chromosome.length == 1
        assert Chromosome.active is True


@pytest.mark.django_db
class TestCytoBand(object):

    def test_str(self, CytoBand):
        assert str(CytoBand) == 'label'

    def test_attributes(self, CytoBand):
        assert CytoBand.label == 'label'
        assert CytoBand.chromosome.id == 1
        assert CytoBand.start == 1
        assert CytoBand.end == 1
        assert CytoBand.stain == 'stain'
        assert CytoBand.active is True

    def test_locus(self, CytoBand):
        assert CytoBand.locus == 'chrLABEL:1-1'


@pytest.mark.django_db
class TestGene(object):

    def test_str(self, Gene):
        assert str(Gene) == 'SYMBOL'

    def test_attributes(self, Gene):
        assert Gene.symbol == 'SYMBOL'
        assert Gene.name == 'name'
        assert Gene.hgnc_id == 1
        assert Gene.status == 1
        assert Gene.get_status_display() == 'approved'
        assert Gene.active is True
        assert Gene.chromosome.id == 1
        assert Gene.previous_name == 'previous_name'
        assert Gene.synonyms.all()[0].id == 1
        assert Gene.locus_type == 'locus_type'
        assert Gene.locus_group == 'locus_group'
        assert Gene.ensembl == 'ensembl'
        assert Gene.refseq == 'refseq'
        assert Gene.not_curated_ensembl == 'not_curated_ensembl,not_curated_ensembl'
        assert Gene.not_curated_refseq == 'not_curated_refseq,not_curated_refseq'
        assert Gene.not_curated_ucsc == 'not_curated_ucsc,not_curated_ucsc'
        assert Gene.not_curated_omim == 'not_curated_omim,not_curated_omim'
        assert Gene.not_curated_uniprot == ''
        assert Gene.not_curated_mouse_genome_database == 'not_curated_mouse_genome_database'
        assert Gene.not_curated_rat_genome_database == 'not_curated_rat_genome_database'
        assert Gene.active is True

    def test_build_urls(self, Gene):
        assert Gene.build_urls('url=', None) is None
        assert Gene.build_urls('url=', '1,2') == ['url=1', 'url=2']

    def test_ensembl_urls(self, Gene):
        assert Gene.ensembl_urls == [
            'http://www.ensembl.org/Homo_sapiens/Gene/Summary?g=not_curated_ensembl',
            'http://www.ensembl.org/Homo_sapiens/Gene/Summary?g=not_curated_ensembl',
        ]

    def test_refseq_urls(self, Gene):
        assert Gene.refseq_urls == [
            'https://www.ncbi.nlm.nih.gov/gene/?term=not_curated_refseq',
            'https://www.ncbi.nlm.nih.gov/gene/?term=not_curated_refseq',
        ]

    def test_omim_urls(self, Gene):
        assert Gene.omim_urls == [
            'https://www.omim.org/entry/not_curated_omim',
            'https://www.omim.org/entry/not_curated_omim',
        ]

    def test_uniprot_urls(self, Gene):
        assert Gene.uniprot_urls is None

    def test_mgi_urls(self, Gene):
        assert Gene.mgi_urls == [
            'http://www.informatics.jax.org/marker/MGI:not_curated_mouse_genome_database',
        ]

    def test_rgd_urls(self, Gene):
        assert Gene.rgd_urls == [
            'http://rgd.mcw.edu/rgdweb/report/gene/main.html?id=not_curated_rat_genome_database',
        ]


@pytest.mark.django_db
class TestGeneSynonym(object):

    def test_str(self, GeneSynonym):
        assert str(GeneSynonym) == 'label'

    def test_attributes(self, GeneSynonym):
        assert GeneSynonym.label == 'label'
        assert GeneSynonym.active is True


@pytest.mark.django_db
class TestTranscript(object):

    def test_str(self, Transcript):
        assert str(Transcript) == 'label'

    def test_attributes(self, Transcript):
        assert Transcript.label == 'label'
        assert Transcript.active is True
        assert Transcript.gene.id == 1
        assert Transcript.strand == 1
        assert Transcript.get_strand_display() == '+'
        assert Transcript.transcription_start == 1
        assert Transcript.transcription_end == 1
        assert Transcript.cds_start == 1
        assert Transcript.cds_end == 1


@pytest.mark.django_db
class TestExon(object):

    def test_str(self, Exon):
        assert str(Exon) == '1'

    def test_attributes(self, Exon):
        assert Exon.number == 1
        assert Exon.active is True
        assert Exon.transcript.id == 1
        assert Exon.start == 1
        assert Exon.end == 1
        assert Exon.cds is True
