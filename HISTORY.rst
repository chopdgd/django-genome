.. :changelog:

History
-------

0.1.0 (2017-12-30)
++++++++++++++++++

* First release on PyPI.
* Initial models and REST API
* Syncs data from HGNC and UCSC to build database

0.2.0 (2018-01-05)
++++++++++++++++++

`0.2.0 Changelog <https://github.com/chopdgd/django-genome/compare/v0.1.0...v0.2.0>`_

* Improved REST API Filters
* made Chromosomes and Gene Symbols save as uppercase to maintain consistency


0.2.1 (2018-01-08)
++++++++++++++++++

`0.2.1 Changelog <https://github.com/chopdgd/django-genome/compare/v0.2.0...v0.2.1>`_

* Fixed issues with migrations

0.2.2 (2018-01-12)
++++++++++++++++++

`0.2.2 Changelog <https://github.com/chopdgd/django-genome/compare/v0.2.1...v0.2.2>`_

* Fixed route names for SimpleRouter

0.3.0 (2018-02-09)
++++++++++++++++++

`0.3.0 Changelog <https://github.com/chopdgd/django-genome/compare/v0.2.2...v0.3.0>`_

* Updated requirements to the latest


0.4.0 (2018-03-30)
++++++++++++++++++

`0.4.0 Changelog <https://github.com/chopdgd/django-genome/compare/v0.3.0...v0.4.0>`_

* Added API for chromosomes
* Changed gene_symbol from being unique

0.5.0 (2018-04-04)
++++++++++++++++++

`0.5.0 Changelog <https://github.com/chopdgd/django-genome/compare/v0.4.0...v0.5.0>`_

* Added GraphQL Nodes

0.6.0 (2018-04-07)
++++++++++++++++++

`0.6.0 Changelog <https://github.com/chopdgd/django-genome/compare/v0.5.0...v0.6.0>`_

* Added support for Django 2 and Python 3.6
* Dropped support for Django < 1.11 and Python 2.7, 3.3, 3.4

0.6.1 (2018-04-18)
++++++++++++++++++

`0.6.1 Changelog <https://github.com/chopdgd/django-genome/compare/v0.6.0...v0.6.1>`_

* Updated 3rd party libs

0.6.2 (2018-05-14)
++++++++++++++++++

`0.6.2 Changelog <https://github.com/chopdgd/django-genome/compare/v0.6.1...v0.6.2>`_

* Updated chromosomes sync to ensure lexicographic ordering of chromosomes

0.6.3 (2018-05-16)
++++++++++++++++++

`0.6.3  Changelog <https://github.com/chopdgd/django-genome/compare/v0.6.2...v0.6.3>`_

* Updated sync to be able to skip sync of exons

0.6.4 (2018-05-16)
++++++++++++++++++

`0.6.4 Changelog <https://github.com/chopdgd/django-genome/compare/v0.6.3...v0.6.4>`_

* Updated setup.py to read requirements.txt

0.7.0 (2018-06-01)
++++++++++++++++++

`0.7.0 Changelog <https://github.com/chopdgd/django-genome/compare/v0.6.4...v0.7.0>`_

* Added Gene List model
* Removed support for GraphQL - this is not needed here.  Applications that import this package can set up Nodes/Schema using models

0.7.1 (2018-06-07)
++++++++++++++++++

`0.7.1 Changelog <https://github.com/chopdgd/django-genome/compare/v0.7.0...v0.7.1>`_

* #54 - Updated management methods to allow for updating when retrieving latest changes from RefSeq
* #56 - Updated Gene model to have property ensembl_gene_id - which will check HGNC and Ensembl provided gene Ids

0.7.2 (2018-08-13)
++++++++++++++++++

`0.7.2 Changelog <https://github.com/chopdgd/django-genome/compare/v0.7.1...v0.7.2>`_

* Updated 3rd party requirements. Some requirements had changed so it was causing failures

0.7.3 (2018-09-26)
++++++++++++++++++

`0.7.3 Changelog <https://github.com/chopdgd/django-genome/compare/v0.7.2...v0.7.3>`_

* Updated transcript model to include preferred transcript boolean

0.7.4 (2018-10-29)
++++++++++++++++++

`0.7.4 Changelog <https://github.com/chopdgd/django-genome/compare/v0.7.3...v0.7.4>`_

* Updated 3rd party libs

0.7.6 (2018-11-27)
++++++++++++++++++

`0.7.6 Changelog <https://github.com/chopdgd/django-genome/compare/v0.7.5...v0.7.6>`_

* HGNC changed their headers - so gene sync was broken.  Made reading headers case insensitive

0.7.7 (2019-02-08)
++++++++++++++++++

`0.7.7 Changelog <https://github.com/chopdgd/django-genome/compare/v0.7.6...v0.7.7>`_

* Updated 3rd party libs
* Updated tests to use py.test fixtures correctly

0.7.8 (2019-04-10)
++++++++++++++++++

`0.7.8 Changelog <https://github.com/chopdgd/django-genome/compare/v0.7.7...v0.7.8>`_

* Updated 3rd party libs
* Updated travis to use xenial distribution. Django 2.1 dropped support for SQLite < 3.8.3

0.8.0 (2019-05-31)
++++++++++++++++++

`0.8.0 Changelog <https://github.com/chopdgd/django-genome/compare/v0.7.8...v0.8.0>`_

* Refactored sync to use UCSC MySQL database connection
* Updated sync to incorporate transcript refseq versions
* Updated package to use latest cookiecutter template

0.8.1 (2019-06-14)
++++++++++++++++++

`0.8.1 Changelog <https://github.com/chopdgd/django-genome/compare/v0.8.0...v0.8.1>`_

* Gene entries created from RefSeq where not setting the chromosome attribute
* Added better logging functionality

0.8.2 (2019-07-26)
++++++++++++++++++

`0.8.2 Changelog <https://github.com/chopdgd/django-genome/compare/v0.8.1...v0.8.2>`_

* Updated 3rd party libs

0.9.0 (2019-08-02)
++++++++++++++++++

`0.9.0 Changelog <https://github.com/chopdgd/django-genome/compare/v0.8.2...v0.9.0>`_

* Updated Gene data model and sync to include date approved/modified.

0.9.1 (2019-08-05)
++++++++++++++++++

`0.9.1 Changelog <https://github.com/chopdgd/django-genome/compare/v0.9.0...v0.9.1>`_

* Fixed issue with bundle not being published correctly

0.9.2 (2019-08-09)
++++++++++++++++++

`0.9.2 Changelog <https://github.com/chopdgd/django-genome/compare/v0.9.1...v0.9.2>`_

* Updated 3rd party libs

0.9.3 (2019-09-09)
++++++++++++++++++

`0.9.3 Changelog <https://github.com/chopdgd/django-genome/compare/v0.9.2...v0.9.3>`_

* Updated 3rd party libs

1.0.0 (2019-11-01)
++++++++++++++++++

`1.0.0 Changelog <https://github.com/chopdgd/django-genome/compare/v0.9.3...v1.0.0>`_

* Updated Gene model to make sure it is unique on symbol
* First, production release

1.1.0 (2019-11-26)
++++++++++++++++++

`1.1.0 Changelog <https://github.com/chopdgd/django-genome/compare/v1.0.0...v1.0.``>`_

* Updated dependencies
