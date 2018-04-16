from .. import ast_helpers
from .. import url_helpers


def has_no_star_imports(project_folder, *args, **kwargs):
    for parsed_file in project_folder.get_parsed_py_files():
        if ast_helpers.is_tree_has_star_imports(parsed_file.ast_tree):
            return 'has_star_import', parsed_file.name


def has_no_local_imports(project_folder, local_imports_paths_to_ignore, *args, **kwargs):
    for parsed_file in project_folder.get_parsed_py_files(whitelist=local_imports_paths_to_ignore):
        if ast_helpers.is_has_local_imports(parsed_file.ast_tree):
            return 'has_local_import', parsed_file.name
