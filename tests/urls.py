# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include
from django.contrib import admin

from genome.urls import urlpatterns as genome_urls


urlpatterns = [
    url(r'^', include(genome_urls, namespace='genome')),
    url(r'^admin/', admin.site.urls),
]
