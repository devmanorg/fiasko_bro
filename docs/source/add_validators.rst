Write you own validators
========================

Let's pretend we only want to check if the folder contains any Python files with a syntax error.
All the code you need to write in order to implement the behavior is these 12 lines:

.. code-block:: python

    from fiasko_bro import validate


    def syntax_error(project_folder, *args, **kwargs):
        for parsed_file in project_folder.get_parsed_py_files():
            if not parsed_file.is_syntax_correct:
                return parsed_file.name


    validator_groups = {
        'general': [syntax_error]
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

    def no_more_commits_than_origin(project_folder, original_project_folder=None, *args, **kwargs):
        if not original_project_folder:
            return
        if not project_folder.repo or not original_project_folder.repo:
            return
        if project_folder.repo.count_commits() <= original_project_folder.repo.count_commits():
            return ''

Notice we made our validator succeed in case there's no ``original_project_folder`` or no repositories are attached to the folders.
We consider it a sensible solution for our case, but you can choose any other behavior.


Validation parameters
~~~~~~~~~~~~~~~~~~~~~

Validation parameters are simply keyword arguments passed to ``validate`` method. Let's parameterize our syntax validator so
that it could tolerate some number of files with a syntax error:

.. code-block:: python

    from fiasko_bro import validate


    def too_many_syntax_errors(project_folder, max_syntax_error_files_amount, *args, **kwargs):
        syntax_error_files_amount = 0
        for parsed_file in project_folder.get_parsed_py_files():
            if not parsed_file.is_syntax_correct:
                syntax_error_files_amount += 1
        if syntax_error_files_amount > max_syntax_error_files_amount:
            return str(syntax_error_files_amount)


    validator_groups = {
        'general': [too_many_syntax_errors]
    }
    print(validate('/Users/project', max_syntax_error_files_amount=2, error_validator_groups=validator_groups))

Ignored paths
~~~~~~~~~~~~~~~~~~~

Suppose we want to ignore some of the files and directories while we validating for syntax errors.
This is how it can be done:

.. code-block:: python

    from fiasko_bro import validate


    def syntax_error(project_folder, syntax_files_to_ignore, *args, **kwargs):
        for parsed_file in project_folder.get_parsed_py_files(whitelist=syntax_files_to_ignore):
            if not parsed_file.is_syntax_correct:
                return parsed_file.name


    validator_groups = {
        'general': [syntax_error]
    }
    ignore_list = ['trash.py', 'garbage.py']
    print(validate('/Users/project', syntax_files_to_ignore=ignore_list, error_validator_groups=validator_groups))

Now, if ``trash.py`` is a part of a file's path, the file is not going to be returned by ``get_parsed_py_files`` method.

Validator return values
^^^^^^^^^^^^^^^^^^^^^^^

A validator returns ``None`` if everything's fine.

In case of a problem, a validator is expected to return an error message string that helps to fix the problem. For example,
if a file has a syntax error, we return the name of the file. In case of PEP8 violations, we return their number.
If you absolutely sure you don't want any error message, return an empty string.

Conditional validator execution
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want the validator to be executed only for certain types of repositories, you can use ``tokenized_validators`` module.
Inside this module you can find three main decorators:

    ``@tokenized_validators.run_if_any(tokens)``

decorated validator will be run if repo is marked by any of the tokens

    ``@tokenized_validators.run_if_all(tokens)``

in this case validator will be run only if repo is marked by all of the tokens

decorator's parameter ``tokens`` can be any kind of iterable i.e. ``['django', 'sqlalchemy']``

You can also use decorator with single token as a string

    ``@tokenized_validators.run_if(token):``

Example:
::

    from fiasko_bro import tokenized_validators

    @tokenized_validators.run_if('min_max_challenge')
    def no_min_max_functions(project_folder, *args, **kwargs):
        for parsed_file in project_folder.get_parsed_py_files():
            names = get_all_names_from_tree(parsed_file.ast_tree)
            if 'min' in names and 'max' in names:
                return
        return 'this repo has to contain a call to min or max function'

then add the validator to the appropriate group

    code_validator.error_validator_groups['general'].append(has_min_max_functions)

and when calling ``validate`` for certain repo, mark repo with the token:

    code_validator.validate(solution_repo=solution_repo, validator_token='min_max_challenge')

If you wish to mark repo with multiple tokens use an iterable and keyword argument ``validator_tokens``:

    code_validator.validate(solution_repo=solution_repo, validator_tokens={'min_max_challenge', 'django'})

If you need even more customization you can use ``@tokenized_validators.run_if_tokens_satisfy_condition(tokens, condition):``

where ``condition`` your own defined function with two arguments ``tokens``, ``repo_tokens`` and boolean return type.

Example:
::

    from fiasko_bro import tokenized_validators

    def my_condition(tokens, repo_tokens):
        return len(tokens) > len(repo_tokens)

    @tokenized_validators.run_if_tokens_satisfy_condition(['sql', 'js'], my_condition)
    def no_min_max_functions(project_folder, *args, **kwargs):
        for parsed_file in project_folder.get_parsed_py_files():
            names = get_all_names_from_tree(parsed_file.ast_tree)
            if 'min' in names and 'max' in names:
                return
        return 'this repo has to contain a call to min or max function'

In this particular case validator will be run only if repo is marked with the ammount of tokens greater than 2.

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
                [validators.no_more_commits_than_origin],
            ),
            (
                'syntax',
                [validators.syntax_error],
            ),
            ...
            (
                'general',
                [
                    validators.too_many_pep8_violations,
                    ...
                ],
            ),
        ]
    )

Here, for example, you have the group ``general`` that consists of a list of validators. We used ``OrderedDict``
because the order in which the validator groups run matters.

In each group, every single validator is executed.
If one of the validators in the group fails, the ``validate`` method executes the rest of the group and then
returns the error list without proceeding to the next group.
If all the validators in the error group succeed, the warning validators for this group are executed.
Here's the structure of the warnings validators::

    WARNING_VALIDATOR_GROUPS = {
        'commits': [
            validators.commit_message_from_blacklist,
        ],
        'syntax': [
            validators.indent_not_multiple_of_tab_size,
            validators.variables_that_shadow_default_names,
        ]
    }

The ``commits`` warning validator group is executed only if the ``commits`` error validator group passes successfully.

Warning validators are not executed if none of the error validators are failed.
They just add more error messages in case the validation fails.

Adding pre-validation checks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pre-validator checks have the same structure as ``error_validator_groups`` and their usage is the same too:

.. code-block:: python

    from fiasko_bro import validate


    def my_pre_validation_check(project_path, *args, **kwargs):
        pass


    pre_validation_checks = {
        'general': [my_pre_validation_check]
    }
    print(validate('/Users/project', pre_validation_checks=pre_validation_checks))

Note that the pre-valdation check receives ``project_path`` (a string), not ``project_folder`` (a ``ProjectFolder`` object)
because the the whole point of the check is to ensure it's OK to parse the files into ASTs.
