#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test django-genome management command transcript_sync
------------
Tests for `django-genome` transcript_sync command.
"""

from django.core.management import call_command

import mock
import pytest

from genomix import utils
from genome import models

from .fixtures import Gene


@pytest.mark.django_db
@mock.patch.object(utils, 'retrieve_compressed_data')
def test_transcript_sync(retrieve_compressed_data_mock):
    retrieve_compressed_data_mock.return_value = [
        'na\ttranscript\tna\t+\t1\t2\t3\t4\t2\t1,2\t2,3\tna\tsymbol',
        'na\ttranscript2\tna\t-\t1\t2\t3\t4\t2\t1,2\t2,3\tna\tsymbol'
    ]

    # Create Gene object before calling transcript_sync
    Gene()

    call_command('transcript_sync', genome_build='hg18')

    # Make sure it is called with the right URLs
    retrieve_compressed_data_mock.assert_called_once_with('http://hgdownload.soe.ucsc.edu/goldenPath/hg18/database/refGene.txt.gz')

    # Make sure it creates the Transcript object
    transcript_obj = models.Transcript.objects.get(label='transcript')
    assert transcript_obj.id == 1
    assert transcript_obj.gene.id == 1
    assert transcript_obj.strand == 1
    assert transcript_obj.transcription_start == 1
    assert transcript_obj.transcription_end == 2
    assert transcript_obj.cds_start == 3
    assert transcript_obj.cds_end == 4

    transcript_obj = models.Transcript.objects.get(label='transcript2')
    assert transcript_obj.id == 2
    assert transcript_obj.gene.id == 1
    assert transcript_obj.strand == 2
    assert transcript_obj.transcription_start == 1
    assert transcript_obj.transcription_end == 2
    assert transcript_obj.cds_start == 3
    assert transcript_obj.cds_end == 4

    # Make sure it creates correct Exons numbered correctly for + strand
    exon_plus_obj = models.Exon.objects.filter(transcript__label='transcript')
    assert exon_plus_obj[0].number == 1
    assert exon_plus_obj[0].start == 1
    assert exon_plus_obj[0].end == 2
    assert exon_plus_obj[1].number == 2
    assert exon_plus_obj[1].start == 2
    assert exon_plus_obj[1].end == 3

    # Make sure it creates correct Exons numbered correctly for - strand
    exon_minus_obj = models.Exon.objects.filter(transcript__label='transcript2')
    assert exon_minus_obj[0].number == 2
    assert exon_minus_obj[0].start == 1
    assert exon_minus_obj[0].end == 2
    assert exon_minus_obj[1].number == 1
    assert exon_minus_obj[1].start == 2
    assert exon_minus_obj[1].end == 3
