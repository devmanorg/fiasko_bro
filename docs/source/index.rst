Fiasko Bro
==========

.. image:: https://travis-ci.org/devmanorg/fiasko_bro.svg?branch=master
    :target: https://travis-ci.org/devmanorg/fiasko_bro

.. image:: https://codecov.io/gh/devmanorg/fiasko_bro/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/devmanorg/fiasko_bro

.. image:: https://readthedocs.org/projects/fiasko-bro/badge/?version=latest
    :target: http://fiasko-bro.readthedocs.io/en/latest/?badge=latest

Fiasko is a static analysis tool for Python code that catches common style errors.

It enables you to comprehensively analyze Python projects by looking not only at the Python code,
but also commit messages, file encodings, non-Python files, etc.

Installation
~~~~~~~~~~~~

With pip:

.. code-block:: bash

    pip install fiasko_bro

With Pipenv:

.. code-block:: bash

    pipenv install fiasko_bro

Or just clone the project and install the requirements:

.. code-block:: bash

    $ git clone https://github.com/devmanorg/fiasko_bro.git
    $ cd fiasko_bro
    $ pip install -r requirements.txt

Usage
~~~~~

Fiasko was conceived as a tool used through Python interface. Here's the simplest usage example:

.. code-block:: python

    >>> from fiasko_bro import validate
    >>> validate('/user/projects/fiasko_bro/')
    [('git_history_warning', 'add files via upload'), ('pep8', '33 PEP8 violations'), ('mccabe_failure', 'has_changed_readme'), ('has_star_import', '__init__.py'), ('has_local_import', 'setup.py'), ('bad_titles', 'name, n'), ('bad_titles', 'n, r, l, t, i'), ('file_too_long', 'ast_helpers.py'), ('too_nested', 'code_validator.py:54'), ('indent_not_four_spaces', 'ast_helpers.py:130'), ('title_shadows', '_, slice')]


Then CLI was added:

.. code-block:: bash

    $ fiasko -p ~/projects/fiasko_bro
    git_history_warning                     	add files via upload
    pep8                                    	33 PEP8 violations
    mccabe_failure                          	has_changed_readme
    has_star_import                         	__init__.py
    has_local_import                        	setup.py
    bad_titles                              	name, n
    bad_titles                              	i, r, n, t, l
    file_too_long                           	ast_helpers.py
    too_nested                              	code_validator.py:54
    indent_not_four_spaces                  	ast_helpers.py:130
    title_shadows                           	slice
    ==================================================
    Total 11 violations

In this example, the folder ``~/projects/fiasko_bro`` contains a git repository which allowed Fiasko to find
a questionable commit message "add files via upload".

Tests
~~~~~

``python -m pytest``

Versioning
~~~~~~~~~~

We follow `semantic versioning <https://github.com/dbrock/semver-howto/blob/master/README.md)>`_.

What's next
~~~~~~~~~~~

.. toctree::
   :maxdepth: 2

   advanced_usage
   add_validators
   validators_info
   contributing
   roadmap
   internationalization
