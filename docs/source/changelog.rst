Release History
---------------

dev
+++

**Python API Changes**

This is what the Fiasko architecture looked like in ``0.0.1.1``:

.. image:: https://user-images.githubusercontent.com/13587415/39800603-098a280e-5371-11e8-97f8-cef27373ee86.png

Here's how it looks now:

.. image:: https://user-images.githubusercontent.com/13587415/39800607-0b2cdec2-5371-11e8-9ccc-b0d649b8d268.png

- Validation parameters became actual parameters of ``validate`` method
  instead of being class attributes.
- The difference between validation parameters and whitelists/blacklists is erased:
  from now on, both work the same way.
- The project folder does not need to be a git repository in order to be validated correctly
  because ``LocalRepository`` is now decoupled from ``ast_tree``.
- Validator names became the validator error slugs. That means that validator and error slugs now have
  one-to-one relationship.
- Instead of a tuple ``(error_slug, error_message)``, validators have to
  return only the error message string.
- The list of all error slugs can be obtained by calling ``get_error_slugs``.
  It was impossible before.

**Features**

- Added pre validation checks. They ensure it's OK to parse the AST tree of the Python files.
- Added CLI interface.
- Added more complex conditions to conditional validator execution.

**Improvements**

- Added ``Pipfile`` and separated the requirements into deploy and development.
- Added tests on multiple Python versions with ``tox``.
- Cleaned up ``setup.py``.
- Moved helpers to a separate ``utils`` folder.
- Made all validators (and pre validation checks) respect ``directories_to_skip`` setting.

**Misc**

- Fixed numerous bugs.
- Increased test coverage.
- Added new validators.

**Dependencies**

- Updated ``GitPython`` from 2.1.8 to 2.1.9.


0.0.1.1 (2018-02-14)
+++++++++++++++++++

First alpha release.
