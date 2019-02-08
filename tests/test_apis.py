#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test django-genome
------------
Tests for `django-genome` API.
"""

try:
    from django.urls import reverse
except:
    from django.core.urlresolvers import reverse

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from .fixtures import *


@pytest.mark.django_db
def setup_client(user=None):
    client = APIClient()

    if user:
        client.force_authenticate(user=user)

    return client


def test_api_permissions():
    client = setup_client()

    response = client.post(reverse('genome:genome-list'), {})
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.post(reverse('genome:chromosome-list'), {})
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.post(reverse('genome:gene-list'), {})
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.post(reverse('genome:transcript-list'), {})
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.post(reverse('genome:exon-list'), {})
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.put(reverse('genome:genome-detail', kwargs={'label': 'label'}), {})
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.put(reverse('genome:chromosome-detail', kwargs={'label': 'label'}), {})
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.put(reverse('genome:gene-detail', kwargs={'symbol__iexact': 'label'}), {})
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.put(reverse('genome:transcript-detail', kwargs={'label': 'label'}), {})
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.put(reverse('genome:exon-detail', kwargs={'pk': 1}), {})
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.patch(reverse('genome:genome-detail', kwargs={'label': 'label'}), {})
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.patch(reverse('genome:chromosome-detail', kwargs={'label': 'label'}), {})
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.patch(reverse('genome:gene-detail', kwargs={'symbol__iexact': 'label'}), {})
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.patch(reverse('genome:transcript-detail', kwargs={'label': 'label'}), {})
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.patch(reverse('genome:exon-detail', kwargs={'pk': 1}), {})
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.delete(reverse('genome:genome-detail', kwargs={'label': 'label'}))
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.delete(reverse('genome:chromosome-detail', kwargs={'label': 'label'}))
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.delete(reverse('genome:gene-detail', kwargs={'symbol__iexact': 'symbol'}))
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.delete(reverse('genome:transcript-detail', kwargs={'label': 'label'}))
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.delete(reverse('genome:exon-detail', kwargs={'pk': 1}))
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
def test_get_genomes_list(Genome):
    Genome(label='hg19')
    client = setup_client()
    response = client.get(reverse('genome:genome-list'), format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json().get('results', [])) == 1

    observed_keys = list(response.json()['results'][0].keys())
    expected_keys = [
        'id',
        'label',
        'description',
        'description_url',
        'active',
        'created',
        'modified'
    ]
    difference = set(observed_keys).difference(set(expected_keys))
    assert len(difference) == 0


@pytest.mark.django_db
def test_get_genomes_detail(Genome):
    Genome(label='hg19')
    client = setup_client()
    response = client.get(reverse('genome:genome-detail', kwargs={'label': 'hg19'}), format='json')
    assert response.status_code == status.HTTP_200_OK

    observed_keys = list(response.json().keys())
    expected_keys = [
        'id',
        'label',
        'description',
        'description_url',
        'active',
        'created',
        'modified'
    ]
    difference = set(observed_keys).difference(set(expected_keys))
    assert len(difference) == 0


@pytest.mark.django_db
def test_get_chromosomes_list(Chromosome):
    Chromosome(label='chr1')
    client = setup_client()
    response = client.get(reverse('genome:chromosome-list'), format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json().get('results', [])) == 1

    observed_keys = list(response.json()['results'][0].keys())
    expected_keys = [
        'id',
        'genome',
        'label',
        'length',
        'active',
    ]
    difference = set(observed_keys).difference(set(expected_keys))
    assert len(difference) == 0


@pytest.mark.django_db
def test_get_chromosomes_detail(Chromosome):
    Chromosome(label='chr1')
    client = setup_client()
    response = client.get(reverse('genome:chromosome-detail', kwargs={'label': 'CHR1'}), format='json')
    assert response.status_code == status.HTTP_200_OK

    observed_keys = list(response.json().keys())
    expected_keys = [
        'id',
        'genome',
        'label',
        'length',
        'active',
    ]
    difference = set(observed_keys).difference(set(expected_keys))
    assert len(difference) == 0


@pytest.mark.django_db
def test_get_genes_list(Gene):
    Gene(symbol='gene')
    client = setup_client()
    response = client.get(reverse('genome:gene-list'), format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json().get('results', [])) == 1

    observed_keys = list(response.json()['results'][0].keys())
    expected_keys = [
        'id',
        'hgnc_id',
        'symbol',
        'name',
        'status',
        'chromosome',
        'synonyms',
        'active',
        'created',
        'modified',
    ]
    difference = set(observed_keys).difference(set(expected_keys))
    assert len(difference) == 0


@pytest.mark.django_db
def test_get_genes_detail(Gene):
    Gene(symbol='gene')
    client = setup_client()
    response = client.get(reverse('genome:gene-detail', kwargs={'symbol__iexact': 'gene'}), format='json')
    assert response.status_code == status.HTTP_200_OK

    observed_keys = list(response.json().keys())
    expected_keys = [
        'id',
        'hgnc_id',
        'symbol',
        'name',
        'status',
        'chromosome',
        'synonyms',
        'active',
        'created',
        'modified',
    ]
    difference = set(observed_keys).difference(set(expected_keys))
    assert len(difference) == 0


@pytest.mark.django_db
def test_get_transcripts_list(Transcript):
    Transcript(label='transcript')
    client = setup_client()
    response = client.get(reverse('genome:transcript-list'), format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json().get('results', [])) == 1

    observed_keys = list(response.json()['results'][0].keys())
    expected_keys = [
        'id',
        'label',
        'gene',
        'strand',
        'chromosome',
        'transcription_start',
        'transcription_end',
        'cds_start',
        'cds_end',
        'active',
        'created',
        'modified',
    ]
    difference = set(observed_keys).difference(set(expected_keys))
    assert len(difference) == 0


@pytest.mark.django_db
def test_get_transcripts_detail(Transcript):
    Transcript(label='transcript')
    client = setup_client()
    response = client.get(reverse('genome:transcript-detail', kwargs={'label': 'transcript'}), format='json')
    assert response.status_code == status.HTTP_200_OK

    observed_keys = list(response.json().keys())
    expected_keys = [
        'id',
        'label',
        'gene',
        'strand',
        'chromosome',
        'transcription_start',
        'transcription_end',
        'cds_start',
        'cds_end',
        'active',
        'created',
        'modified',
    ]
    difference = set(observed_keys).difference(set(expected_keys))
    assert len(difference) == 0


@pytest.mark.django_db
def test_get_exons_list(Exon):
    Exon(pk=100)
    client = setup_client()
    response = client.get(reverse('genome:exon-list'), format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json().get('results', [])) == 1

    observed_keys = list(response.json()['results'][0].keys())
    expected_keys = [
        'id',
        'number',
        'transcript',
        'start',
        'end',
        'cds',
        'active',
        'created',
        'modified',
    ]
    difference = set(observed_keys).difference(set(expected_keys))
    assert len(difference) == 0


@pytest.mark.django_db
def test_get_exons_detail(Exon):
    Exon(pk=100)
    client = setup_client()
    response = client.get(reverse('genome:exon-detail', kwargs={'pk': 100}), format='json')
    assert response.status_code == status.HTTP_200_OK

    observed_keys = list(response.json().keys())
    expected_keys = [
        'id',
        'number',
        'transcript',
        'start',
        'end',
        'cds',
        'active',
        'created',
        'modified',
    ]
    difference = set(observed_keys).difference(set(expected_keys))
    assert len(difference) == 0
