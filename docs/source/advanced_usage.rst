Advanced usage
==============

Validation parameters
^^^^^^^^^^^^^^^^^^^^^

The default validation parameters can be found in ``defaults.VALIDATION_PARAMETERS`` dictionary.

The correct way to use the dictionary is to treat it as a read-only object.
If you want to override the default values, just pass the parameters to ``validate`` function directly:

.. code-block:: python

    >>> from fiasko_bro import validate, defaults
    >>> default_directories_to_skip = defaults.VALIDATION_PARAMETERS['directories_to_skip']
    >>> directories_to_skip = default_directories_to_skip.union({'test_fixtures', '.pytest_cache', 'venv'})
    >>> validate('/user/projects/fiasko_bro/', directories_to_skip=directories_to_skip)

The names of the parameters tend to be self-explanatory.
They also have sensible defaults so you didn't have to worry about them until absolutely have to.
The list of validation parameters may change as you add your own validators.

Command line interface
^^^^^^^^^^^^^^^^^^^^^^

When you run

.. code-block:: bash

    $ fiasko

Fiasko starts to validate the current directory, taking its validation parameters from ``fiasko_bro`` section
of the local ``setup.cfg`` if it's present.

The project path and config file location can be modified:

.. code-block:: bash

    $ fiasko -p ~/projects/fiasko_bro --config ~/projects/fiasko_bro/setup.cfg

Right now, the CLI is not as flexible as the Python interface: it lets you use the default validators only
and doesn't let you modify their whitelists and blacklists.

The config file
^^^^^^^^^^^^^^^

The config file allows you to override validation parameters.

Here's a part of Fiasko's own ``setup.cfg`` file::

    [fiasko_bro]
    directories_to_skip=build,dist,test_fixtures,.pytest_cache

(the lack of the whitespace between the directories here `is important <https://github.com/devmanorg/fiasko_bro/issues/107>`_ for now)

Python API doesn't take into consideration the ``setup.cfg`` parameters.
This is a `subject to discussion <https://github.com/devmanorg/fiasko_bro/issues/105>`_.

"Original" repo
^^^^^^^^^^^^^^^

If you want to validate how the project deviated from some "original" repository you can do so
by passing ``original_project_path`` argument:

    >>> from fiasko_bro import validate
    >>> code_validator.validate(project_path='/path/to/folder/', original_project_path='/path/to/different/folder/')
    [('readme_not_changed', '')]

In this example, the original readme was not modified, even though we expected it to.

Pre-validation checks
^^^^^^^^^^^^^^^^^^^^^

Pre-validation checks are here to ensure it's safe to parse the files in the folder into ASTs. For example, they check
file encodings and and the size of the folder under validation so that other validators did not error out.
From the client's perspective, they work exactly like validators.


