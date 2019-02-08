#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-genome
------------

Tests for `django-genome` models module.
"""

from .fixtures import *


@pytest.mark.django_db
def test_Genome(Genome):
    instance = Genome(label='hg19')
    assert str(instance) == 'hg19'


@pytest.mark.django_db
def test_Chromosome(Chromosome):
    instance = Chromosome(label='chr1')
    assert str(instance) == 'CHR1'


@pytest.mark.django_db
def test_CytoBand(CytoBand):
    instance = CytoBand(label='q11.1', start=1, end=99)
    assert str(instance) == 'q11.1'
    assert instance.locus == 'chr1:1-99'


@pytest.mark.django_db
def test_Gene(Gene):
    instance = Gene(
        symbol='symbol',
        ensembl='ensembl',
        not_curated_ensembl='not_curated_ensembl',
        not_curated_refseq='not_curated_refseq,not_curated_refseq2',
        not_curated_ucsc='not_curated_ucsc',
        not_curated_omim='not_curated_omim',
        not_curated_uniprot='not_curated_uniprot',
        not_curated_mouse_genome_database='not_curated_mouse_genome_database',
        not_curated_rat_genome_database='not_curated_rat_genome_database',
    )
    assert str(instance) == 'SYMBOL'
    assert instance.build_urls('url=', '1,2') == ['url=1', 'url=2']
    assert instance.ensembl_urls == [
        'http://www.ensembl.org/Homo_sapiens/Gene/Summary?g=not_curated_ensembl',
    ]
    assert instance.refseq_urls == [
        'https://www.ncbi.nlm.nih.gov/gene/?term=not_curated_refseq',
        'https://www.ncbi.nlm.nih.gov/gene/?term=not_curated_refseq2',
    ]
    assert instance.omim_urls == [
        'https://www.omim.org/entry/not_curated_omim',
    ]
    assert instance.uniprot_urls == [
        'http://www.uniprot.org/uniprot/not_curated_uniprot'
    ]
    assert instance.mgi_urls == [
        'http://www.informatics.jax.org/marker/MGI:not_curated_mouse_genome_database',
    ]
    assert instance.rgd_urls == [
        'http://rgd.mcw.edu/rgdweb/report/gene/main.html?id=not_curated_rat_genome_database',
    ]
    assert instance.ensembl_gene_id == 'ensembl'


@pytest.mark.django_db
def test_GeneSynonym(GeneSynonym):
    instance = GeneSynonym(label='Synonym')
    assert str(instance) == 'Synonym'


@pytest.mark.django_db
def test_Transcript(Transcript):
    instance = Transcript(label='Transcript')
    assert str(instance) == 'Transcript'


@pytest.mark.django_db
def test_Exon(Exon):
    instance = Exon(number='1')
    assert str(instance) == '1'


@pytest.mark.django_db
def test_GeneList(GeneList):
    instance = GeneList(label='GeneList')
    assert str(instance) == 'GeneList'
