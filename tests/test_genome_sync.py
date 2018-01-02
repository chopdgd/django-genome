#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test django-genome management command genome_sync
------------
Tests for `django-genome` genome_sync command.
"""

from django.core.management import call_command

import mock
import pytest

from genome.management.commands import genome_sync


@pytest.mark.django_db
@mock.patch.object(genome_sync, 'call_command')
def test_genome_sync(call_command_mock):
    call_command('genome_sync', genome_build='hg18')
    call_command_mock.call_count == 3
