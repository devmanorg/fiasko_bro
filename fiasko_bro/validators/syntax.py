import ast

from ..utils import ast_helpers, file_helpers, url_helpers


def has_no_syntax_errors(solution_repo, *args, **kwargs):
    for filepath, tree in solution_repo.get_ast_trees(with_filenames=True, with_syntax_error_trees=True):
        if tree is None:
            filename = url_helpers.get_filename_from_path(filepath)
            return 'syntax_error', filename


def has_indents_of_spaces(solution_repo, tab_size, *args, **kwargs):
    """
        Since there are cases for which col_offset is computed incorrectly,
        this validator must be nothing more than a simple warning.
    """
    node_types_to_validate = (ast.For, ast.If, ast.FunctionDef, ast.With)
    for filepath, file_content, tree in solution_repo.get_ast_trees(
        with_filenames=True,
        with_file_content=True
    ):
        lines_offsets = file_helpers.get_line_offsets(file_content)
        for node in ast.walk(tree):
            if not ast_helpers.is_node_offset_fine(
                node,
                lines_offsets,
                node_types_to_validate,
                tab_size,
            ):
                filename = url_helpers.get_filename_from_path(filepath)
                return 'indent_not_four_spaces', '{}:{}'.format(filename, node.lineno)
