Advanced usage
==============

Write you own validators
------------------------

How validators work
^^^^^^^^^^^^^^^^^^^

Of course, the standard suit of validators can be modified in a way that best suits your needs.

The are two kinds of validators: error validators and warning validators.
The difference between them is that warning validators don't halt the validation process, while the error validators do.
Error validators are grouped according to their purpose, like `in this code <https://github.com/devmanorg/fiasko_bro/blob/master/fiasko_bro/code_validator.py#L133>`_ ::

    error_validator_groups = OrderedDict(
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
        ]
    )

Here, for example, you have the group ``commits`` that consists of the only ``has_more_commits_than_origin`` validator.

In each group, every validator is executed.
If some of the validators in the group fail, the ``validate`` method returns the error list without proceeding to the next group.
If all the validators in the error group succeed, the warning validators for this group are executed.
They are stored in ``warning_validator_groups``::

    warning_validator_groups = {
        'commits': [
            validators.has_no_commit_messages_from_blacklist,
        ],
        'syntax': [
            validators.has_indents_of_spaces,
            validators.has_no_variables_that_shadow_default_names,
        ]
    }

The ``commits`` warning validator group is executed only if the ``commits`` error validator group passes successfully.

Warning validators just add some more errors in case the validation failed.
They are not executed if none of the error validators failed.

Add a simple validator
^^^^^^^^^^^^^^^^^^^^^^

A simple validator is a validator that only takes the argument ``project_folder`` (the name is important) to validate. It returns ``None`` is case of success
and a tuple of an error slug and an error message in case of a problem. Here's an example of existing validator::

    def has_no_syntax_errors(project_folder, *args, **kwargs):
        for parsed_file in project_folder.get_parsed_py_files():
            if not parsed_file.is_syntax_correct:
                return 'syntax_error', parsed_file.name

Note the ``*args, **kwargs`` part. The validator actually gets a lot of arguments, but there's no reason to use them all.

``project_folder`` argument is a ``ProjectFolder`` object, and in this case we use some of its properties to simplify the validation.

The error message has to indicate where the problem occurred so that the user could easily find it.

Now you can add validator to one of the existing validator groups or create your own:

    code_validator.error_validator_groups['general'].append(has_no_syntax_errors)

Compare against some "original" project folder
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want your validator to compare the project against some "original" code, use the ``original_project_folder`` argument.
::

    def has_more_commits_than_origin(project_folder, original_project_folder=None, *args, **kwargs):
        if not original_project_folder:
            return
        if not project_folder.repo or not original_project_folder.repo:
            return
        if project_folder.repo.count_commits() <= original_project_folder.repo.count_commits():
            return 'no_new_code', None

The ``project_folder.repo`` attribute is a ``LocalRepository`` object. It's not ``None`` if the project folder contains
a valid git repository. It allows us to validate such things as commit messages.

Notice we made our validator succeed in case there's no ``original_project_folder`` or no repositories attached to the folders.
We consider it a sensible solution for our case, but you can choose any other behavior.

Parameterize your validator
^^^^^^^^^^^^^^^^^^^^^^^^^^^

To add a parameter to your validator, just add it to the arguments.
::

    def has_no_long_files(project_folder, max_number_of_lines, *args, **kwargs):
        for parsed_file in project_folder.get_parsed_py_files():
            number_of_lines = parsed_file.content.count('\n')
            if number_of_lines > max_number_of_lines:
                return 'file_too_long', parsed_file.name

and then don't forget to pass it when calling the ``validate`` function:

    validate(repo, max_number_of_lines=200)

Built-in validators have their argument values set in ``_default_settings`` property of the ``CodeValidator`` class.
These default values can be overriden by passing a keyword argument to ``validate``.

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

Blacklist/whitelists for validators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For every rule there's an exception. Exceptions are easy to take into account using blacklists or whitelists.

First, add the blacklist and whitelist to the ``code_validator`` instance::

    code_validator.whitelists['has_no_calls_with_constants'] = ['pow', 'exit']

Then create and add the validator with the same name as the dictionary key::

    def has_no_calls_with_constants(solution_repo, whitelists, *args, **kwargs):
        whitelist = whitelists.get('has_no_calls_with_constants', [])
        for parsed_file in project_folder.get_parsed_py_files():
            if 'tests' in parsed_file.path:  # tests can have constants in asserts
                continue
            calls = [n for n in ast.walk(parsed_file.ast_tree) if isinstance(n, ast.Call)]
            for call in calls:
                if isinstance(ast_helpers.get_closest_definition(call), ast.ClassDef):  # for case of id = db.String(256)
                    continue
                attr_to_get_name = 'id' if hasattr(call.func, 'id') else 'attr'
                function_name = getattr(call.func, attr_to_get_name, None)
                if not function_name or function_name in whitelist:
                    continue
                for arg in call.args:
                    if isinstance(arg, ast.Num):
                        return 'magic_numbers', 'for example, %s' % arg.n

Notice in the first line we pull the whitelist from the dictionary and incorporate it in our validation logic.
The whitelist handling isn't perfect now and will be changed in the future, see https://github.com/devmanorg/fiasko_bro/issues/9.
