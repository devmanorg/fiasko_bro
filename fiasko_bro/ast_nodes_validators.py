import ast


def is_len_compared_to_zero(node):
    """
        validates if `len(s) >/== 0` pattern
    """

    return _has_call(node) and _has_len_call(node) and _is_compared_with_zero(node)


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
