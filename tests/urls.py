# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from genome.urls import urlpatterns as genome_urls

urlpatterns = [
    url(r'^', include(genome_urls, namespace='genome')),
]
