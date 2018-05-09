Fiasko Bro
==========

   When flake8 is not enough.

.. image:: https://travis-ci.org/devmanorg/fiasko_bro.svg?branch=master
   :target: https://travis-ci.org/devmanorg/fiasko_bro
   :alt: Build Status

.. image:: https://codecov.io/gh/devmanorg/fiasko_bro/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/devmanorg/fiasko_bro
   :alt: codecov

.. image:: https://readthedocs.org/projects/fiasko-bro/badge/?version=latest
   :target: http://fiasko-bro.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://api.codeclimate.com/v1/badges/4f26aec50f07294b37e3/maintainability
   :target: https://codeclimate.com/github/devmanorg/fiasko_bro/maintainability
   :alt: Maintainability

.. image:: https://badge.fury.io/py/Fiasko-Bro.svg
   :target: https://badge.fury.io/py/Fiasko-Bro
   :alt: PyPI version

Fiasko is a static analysis tool for Python code that catches common style errors.

.. image:: http://melevir.com/static/fiasko.jpg

Example
~~~~~~~

From command line:

.. code-block:: bash

    $ fiasko -p ~/projects/fiasko_bro
    commit_messages_from_blacklist              add files via upload
    too_many_pep8_violations                    33 PEP8 violations
    too_difficult_by_mccabe                     has_changed_readme
    star_import                                 __init__.py
    local_import                                setup.py
    has_variables_from_blacklist                name, n
    short_variable_name                         i, r, n, t, l
    file_too_long                               ast_helpers.py
    too_nested                                  code_validator.py:54
    indent_not_multiple_of_tab_size             ast_helpers.py:130
    variables_that_shadow_default_names         slice
    ==================================================
    Total 11 violations

See ``fiasko --help`` for more CLI arguments.

From Python code:

.. code-block:: python

    >>> from fiasko_bro import validate
    >>> validate('/user/projects/fiasko_bro/')
    [('commit_messages_from_blacklist', 'add files via upload'), ('too_many_pep8_violations', '33 PEP8 violations'), ('too_difficult_by_mccabe', 'has_changed_readme'), ('star_import', '__init__.py'), ('local_import', 'setup.py'), ('has_variables_from_blacklist', 'name, n'), ('short_variable_name', 'n, r, l, t, i'), ('file_too_long', 'ast_helpers.py'), ('too_nested', 'code_validator.py:54'), ('indent_not_four_spaces', 'ast_helpers.py:130'), ('variables_that_shadow_default_names', '_, slice')]

The ``validate`` method returns list of tuples which consist of an error slug and an error message.

Fiasko has a flexible Python API which you can read more about `in the docs <https://fiasko-bro.readthedocs.io/en/latest/advanced_usage.html>`_.

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

Docs
~~~~

`fiasko-bro.readthedocs.io <http://fiasko-bro.readthedocs.io/>`_


Contributing
~~~~~~~~~~~~

To contribute, `pick an issue <https://github.com/devmanorg/fiasko_bro/issues>`_ to work on and leave a comment saying
that you've taken the issue. Don't forget to mention when you want to submit the pull request.

You can read more about contribution guidelines in `the docs <http://fiasko-bro.readthedocs.io/en/latest/contributing.html>`_

If your suggestion (or bug report) is new, be sure to `create an issue <https://github.com/devmanorg/fiasko_bro/issues/>`_ first.

Launch tests
~~~~~~~~~~~~

``python -m pytest``


Versioning
~~~~~~~~~~

We follow `semantic versioning <https://github.com/dbrock/semver-howto/blob/master/README.md)>`_.
