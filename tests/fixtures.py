# -*- coding: utf-8 -*-
from model_mommy import mommy
import pytest


@pytest.fixture
def Genome():

    return mommy.make(
        'genome.Genome',
        id=1,
        label='label',
        description_url='https://www.google.com',
    )


@pytest.fixture
def Chromosome():

    return mommy.make(
        'genome.Chromosome',
        id=1,
        label='label',
        genome=Genome(),
        length=1,
        active=True,
    )


@pytest.fixture
def CytoBand():

    return mommy.make(
        'genome.CytoBand',
        id=1,
        label='label',
        chromosome=Chromosome(),
        start=1,
        end=1,
        stain='stain',
        active=True,
    )


@pytest.fixture
def Gene():

    return mommy.make(
        'genome.Gene',
        id=1,
        symbol='symbol',
        name='name',
        hgnc_id=1,
        status=1,
        active=True,
        chromosome=Chromosome(),
        previous_name='previous_name',
        synonyms=[GeneSynonym()],
        locus_type='locus_type',
        locus_group='locus_group',
        ensembl='ensembl',
        refseq='refseq',
        not_curated_ensembl='not_curated_ensembl,not_curated_ensembl',
        not_curated_refseq='not_curated_refseq,not_curated_refseq',
        not_curated_ucsc='not_curated_ucsc,not_curated_ucsc',
        not_curated_omim='not_curated_omim,not_curated_omim',
        not_curated_uniprot='',
        not_curated_mouse_genome_database='not_curated_mouse_genome_database',
        not_curated_rat_genome_database='not_curated_rat_genome_database',
    )


@pytest.fixture
def GeneSynonym():

    return mommy.make(
        'genome.GeneSynonym',
        id=1,
        label='label',
        active=True,
    )


@pytest.fixture
def Transcript():

    return mommy.make(
        'genome.Transcript',
        id=1,
        label='label',
        active=True,
        gene=Gene(),
        strand=1,
        transcription_start=1,
        transcription_end=1,
        cds_start=1,
        cds_end=1,
        preferred_transcript=True,
    )


@pytest.fixture
def Exon():

    return mommy.make(
        'genome.Exon',
        id=1,
        number=1,
        active=True,
        transcript=Transcript(),
        start=1,
        end=1,
        cds=True,
    )


@pytest.fixture
def GeneList():

    return mommy.make(
        'genome.GeneList',
        id=1,
        label='GeneList',
        description='description',
        version='version',
        active=True,
        genes=[Gene()],
    )
