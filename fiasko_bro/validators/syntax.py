import ast

from ..utils import ast_helpers, file_helpers


def syntax_error(project_folder, *args, **kwargs):
    for parsed_file in project_folder.get_parsed_py_files():
        if not parsed_file.is_syntax_correct:
            return parsed_file.name


def indent_not_multiple_of_tab_size(project_folder, tab_size, *args, **kwargs):
    """
        Since there are cases for which col_offset is computed incorrectly,
        this validator must be nothing more than a simple warning.

        It compliments the pep8 validator which tends to fail in cases when
        the indent is incorrect.
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
                return parsed_file.get_name_with_line(node.lineno)
