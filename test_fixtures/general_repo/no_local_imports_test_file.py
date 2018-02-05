# This file for tests/test_general_validators/test_has_no_local_imports.py


def func_for_test_local_imports():
    from datetime import datetime as dt
    return dt.now()
