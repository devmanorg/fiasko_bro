Fiasko Bro
==========

.. image:: https://travis-ci.org/devmanorg/fiasko_bro.svg?branch=master
    :target: https://travis-ci.org/devmanorg/fiasko_bro

.. image:: https://codecov.io/gh/devmanorg/fiasko_bro/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/devmanorg/fiasko_bro

.. image:: https://readthedocs.org/projects/fiasko-bro/badge/?version=latest
    :target: http://fiasko-bro.readthedocs.io/en/latest/?badge=latest

Fiasko Bro enables you to automatically review Python code in a git repo.


Installation
============

With pip::

    pip install git+https://github.com/devmanorg/fiasko_bro.git


Or just clone the project and install the requirements::

    $ git clone https://github.com/devmanorg/fiasko_bro.git
    $ cd fiasko_bro
    $ pip install -r requirements.txt


Usage
=====

Here's the simplest usage example::

    >>> import fiasko_bro
    >>> fiasko_bro.validate('/path/to/repo/')
    [('camel_case_vars', 'for example, rename the following: WorkBook'), ('file_too_long', 'source_file.py')]


Launch tests
============

``python -m pytest``



Whats next
==========

.. toctree::
   :maxdepth: 2

   usage
   advanced_usage
   validators_info
   contributing
   roadmap
   internationalization
