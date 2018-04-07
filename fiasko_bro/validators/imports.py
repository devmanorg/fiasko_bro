from .. import ast_helpers
from .. import url_helpers


def has_no_star_imports(solution_repo, *args, **kwargs):
    for parsed_file in solution_repo.get_parsed_py_files():
        if ast_helpers.is_tree_has_star_imports(parsed_file.ast_tree):
            return 'has_star_import', parsed_file.name


def has_no_local_imports(solution_repo, whitelists, *args, **kwargs):
    whitelist = whitelists.get('has_no_local_imports', [])
    for parsed_file in solution_repo.get_parsed_py_files(whitelist=whitelist):
        if ast_helpers.is_has_local_imports(parsed_file.ast_tree):
            return 'has_local_import', parsed_file.name
