# -*- coding: utf-8 -*-
from django import forms
from django.db.models import CharField, TextField

import django_filters
from genomix.filters import DisplayChoiceFilter

from . import choices, models


class ChromosomeFilter(django_filters.rest_framework.FilterSet):

    class Meta:
        model = models.Chromosome
        fields = [
            'label',
            'genome'
        ]
        filter_overrides = {
            CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'iexact',
                },
            },
        }


class GenomeFilter(django_filters.rest_framework.FilterSet):

    class Meta:
        model = models.Genome
        fields = [
            'label',
            'description',
        ]
        filter_overrides = {
            CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }


class GeneFilter(django_filters.rest_framework.FilterSet):

    status = DisplayChoiceFilter(choices=choices.HGNC_GENE_STATUS)

    class Meta:
        model = models.Gene
        fields = [
            'symbol',
            'name',
            'hgnc_id',
            'status',
            'active',
            'chromosome',
        ]
        filter_overrides = {
            CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'iexact',
                },
            },
            TextField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            }
        }


class TranscriptFilter(django_filters.rest_framework.FilterSet):

    gene = django_filters.ModelChoiceFilter(
        queryset=models.Gene.objects.all(),
        widget=forms.NumberInput,
    )
    strand = DisplayChoiceFilter(choices=choices.STRAND_TYPES)

    class Meta:
        model = models.Transcript
        fields = [
            'label',
            'active',
            'gene',
            'gene__symbol',
            'strand',
            'transcription_start',
            'transcription_end',
            'cds_start',
            'cds_end',
            'preferred_transcript',
        ]
        filter_overrides = {
            CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'iexact',
                },
            }
        }


class ExonFilter(django_filters.rest_framework.FilterSet):

    transcript = django_filters.ModelChoiceFilter(
        queryset=models.Transcript.objects.all(),
        widget=forms.NumberInput,
    )

    class Meta:
        model = models.Exon
        fields = [
            'number',
            'active',
            'transcript',
            'transcript__label',
            'start',
            'end',
            'cds',
        ]
        filter_overrides = {
            CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'iexact',
                },
            }
        }
