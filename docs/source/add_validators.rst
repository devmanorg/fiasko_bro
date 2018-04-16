Write you own validators
========================

Let's pretend we only want to check if the folder contains any Python files with a syntax error.
All the code you need to write in order to implement the behavior is these 12 lines:

.. code-block:: python

    from fiasko_bro import validate


    def has_no_syntax_errors(project_folder, *args, **kwargs):
        for parsed_file in project_folder.get_parsed_py_files():
            if not parsed_file.is_syntax_correct:
                return 'syntax_error', parsed_file.name


    validator_groups = {
        'general': [has_no_syntax_errors]
    }
    print(validate('/Users/project', error_validator_groups=validator_groups))

For the rest of the document we will discuss the things in this example.

Validator arguments
^^^^^^^^^^^^^^^^^^^

A validator receives three kinds of arguments:
    - ``ProjectFolder`` objects
    - validation parameters
    - ``whitelists`` and ``blacklists`` dictionaries (`this is going to change soon <https://github.com/devmanorg/fiasko_bro/issues/102>`_).

ProjectFolder
~~~~~~~~~~~~~

``ProjectFolder`` objects contain all the information about the project:
    - Its Git repository. It's stored in ``repo`` attribute, which is either a ``LocalRepository`` object (if the repository is actually present) or ``None``.
    - All of the Python files. They can be accessed through ``get_parsed_py_files`` method. It returns ``ParsedPyFile`` objects which store store path, name, contents and an ast tree for the associated files.

``ProjectFolder`` class also allows the access to non-Python project files.

The only argument that's guaranteed to be ``ProjectFolder`` is ``project_folder``.
If ``original_project_folder`` is not ``None``, it's a ``ProjectFolder`` object too.

To illustrate the usage of ``original_project_folder``, let's consider a validator that naively counts commits to see if any new code was committed:

.. code-block:: python

    def has_more_commits_than_origin(project_folder, original_project_folder=None, *args, **kwargs):
        if not original_project_folder:
            return
        if not project_folder.repo or not original_project_folder.repo:
            return
        if project_folder.repo.count_commits() <= original_project_folder.repo.count_commits():
            return 'no_new_code', None

Notice we made our validator succeed in case there's no ``original_project_folder`` or no repositories are attached to the folders.
We consider it a sensible solution for our case, but you can choose any other behavior.


Validation parameters
~~~~~~~~~~~~~~~~~~~~~

Validation parameters are simply keyword arguments passed to ``validate`` method. Let's parameterize our syntax validator so
that it could tolerate some number of files with a syntax error:

.. code-block:: python

    from fiasko_bro import validate


    def has_almost_no_syntax_errors(project_folder, max_syntax_error_files_amount, *args, **kwargs):
        syntax_error_files_amount = 0
        for parsed_file in project_folder.get_parsed_py_files():
            if not parsed_file.is_syntax_correct:
                syntax_error_files_amount += 1
        if syntax_error_files_amount > max_syntax_error_files_amount:
            return 'too_many_syntax_errors', syntax_error_files_amount


    validator_groups = {
        'general': []
    }
    print(validate('/Users/project', max_syntax_error_files_amount=2, error_validator_groups=validator_groups))

Whitelists and blacklists
~~~~~~~~~~~~~~~~~~~~~~~~~

    The docs are postponed since the mechanism is `going to be changed <https://github.com/devmanorg/fiasko_bro/issues/102>`_ soon.

Validator return values
^^^^^^^^^^^^^^^^^^^^^^^

A validator is expected to return either ``None`` (if the validation was successful) or a tuple.

The tuple has to consist of an error slug (which is used as an error identifier) and some info that will clarify the error.
In the examples above we either return a file name with a syntax error or the number of syntax errors if it's more relevant.
In case there's no helpful information to return, just return ``error_slug, None``.

Conditionally execute a validator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want the validator to be executed only for certain types of repositories, add ``tokenized_validator`` to it::

    from fiasko_bro import tokenized_validator

    @tokenized_validator(token='min_max_challenge')
    def has_min_max_functions(solution_repo, *args, **kwargs):
        for parsed_file in project_folder.get_parsed_py_files():
            names = get_all_names_from_tree(parsed_file.ast_tree)
            if 'min' in names and 'max' in names:
                return
        return 'builtins', 'no min or max is used'

then add the validator to the appropriate group

    code_validator.error_validator_groups['general'].append(has_min_max_functions)

and when calling ``validate`` for certain folder, pass the token:

    code_validator.validate(project_folder, validator_token='min_max_challenge')

The validator won't be executed for any folder without ``validator_token='min_max_challenge'``.

Adding your validators to the default ones
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A quick example
~~~~~~~~~~~~~~~

Consider the example:

.. code-block:: python

    from fiasko_bro import validate, defaults


    def my_fancy_validator(project_folder, *args, **kwargs):
        pass


    validator_groups = defaults.ERROR_VALIDATOR_GROUPS.copy()
    validator_groups['general'] += (my_fancy_validator,)
    print(
        validate(
            '/Users/project',
            error_validator_groups=validator_groups,
            warning_validators_groups=defaults.WARNING_VALIDATOR_GROUPS
        )
    )

As you can see, we simply copy the default validators structure, modify it to suit our needs and pass to the ``validate`` method.

The minor issue is that since we pass our own error validators, the default warning validators have to be restored by hand.
We did so by passing them as an argument too.

The intricacies
~~~~~~~~~~~~~~~

The are two kinds of validators: error validators and warning validators.
The difference between them is that warning validators don't halt the validation process, while the error validators do.
The error validators are expected to be grouped according to their purpose, like so::

    ERROR_VALIDATOR_GROUPS = OrderedDict(
        [
            (
                'commits',
                [validators.has_more_commits_than_origin],
            ),
            (
                'readme',
                [validators.has_readme_file],
            ),
            ...
            (
                'general',
                [
                    validators.is_pep8_fine,
                    ...
                ],
            ),
        ]
    )

Here, for example, you have the group ``general`` that consists of a list of validators.

In each group, every single validator is executed.
If one of the validators in the group fails, the ``validate`` method executes the rest of the group and then
returns the error list without proceeding to the next group.
If all the validators in the error group succeed, the warning validators for this group are executed.
Here's the structure of the warnings validators::

    WARNING_VALIDATOR_GROUPS = {
        'commits': [
            validators.has_no_commit_messages_from_blacklist,
        ],
        'syntax': [
            validators.has_indents_of_spaces,
            validators.has_no_variables_that_shadow_default_names,
        ]
    }

The ``commits`` warning validator group is executed only if the ``commits`` error validator group passes successfully.

Warning validators are not executed if none of the error validators are failed.
They just add more error messages in case the validation fails.
