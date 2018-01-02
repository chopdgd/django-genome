#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test django-genome management command genes_sync
------------
Tests for `django-genome` genes_sync command.
"""

from django.core.management import call_command

import mock
import pytest

from genomix import utils
from genome import models


@pytest.mark.django_db
@mock.patch.object(utils, 'retrieve_data')
@mock.patch.object(utils, 'retrieve_compressed_data')
def test_gene_sync(retrieve_compressed_data_mock, retrieve_data_mock):
    retrieve_data_mock.return_value = [
        'Approved Symbol\tApproved Name\tHGNC ID\tStatus\tChromosome\tPrevious Name\tLocus Type\tLocus Group\tEnsembl Gene ID\t'
        'RefSeq IDs\tEnsembl ID(supplied by Ensembl)\tRefSeq(supplied by NCBI)\tUCSC ID(supplied by UCSC)\tOMIM ID(supplied by OMIM)\t'
        'UniProt ID(supplied by UniProt)\tMouse Genome Database ID(supplied by MGI)\tRat Genome Database ID(supplied by RGD)\t'
        'Synonyms\tPrevious Symbols',
        'symbol\tname\tHGNC:1\tapproved\tlabel\tprevious_name\ttype\tgroup\tensembl\t'
        'refseq\tnc_ensembl\tnc_refeq\tnc_ucsc\tnc_omim\t'
        'nc_uniprot\tnc_mgi\tnc_rgd\tSynonym\tPrevious_Symbol'
    ]
    retrieve_compressed_data_mock.return_value = [
        'na\tna\tna\tna\tsymbol2\trefseq\tna\tname'
    ]

    call_command('gene_sync', genome_build='hg18')

    # Make sure it is called with the right URLs
    retrieve_data_mock.assert_called_once_with('http://tinyurl.com/mqot6vl')
    retrieve_compressed_data_mock.assert_called_once_with('http://hgdownload.cse.ucsc.edu/goldenPath/hg18/database/kgXref.txt.gz')

    # Make sure it creates the HGNC gene object
    gene_obj = models.Gene.objects.get(symbol='SYMBOL')
    assert gene_obj.id == 1
    assert gene_obj.name == 'name'
    assert gene_obj.hgnc_id == 1
    assert gene_obj.status == 1
    assert gene_obj.previous_name == 'previous_name'
    assert gene_obj.locus_type == 'type'
    assert gene_obj.locus_group == 'group'
    assert gene_obj.ensembl == 'ensembl'
    assert gene_obj.refseq == 'refseq'
    assert gene_obj.not_curated_ensembl == 'nc_ensembl'
    assert gene_obj.not_curated_refseq == 'nc_refeq'
    assert gene_obj.not_curated_ucsc == 'nc_ucsc'
    assert gene_obj.not_curated_omim == 'nc_omim'
    assert gene_obj.not_curated_uniprot == 'nc_uniprot'
    assert gene_obj.not_curated_mouse_genome_database == 'nc_mgi'
    assert gene_obj.not_curated_rat_genome_database == 'nc_rgd'
    assert len(gene_obj.synonyms.all()) == 2

    # Make sure it creates the kgXref gene object
    gene2_obj = models.Gene.objects.get(symbol='SYMBOL2')
    assert gene2_obj.id == 2
    assert gene2_obj.symbol == 'SYMBOL2'
    assert gene2_obj.name == 'name'
    assert gene2_obj.status == 4
