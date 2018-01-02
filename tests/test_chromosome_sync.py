#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test django-genome management command chromosome_sync
------------
Tests for `django-genome` chromosome_sync command.
"""

from django.core.management import call_command

import mock
import pytest

from genomix import utils
from genome import models


@pytest.mark.django_db
@mock.patch.object(utils, 'retrieve_data')
@mock.patch.object(utils, 'retrieve_compressed_data')
def test_chromosome_sync(retrieve_compressed_data_mock, retrieve_data_mock):
    retrieve_data_mock.return_value = ['chr1\t10']
    retrieve_compressed_data_mock.return_value = ['chr1\t10\t10\tcytoband\tstain']

    call_command('chromosome_sync', genome_build='hg18')

    # Make sure it is called with the right URLs
    retrieve_data_mock.assert_called_once_with('http://hgdownload.soe.ucsc.edu/goldenPath/hg18/bigZips/hg18.chrom.sizes')
    retrieve_compressed_data_mock.assert_called_once_with('http://hgdownload.soe.ucsc.edu/goldenPath/hg18/database/cytoBand.txt.gz')

    # Make sure it creates the Genome object
    genome_obj = models.Genome.objects.get(label='hg18')
    assert genome_obj.id == 1

    # Make sure it creates the chromosome object
    chromosome_obj = models.Chromosome.objects.get(label='1')
    assert chromosome_obj.id == 1

    # Make sure it creates the chromosome object
    cytoband_obj = models.CytoBand.objects.get(label='cytoband')
    assert cytoband_obj.id == 1
