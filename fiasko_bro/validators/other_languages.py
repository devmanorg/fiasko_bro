import ast

from .. import ast_helpers
from .. import i18n


def has_no_return_with_parenthesis(solution_repo, *args, **kwargs):
    for _, file_content, tree in solution_repo.get_ast_trees(
        with_filenames=True,
        with_file_content=True
    ):
        file_content = file_content.split('\n')
        return_lines = [n.lineno for n in ast.walk(tree) if isinstance(n, ast.Return)]
        for line_num in return_lines:
            line = file_content[line_num - 1]
            if line.count('return') == 1 and 'return(' in line or 'return (' in line:
                message = i18n._('for example, the line number %s') % line_num
                return 'return_with_parenthesis', message


def has_no_lines_ends_with_semicolon(solution_repo, *args, **kwargs):
    for _, file_content, tree in solution_repo.get_ast_trees(
        with_filenames=True,
        with_file_content=True
    ):
        total_lines_with_semicolons = len(
            [1 for l in file_content.split('\n') if l.endswith(';') and not l.startswith('#')]
        )
        # TODO: check docstrings for semicolons
        string_nodes = ast_helpers.get_nodes_of_type(tree, ast.Str)
        semicolons_in_string_constants_amount = sum([n.s.count(';') for n in string_nodes])
        if total_lines_with_semicolons > semicolons_in_string_constants_amount:
            return 'has_semicolons', ''
