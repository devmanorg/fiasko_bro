import ast


def has_no_syntax_errors(solution_repo, *args, **kwargs):
    for filename, tree in solution_repo.get_ast_trees(with_filenames=True):
        if tree is None:
            return 'syntax_error', filename


def has_indents_of_spaces(solution_repo, tab_size, *args, **kwargs):
    """
        Иногда при парсинге дерева col_offset считается неправильно,
        так что эта проверка может быть только предупреждением.
    """
    node_types_to_validate = (ast.For, ast.If, ast.FunctionDef, ast.With)
    for _, file_content, tree in solution_repo.get_ast_trees(
        with_filenames=True,
        with_file_content=True
    ):
        lines_offsets = [None]
        for line in file_content.split('\n'):
            lines_offsets.append(len(line) - len(line.lstrip(' ')))
        for node in ast.walk(tree):
            if not hasattr(node, 'parent'):
                continue
            node_line = getattr(node, 'lineno', None)
            parent_line = getattr(node.parent, 'lineno', None)
            if node_line is None or parent_line is None:
                continue
            node_offset = lines_offsets[node_line]
            parent_offset = lines_offsets[parent_line]
            if (
                node_line != parent_line and node_offset > parent_offset and
                node_offset - parent_offset != tab_size and
                isinstance(node.parent, node_types_to_validate)
            ):
                return 'indent_not_four_spaces', _('for example, line number %s') % node.lineno
