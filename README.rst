=============================
Django Genome
=============================

.. image:: https://badge.fury.io/py/django-genome.svg
    :target: https://badge.fury.io/py/django-genome

.. image:: https://travis-ci.org/genomics-geek/django-genome.svg?branch=master
    :target: https://travis-ci.org/genomics-geek/django-genome

.. image:: https://codecov.io/gh/genomics-geek/django-genome/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/genomics-geek/django-genome

Django app for syncing and storing human genome reference data

Documentation
-------------

The full documentation is at https://django-genome.readthedocs.io.

Quickstart
----------

Install Django Genome::

    pip install django-genome

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'genome.apps.GenomeConfig',
        ...
    )

Add Django Genome's URL patterns:

.. code-block:: python

    from genome import urls as genome_urls


    urlpatterns = [
        ...
        url(r'^', include(genome_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
