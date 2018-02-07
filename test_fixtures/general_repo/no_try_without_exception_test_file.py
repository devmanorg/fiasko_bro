# This file for tests/test_general_validators/test_has_no_try_without_exception.py


def function_with_broad_exception():
    try:
        var_for_except = 1/0
        return var_for_except
    except Exception:
        pass
    return 'test_func'
