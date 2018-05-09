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
    [('commit_messages_from_blacklist', 'add files via upload'), ('too_many_pep8_violations', '33 PEP8 violations'), ('too_difficult_by_mccabe', 'has_changed_readme'), ('star_import', '__init__.py'), ('local_import', 'setup.py'), ('has_variables_from_blacklist', 'name, n'), ('short_variable_name', 'n, r, l, t, i'), ('file_too_long', 'ast_helpers.py'), ('too_nested', 'code_validator.py:54'), ('indent_not_multiple_of_tab_size', 'ast_helpers.py:130'), ('variables_that_shadow_default_names', '_, slice')]


Then CLI was added:

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
   changelog
