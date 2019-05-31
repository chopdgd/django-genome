# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import include, url
from django.contrib import admin


app_name = 'genome'
urlpatterns = [
    url(r'^', include('genome.urls')),
    url(r'^admin/', admin.site.urls),
]
