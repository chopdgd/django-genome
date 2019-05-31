=====
Usage
=====

To use django-genome in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'genome.apps.GenomeConfig',
        ...
    )

Add django-genome's URL patterns:

.. code-block:: python

    from genome import urls as genome_urls


    urlpatterns = [
        ...
        url(r'^', include(genome_urls)),
        ...
    ]
