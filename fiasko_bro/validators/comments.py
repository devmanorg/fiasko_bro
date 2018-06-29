import ast

from ..utils import ast_helpers


def extra_docstrings(
    project_folder,
    extra_dockstrings_paths_to_ignore,
    functions_with_docstrings_percent_limit,
    *args,
    **kwargs
):
    for parsed_file in project_folder.get_parsed_py_files(whitelist=extra_dockstrings_paths_to_ignore):
        defs = ast_helpers.get_nodes_of_type(parsed_file.ast_tree, ast.FunctionDef)
        if not defs:
            continue

        docstrings = [ast.get_docstring(d) for d in defs if ast.get_docstring(d) is not None]
        if len(docstrings) / len(defs) * 100 > functions_with_docstrings_percent_limit:
            return parsed_file.name
