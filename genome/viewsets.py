# -*- coding: utf-8 -*-
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from . import filters, models, serializers


class ChromosomeViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing Chromosomes."""

    queryset = models.Chromosome.objects.all()
    serializer_class = serializers.ChromosomeSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = filters.ChromosomeFilter
    lookup_field = 'label'


class GenomeViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing Genomes."""

    queryset = models.Genome.objects.all()
    serializer_class = serializers.GenomeSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = filters.GenomeFilter
    search_fields = (
        'label',
        'description',
    )
    lookup_field = 'label'


class GeneViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing Genes."""

    queryset = models.Gene.objects.fast()
    serializer_class = serializers.GeneSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = filters.GeneFilter
    search_fields = (
        'symbol',
        'synonyms__label',
    )
    lookup_field = 'symbol__iexact'


class TranscriptViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing Transcripts."""

    queryset = models.Transcript.objects.fast()
    serializer_class = serializers.TranscriptSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = filters.TranscriptFilter
    lookup_field = 'label'


class ExonViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing Exons."""

    queryset = models.Exon.objects.fast()
    serializer_class = serializers.ExonSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = filters.ExonFilter
