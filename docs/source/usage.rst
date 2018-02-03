How to use Fiasko
=================


Here's the simplest usage example:

    >>> import fiasko_bro
    >>> fiasko_bro.validate_repo('/path/to/repo/')
    [('camel_case_vars', 'переименуй, например, WorkBook.')]

The ``validate`` method returns list of tuples which consist of an error slug and an error message.

You might also want to compare it against some "original" repo:

    >>> from fiasko_bro import CodeValidator, LocalRepositoryInfo
    >>> code_validator = CodeValidator()
    >>> repo_to_validate = LocalRepositoryInfo(solution_repo='/path/to/repo/')
    >>> original_repo = LocalRepositoryInfo(original_repo='/path/to/different/repo/')
    >>> code_validator.validate(solution_repo=repo_to_validate, original_repo=original_repo)
    [('no_new_code', None)]

In this example, no new code was added to the original repo, so the validation has stopped.
