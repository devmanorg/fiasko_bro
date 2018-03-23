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

A simple validator is a validator that only takes the repository (more precisely, ``LocalRepositoryInfo`` object) to validate. It returns ``None`` is case of success
and a tuple of an error slug and an error message in case of a problem. Here's an example of existing validator::

    def has_no_syntax_errors(solution_repo, *args, **kwargs):
        for filename, tree in solution_repo.get_ast_trees(with_filenames=True):
            if tree is None:
                return 'syntax_error', 'в %s' % filename

Note the ``*args, **kwargs`` part. The validator actually gets a lot of arguments, but doesn't care about them.

Now you can add validator to one of the existing validator groups or create your own:

    code_validator.error_validator_groups['general'].append(has_no_syntax_errors)

Compare against some "original" repo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want your validator to compare against some other repository, add the ``original_repo`` argument.
::

    def has_more_commits_than_origin(solution_repo, original_repo=None, *args, **kwargs):
        if not original_repo:
            return
        if solution_repo.count_commits() <= original_repo.count_commits():
            return 'no_new_code', None


Notice we made our validator succeed in case there's no ``original_repo``.
We consider it a sensible solution for our case, but you can choose any other behavior.

Parameterize your validator
^^^^^^^^^^^^^^^^^^^^^^^^^^^

To add a parameter to your validator, just add it to the arguments.
::

    def has_no_long_files(solution_repo, max_number_of_lines, *args, **kwargs):
        for file_path, file_content, _ in solution_repo.get_ast_trees(with_filenames=True, with_file_content=True):
            number_of_lines = file_content.count('\n')
            if number_of_lines > max_number_of_lines:
                file_name = url_helpers.get_filename_from_path(file_path)
                return 'file_too_long', file_name

and then don't forget to pass it:

    code_validator.validate(repo, max_number_of_lines=200)

Of course, built-in validators have their own defaults in `_default_settings` property of `CodeValidator` class.

Conditionally execute a validator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
    def has_min_max_functions(solution_repo, *args, **kwargs):
        for tree in solution_repo.get_ast_trees():
            names = get_all_names_from_tree(tree)
            if 'min' in names and 'max' in names:
                return
        return 'builtins', 'no min or max is used'

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
    def has_min_max_functions(solution_repo, *args, **kwargs):
        for tree in solution_repo.get_ast_trees():
            names = get_all_names_from_tree(tree)
            if 'min' in names and 'max' in names:
                return
        return 'builtins', 'no min or max is used'

In this particular case validator will be run only if repo is marked with the ammount of tokens greater than 2.

Blacklist/whitelists for validators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For every rule there's an exception. Exceptions are easy to take into account using blacklists or whitelists.

First, add the blacklist and whitelist to the ``code_validator`` instance::

    code_validator.whitelists['has_no_calls_with_constants'] = ['pow', 'exit']

Then create and add the validator with the same name as the dictionary key::

    def has_no_calls_with_constants(solution_repo, whitelists, *args, **kwargs):
        whitelist = whitelists.get('has_no_calls_with_constants', [])
        for filepath, tree in solution_repo.get_ast_trees(with_filenames=True):
            if 'tests' in filepath:  # tests can have constants in asserts
                continue
            calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)]
            for call in calls:
                if isinstance(ast_helpers.get_closest_definition(call), ast.ClassDef):  # for case of id = db.String(256)
                    continue
                attr_to_get_name = 'id' if hasattr(call.func, 'id') else 'attr'
                function_name = getattr(call.func, attr_to_get_name, None)
                if not function_name or function_name in whitelist:
                    continue
                for arg in call.args:
                    if isinstance(arg, ast.Num):
                        return 'magic_numbers', 'например, %s' % arg.n

Notice in the first line we pull the whitelist from the dictionary and incorporate it in our validation logic.
