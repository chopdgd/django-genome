# -*- coding: utf-8 -*-
from django import forms
from django.db.models import Q

import django_filters

from . import models


class GeneFilter(django_filters.rest_framework.FilterSet):

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


class TranscriptFilter(django_filters.rest_framework.FilterSet):

    gene = django_filters.ModelChoiceFilter(
        queryset=models.Gene.objects.all(),
        widget=forms.NumberInput,
    )

    gene_symbol = django_filters.CharFilter(
        name='gene__symbol',
        label='Gene Symbol',
        method='filter_gene_symbol',
    )

    class Meta:
        model = models.Transcript
        fields = [
            'label',
            'active',
            'gene',
            'strand',
            'transcription_start',
            'transcription_end',
            'cds_start',
            'cds_end',
        ]

    def filter_gene_symbol(self, queryset, name, value):
        return queryset.filter(
            Q(gene__symbol__icontains=value) |
            Q(gene__synonyms__label__icontains=value)
        )


class ExonFilter(django_filters.rest_framework.FilterSet):

    transcript = django_filters.ModelChoiceFilter(
        queryset=models.Transcript.objects.all(),
        widget=forms.NumberInput,
    )

    transcript_label = django_filters.CharFilter(
        name='transcript__label',
        label='Transcript Label',
        lookup_expr='iexact',
    )

    class Meta:
        model = models.Exon
        fields = [
            'number',
            'active',
            'transcript',
            'start',
            'end',
            'cds',
        ]
