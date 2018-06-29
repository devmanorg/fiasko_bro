Contributing info
=================

To contribute, `pick an issue <https://github.com/devmanorg/fiasko_bro/issues>`_ to work on and leave a comment saying
that you've taken the issue. Don't forget to mention when you want to submit the pull request.

There are three main ways you can contribute at the moment:

- by adding new validators;
- by writing tests for existing validators;
- by helping us reduce the technical debt.

While writing our code, we simply adhere to `Kenneth Reitz's Code Style™ <http://docs.python-requests.org/en/latest/dev/contributing/#kenneth-reitz-s-code-style>`_.
We firmly believe that function names should start with a verb: ``count_pep8_violations``, ``is_pep8_fine``, ``has_no_syntax_errors``.

When a particular convention is not documented, strive for consistency with the existing code and use your best judgement.

Add new validators
^^^^^^^^^^^^^^^^^^
First, find out which validators to add in `Github Issues <https://github.com/devmanorg/fiasko_bro/issues?q=is%3Aissue+is%3Aopen+label%3Anew_validator>`_.

If you have an idea of your own, make sure to create an issue first.

`Write your validator <http://fiasko-bro.readthedocs.io/en/latest/advanced_usage.html#customize-validators>`_
and put it in ``validators`` folder and an appropriate validator group.

A good name for a validator would be the one that plays along nicely with the error message.
For example, if the error message consists of a file name and a line number,
then the validator name should indicate what is wrong with the line: ``too_nested``, ``fails_john_complexity``.

Make sure you have the tests for your validator.

Write tests for validators
^^^^^^^^^^^^^^^^^^^^^^^^^^

Before writing a test for validator, choose where to put it. The most suitable place would be ``test_<validator group name>_validators`` module
inside ``tests`` folder. Inside the module, create file ``test_<validator name>.py`` and put all of the test cases there.

Every validator group should have its own fixture repository located in ``test_fixtures`` under the name ``<validator group>_repo``. Put the fixture files there.

The name of the fixture files should reflect their contents, not what they are used for.
So the good name for a function would be ``function_with_tabs`` and not ``function_to_test_are_tabs_used_validator``.
This facilitates fixture reuse.

Reduce technical debt
^^^^^^^^^^^^^^^^^^^^^
You are always welcome to `refactor <https://github.com/devmanorg/fiasko_bro/issues?q=is%3Aissue+is%3Aopen+label%3Atech_debt>`_
the existing code, fix and file bugs and improve documentation.
