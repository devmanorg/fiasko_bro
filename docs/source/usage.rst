How to use Fiasko
=================


Here's the simplest usage example:

    >>> import fiasko_bro
    >>> fiasko_bro.validate_repo('/path/to/repo/')
    [('camel_case_vars', 'переименуй, например, WorkBook.')]

The ``validate`` method returns list of tuples which consist of an error slug and an error message.

You might also want to compare it against some "original" repo:

    >>> from fiasko_bro import CodeValidator
    >>> code_validator = CodeValidator()
    >>> code_validator.validate(solution_repo='/path/to/repo/', original_repo='/path/to/different/repo/')
    [('no_new_code', None)]

In this example, no new code was added to the original repo, so the validation has stopped.
