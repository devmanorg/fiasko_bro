# This file for tests/test_general_validators/test_has_no_local_imports.py


def function_with_local_import():
    from datetime import datetime as dt
    return dt.now()
