# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^', include('genome.urls', namespace='genome')),
    url(r'^admin/', admin.site.urls),
]
