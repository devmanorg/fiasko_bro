import ast

from ..utils import ast_helpers


def return_with_parenthesis(project_folder, *args, **kwargs):
    for parsed_file in project_folder.get_parsed_py_files():
        file_content = parsed_file.content.split('\n')
        return_lines = [n.lineno for n in ast.walk(parsed_file.ast_tree) if isinstance(n, ast.Return)]
        for line_num in return_lines:
            line = file_content[line_num - 1]
            if (
                line.count('return') == 1
                and (
                    'return(' in line
                    or 'return (' in line
                )
                and line.strip().endswith(')')
            ):
                return parsed_file.get_name_with_line(line_num)


def line_ends_with_semicolon(project_folder, *args, **kwargs):
    for parsed_file in project_folder.get_parsed_py_files():
        total_lines_with_semicolons = len(
            [1 for l in parsed_file.content.split('\n') if l.endswith(';') and not l.startswith('#')]
        )
        # TODO: check docstrings for semicolons
        string_nodes = ast_helpers.get_nodes_of_type(parsed_file.ast_tree, ast.Str)
        semicolons_in_string_constants_amount = sum([n.s.count(';') for n in string_nodes])
        if total_lines_with_semicolons > semicolons_in_string_constants_amount:
            return parsed_file.name
