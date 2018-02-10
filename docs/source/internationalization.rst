Internationalization
====================

The error messages returned by the validators can be translated.
Fiasko Bro currently supports English and Russian languages.

The choice of the language depends on environment variables ``LANGUAGE``, ``LC_ALL``, ``LC_MESSAGES`` and ``LANG``
(in the same order of priority: if ``LANGUAGE`` is set, others ignored).

For example::

    $ python
    >>> from fiasko_bro import validate_repo
    >>> validate_repo('../10_coursera_temp')
    [('camel_case_vars', 'for example, rename the following: WorkBook'), ('file_too_long', 'coursera.py')]
    >>>
    $ export LANGUAGE=ru
    $ python
    >>> from fiasko_bro import validate_repo
    >>> validate_repo('../10_coursera_temp')
    [('camel_case_vars', 'переименуй, например, WorkBook'), ('file_too_long', 'coursera.py')]
    >>>

