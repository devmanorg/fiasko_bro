import ast


def is_len_compared_to_zero(node):
    """
        validates if `len(s) >/== 0` pattern
    """

    return _has_call(node) and _has_len_call(node) and _is_compared_with_zero(node)


def is_status_code_compared_to_200(node):
    """
        validates blah.status_code == 200
    """
    return (
        _has_eq_compare(node)
        and _has_compare_to_200(node)
        and _has_attr_call(node, 'status_code')
    )


def _has_eq_compare(node):
    return len(node.ops) == 1 and isinstance(node.ops[0], ast.Eq)


def _has_compare_to_200(node):
    return (
        len(node.comparators) == 1
        and isinstance(node.comparators[0], ast.Num)
        and node.comparators[0].n == 200
    )


def _has_attr_call(node, attr_name):
    return (
        isinstance(node.left, ast.Attribute)
        and node.left.attr == attr_name
    )


def _has_call(node):
    return len(node.ops) == 1 and isinstance(node.left, ast.Call)


def _has_len_call(node):
    return (
        hasattr(node.left, 'func')
        and hasattr(node.left.func, 'id')
        and node.left.func.id == 'len'
    )


def _is_compared_with_zero(node):
    return (
        isinstance(node.ops[0], (ast.Gt, ast.Eq))
        and isinstance(node.comparators[0], ast.Num)
        and node.comparators[0].n == 0
    )
