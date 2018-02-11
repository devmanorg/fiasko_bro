

def function_with_non_type_exception():
    try:
        var_for_except = 1/0
        return var_for_except
    except:
        pass
    return 'test_func'
