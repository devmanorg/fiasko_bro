Internationalization
====================

The error messages returned by the validators can be translated.
Fiasko Bro currently supports English and Russian languages.

The choice of the language depends on environment variables ``LANGUAGE``, ``LC_ALL``, ``LC_MESSAGES`` and ``LANG``
(in the same order of priority: if ``LANGUAGE`` is set, others ignored).

For example::

    $ python
    >>> from fiasko_bro import validate
    >>> validate('../10_coursera_temp')
    [('camel_case_vars', 'for example, rename the following: WorkBook'), ('file_too_long', 'coursera.py')]
    >>>
    $ export LANGUAGE=ru
    $ python
    >>> from fiasko_bro import validate
    >>> validate('../10_coursera_temp')
    [('camel_case_vars', 'переименуй, например, WorkBook'), ('file_too_long', 'coursera.py')]
    >>>


Add translations
^^^^^^^^^^^^^^^^

The whole process consists of three parts. First, you have to find the strings that need translations and put them into
the ``.pot`` file. Second, you need to translate the strings and put the translations into ``.po`` file. Finally, you
have to compile the ``.po`` files to ``.mo`` files and test your translations. Here are more detailed instructions on
each of the steps:

0. Mark the strings that need the translation by importing ``gettext`` function::

    from i18n import _

    # ...

    _('a string to translate')


1. To generate the ``.pot`` file, user Babel::

    pybabel extract fiasko_bro -o fiasko_bro/locale/fiasko_bro.pot

2. To translate the extracted strings, use a tool like `Poedit <https://poedit.net/>`_. Open the ``.pot`` file with it
    and add the translations. When you're done, place the file in the following directory and with the following name:
    ``fiasko_bro/locale/<locale name>/LC_MESSAGES/fiasko_bro.po``.
3. Compile the file::

    pybabel compile -i fiasko_bro/locale/<locale name>/LC_MESSAGES/fiasko_bro.po -o fiasko_bro/locale/<locale name>/LC_MESSAGES/fiasko_bro.mo


Now change the locale make sure Fiasko produces the right output::

    $ python
    >>> from fiasko_bro import validate
    >>> validate('../10_coursera_temp')
    [('camel_case_vars', 'for example, rename the following: WorkBook'), ('file_too_long', 'coursera.py')]
    >>>
    $ export LANGUAGE=<locale name>
    $ python
    >>> from fiasko_bro import validate
    >>> validate('../10_coursera_temp')
    [('camel_case_vars', 'переименуй, например, WorkBook'), ('file_too_long', 'coursera.py')]
    >>>

Finally, add the ``.po`` file to git and you're done.
