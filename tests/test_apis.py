#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test django-genome
------------
Tests for `django-genome` API.
"""

from django.contrib.auth import get_user_model

try:
    from django.urls import reverse
except:
    from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from . import fixtures


class TestChromosomeAPI(APITestCase):

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()

        # Create instance for GET, PUT, PATCH, DELETE Methods
        fixtures.Gene()

    def test_post(self):
        """Test POST."""

        response = self.client.post(
            reverse('genome:chromosome-list'),
            {},
            format='json'
        )

        # Make sure to recieve correct HTTP code
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


    def test_get(self):
        """Test GET."""

        response = self.client.get(
            reverse('genome:chromosome-list'),
            format='json'
        )

        # Make sure to recieve correct HTTP code
        assert response.status_code == status.HTTP_200_OK

        # Make sure data is correct
        response_json = response.json()['results']
        assert response_json[0]['id'] == 1
        assert response_json[0]['label'] == 'LABEL'
        assert response_json[0]['length'] == 1
        assert response_json[0]['genome'] == 'label'
        assert response_json[0]['active'] is True

        # Make sure all expected keys are in the response
        observed_keys = list(response_json[0].keys())
        expected_keys = [
            'id',
            'label',
            'genome',
            'length',
            'active',
            'created',
            'modified'
        ]
        difference = set(observed_keys).difference(set(expected_keys))
        assert len(difference) == 0

    def test_put(self):
        """Test PUT."""

        response = self.client.put(
            reverse('genome:chromosome-detail', kwargs={'label': 'label'}),
            {},
            format='json'
        )

        # Make sure to recieve correct HTTP code
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_patch(self):
        """Test PATCH."""

        response = self.client.patch(
            reverse('genome:chromosome-detail', kwargs={'label': 'label'}),
            {},
            format='json'
        )

        # Make sure to recieve correct HTTP code
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_delete(self):
        """Test DELETE."""
        response = self.client.delete(
            reverse('genome:chromosome-detail', kwargs={'label': 'label'}),
            format='json'
        )

        # Make sure to recieve correct HTTP code
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


class TestGenomeAPI(APITestCase):

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()

        # Create instance for GET, PUT, PATCH, DELETE Methods
        fixtures.Gene()

    def test_post(self):
        """Test POST."""

        response = self.client.post(
            reverse('genome:genome-list'),
            {},
            format='json'
        )

        # Make sure to recieve correct HTTP code
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


    def test_get(self):
        """Test GET."""

        response = self.client.get(
            reverse('genome:genome-list'),
            format='json'
        )

        # Make sure to recieve correct HTTP code
        assert response.status_code == status.HTTP_200_OK

        # Make sure data is correct
        response_json = response.json()['results']
        assert response_json[0]['id'] == 1
        assert response_json[0]['label'] == 'label'
        assert response_json[0]['description'] == ''
        assert response_json[0]['description_url'] == 'https://www.google.com'
        assert response_json[0]['active'] is True

        # Make sure all expected keys are in the response
        observed_keys = list(response_json[0].keys())
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

    def test_put(self):
        """Test PUT."""

        response = self.client.put(
            reverse('genome:genome-detail', kwargs={'label': 'label'}),
            {},
            format='json'
        )

        # Make sure to recieve correct HTTP code
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_patch(self):
        """Test PATCH."""

        response = self.client.patch(
            reverse('genome:genome-detail', kwargs={'label': 'label'}),
            {},
            format='json'
        )

        # Make sure to recieve correct HTTP code
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_delete(self):
        """Test DELETE."""
        response = self.client.delete(
            reverse('genome:genome-detail', kwargs={'label': 'label'}),
            format='json'
        )

        # Make sure to recieve correct HTTP code
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


class TestGeneAPI(APITestCase):

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()

        # Create instance for GET, PUT, PATCH, DELETE Methods
        fixtures.Gene()

    def test_post(self):
        """Test POST."""

        response = self.client.post(
            reverse('genome:gene-list'),
            {},
            format='json'
        )

        # Make sure to recieve correct HTTP code
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


    def test_get(self):
        """Test GET."""

        response = self.client.get(
            reverse('genome:gene-list'),
            format='json'
        )

        # Make sure to recieve correct HTTP code
        assert response.status_code == status.HTTP_200_OK

        # Make sure data is correct
        response_json = response.json()['results']
        assert response_json[0]['id'] == 1
        assert response_json[0]['hgnc_id'] == 1
        assert response_json[0]['symbol'] == 'SYMBOL'
        assert response_json[0]['name'] == 'name'
        assert response_json[0]['status'] == 'approved'
        assert response_json[0]['chromosome'] == 'LABEL'
        assert response_json[0]['synonyms'] == ['label']
        assert response_json[0]['active'] is True

        # Make sure all expected keys are in the response
        observed_keys = list(response_json[0].keys())
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
            'modified'
        ]
        difference = set(observed_keys).difference(set(expected_keys))
        assert len(difference) == 0

    def test_put(self):
        """Test PUT."""

        response = self.client.put(
            reverse('genome:gene-detail', kwargs={'symbol__iexact': 'symbol'}),
            {},
            format='json'
        )

        # Make sure to recieve correct HTTP code
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_patch(self):
        """Test PATCH."""

        response = self.client.patch(
            reverse('genome:gene-detail', kwargs={'symbol__iexact': 'symbol'}),
            {},
            format='json'
        )

        # Make sure to recieve correct HTTP code
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_delete(self):
        """Test DELETE."""
        response = self.client.delete(
            reverse('genome:gene-detail', kwargs={'symbol__iexact': 'symbol'}),
            format='json'
        )

        # Make sure to recieve correct HTTP code
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


class TestTranscriptAPI(APITestCase):

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()

        # Create instance for GET, PUT, PATCH, DELETE Methods
        fixtures.Transcript()

    def test_post(self):
        """Test POST."""

        response = self.client.post(
            reverse('genome:transcript-list'),
            {},
            format='json'
        )

        # Make sure to recieve correct HTTP code
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


    def test_get(self):
        """Test GET."""

        response = self.client.get(
            reverse('genome:transcript-list'),
            format='json'
        )

        # Make sure to recieve correct HTTP code
        assert response.status_code == status.HTTP_200_OK

        # Make sure data is correct
        response_json = response.json()['results']
        assert response_json[0]['id'] == 1
        assert response_json[0]['label'] == 'label'
        assert response_json[0]['gene'] == 'SYMBOL'
        assert response_json[0]['strand'] == '+'
        assert response_json[0]['transcription_start'] == 1
        assert response_json[0]['transcription_end'] == 1
        assert response_json[0]['cds_start'] == 1
        assert response_json[0]['cds_end'] == 1
        assert response_json[0]['active'] is True

        # Make sure all expected keys are in the response
        observed_keys = list(response_json[0].keys())
        expected_keys = [
            'id',
            'label',
            'gene',
            'strand',
            'transcription_start',
            'transcription_end',
            'cds_start',
            'cds_end',
            'active',
            'created',
            'modified'
        ]
        difference = set(observed_keys).difference(set(expected_keys))
        assert len(difference) == 0

    def test_put(self):
        """Test PUT."""

        response = self.client.put(
            reverse('genome:transcript-detail', kwargs={'label': 'label'}),
            {},
            format='json'
        )

        # Make sure to recieve correct HTTP code
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_patch(self):
        """Test PATCH."""

        response = self.client.patch(
            reverse('genome:transcript-detail', kwargs={'label': 'label'}),
            {},
            format='json'
        )

        # Make sure to recieve correct HTTP code
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_delete(self):
        """Test DELETE."""
        response = self.client.delete(
            reverse('genome:transcript-detail', kwargs={'label': 'label'}),
            format='json'
        )

        # Make sure to recieve correct HTTP code
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


class TestExonAPI(APITestCase):

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()

        # Create instance for GET, PUT, PATCH, DELETE Methods
        fixtures.Exon()

    def test_post(self):
        """Test POST."""

        response = self.client.post(
            reverse('genome:exon-list'),
            {},
            format='json'
        )

        # Make sure to recieve correct HTTP code
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


    def test_get(self):
        """Test GET."""

        response = self.client.get(
            reverse('genome:exon-list'),
            format='json'
        )

        # Make sure to recieve correct HTTP code
        assert response.status_code == status.HTTP_200_OK

        # Make sure data is correct
        response_json = response.json()['results']
        assert response_json[0]['id'] == 1
        assert response_json[0]['number'] == 1
        assert response_json[0]['transcript'] == 'label'
        assert response_json[0]['start'] == 1
        assert response_json[0]['end'] == 1
        assert response_json[0]['cds'] is True
        assert response_json[0]['active'] is True

        # Make sure all expected keys are in the response
        observed_keys = list(response_json[0].keys())
        expected_keys = [
            'id',
            'number',
            'transcript',
            'start',
            'end',
            'cds',
            'active',
            'created',
            'modified'
        ]
        difference = set(observed_keys).difference(set(expected_keys))
        assert len(difference) == 0

    def test_put(self):
        """Test PUT."""

        response = self.client.put(
            reverse('genome:exon-detail', kwargs={'pk': 1}),
            {},
            format='json'
        )

        # Make sure to recieve correct HTTP code
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_patch(self):
        """Test PATCH."""

        response = self.client.patch(
            reverse('genome:exon-detail', kwargs={'pk': 1}),
            {},
            format='json'
        )

        # Make sure to recieve correct HTTP code
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_delete(self):
        """Test DELETE."""
        response = self.client.delete(
            reverse('genome:exon-detail', kwargs={'pk': 1}),
            format='json'
        )

        # Make sure to recieve correct HTTP code
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
