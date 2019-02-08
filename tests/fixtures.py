# -*- coding: utf-8 -*-
from model_mommy import mommy
import pytest


@pytest.fixture
def Genome():
    def _func(**kwargs):
        return mommy.make('genome.Genome', **kwargs)
    return _func


@pytest.fixture
def Chromosome():
    def _func(genome=None, **kwargs):
        if not genome:
            genome = mommy.make('genome.Genome', label='hg19')
        return mommy.make('genome.Chromosome', genome=genome, **kwargs)
    return _func


@pytest.fixture
def CytoBand():
    def _func(chromosome=None, **kwargs):
        if not chromosome:
            chromosome = mommy.make('genome.Chromosome', label='1')
        return mommy.make('genome.CytoBand', chromosome=chromosome, **kwargs)
    return _func


@pytest.fixture
def Gene():
    def _func(chromosome=None, synonyms=None, **kwargs):
        if not chromosome:
            chromosome = mommy.make('genome.Chromosome', label='1')
        if not synonyms:
            synonyms = [mommy.make('genome.GeneSynonym', label='synonym')]
        return mommy.make('genome.Gene', synonyms=synonyms, chromosome=chromosome, **kwargs)
    return _func


@pytest.fixture
def GeneSynonym():
    def _func(**kwargs):
        return mommy.make('genome.GeneSynonym', **kwargs)
    return _func


@pytest.fixture
def Transcript():
    def _func(gene=None, **kwargs):
        if not gene:
            gene = mommy.make('genome.Gene', symbol='GENE')
        return mommy.make('genome.Transcript', gene=gene, **kwargs)
    return _func


@pytest.fixture
def Exon():
    def _func(transcript=None, **kwargs):
        if not transcript:
            transcript = mommy.make('genome.Transcript', label='Transcript')
        return mommy.make('genome.Exon', transcript=transcript, **kwargs)
    return _func


@pytest.fixture
def GeneList():
    def _func(genes=None, **kwargs):
        if not genes:
            genes = [mommy.make('genome.Gene', symbol='GENE')]
        return mommy.make('genome.GeneList', genes=genes, **kwargs)
    return _func
