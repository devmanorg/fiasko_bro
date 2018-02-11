import ast

from .. import ast_helpers
from .. import file_helpers
from ..i18n import _ as _t


def has_no_syntax_errors(solution_repo, *args, **kwargs):
    for filename, tree in solution_repo.get_ast_trees(with_filenames=True):
        if tree is None:
            return 'syntax_error', filename


def has_indents_of_spaces(solution_repo, tab_size, *args, **kwargs):
    """
        Иногда при парсинге дерева col_offset считается неправильно,
    """
    node_types_to_validate = (ast.For, ast.If, ast.FunctionDef, ast.With)
    for _, file_content, tree in solution_repo.get_ast_trees(
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
                return 'indent_not_four_spaces', _t('for example, line number %s') % node.lineno
