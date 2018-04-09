How to use Fiasko
=================


Here's the simplest usage example:

    >>> import fiasko_bro
    >>> fiasko_bro.validate('/path/to/folder/')
    [('camel_case_vars', 'for example, rename the following: WorkBook')]

The ``validate`` method returns list of tuples which consist of an error slug and an error message.

You might also want to compare it against some "original" repo:

    >>> from fiasko_bro import CodeValidator
    >>> code_validator = CodeValidator()
    >>> code_validator.validate(project_folder='/path/to/folder/', original_project_folder='/path/to/different/folder/')
    [('no_new_code', None)]

In this example, no new code was added to the original project folder, so the validation has stopped.
