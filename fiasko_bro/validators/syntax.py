import ast

from .. import ast_helpers
from .. import file_helpers


def has_no_syntax_errors(project_folder, *args, **kwargs):
    for parsed_file in project_folder.get_parsed_py_files():
        if not parsed_file.is_syntax_correct:
            return 'syntax_error', parsed_file.name


def has_indents_of_spaces(project_folder, tab_size, *args, **kwargs):
    """
        Since there are cases for which col_offset is computed incorrectly,
        this validator must be nothing more than a simple warning.
    """
    node_types_to_validate = (ast.For, ast.If, ast.FunctionDef, ast.With)
    for parsed_file in project_folder.get_parsed_py_files():
        lines_offsets = file_helpers.get_line_offsets(parsed_file.content)
        for node in ast.walk(parsed_file.ast_tree):
            if not ast_helpers.is_node_offset_fine(
                node,
                lines_offsets,
                node_types_to_validate,
                tab_size,
            ):
                return 'indent_not_four_spaces', '{}:{}'.format(parsed_file.name, node.lineno)
