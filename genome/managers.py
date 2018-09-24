# -*- coding: utf-8 -*-
from django.db import models


class GeneQuerySet(models.QuerySet):

    def fast(self):
        return self.select_related('chromosome').prefetch_related('synonyms').all()


class TranscriptQuerySet(models.QuerySet):

    def fast(self):
        return self.select_related('gene__chromosome').all()


class ExonQuerySet(models.QuerySet):

    def fast(self):
        return self.select_related('transcript').all()
