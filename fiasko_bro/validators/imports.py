from .. import ast_helpers
from .. import url_helpers


def has_no_star_imports(solution_repo, *args, **kwargs):
    for filepath, tree in solution_repo.get_ast_trees(with_filenames=True):
        if ast_helpers.is_tree_has_star_imports(tree):
            filename = url_helpers.get_filename_from_path(filepath)
            return 'has_star_import', filename


def has_no_local_imports(solution_repo, whitelists, *args, **kwargs):
    whitelist = whitelists.get('has_no_local_imports', [])
    for filepath, tree in solution_repo.get_ast_trees(with_filenames=True, whitelist=whitelist):
        if ast_helpers.is_has_local_imports(tree):
            filename = url_helpers.get_filename_from_path(filepath)
            return 'has_local_import', filename


def has_no_multiple_imports_on_same_line(solution_repo, *args, **kwargs):
    """Protects against the case
        import foo, bar
    """
    for filepath, tree in solution_repo.get_ast_trees(with_filenames=True):
        if 'file_with_multiple_imports_on_same_line' in filepath:
            imports = ast_helpers.get_all_imports(tree)
            for import_node in imports:
                if ast_helpers.is_multiple_imports_on_one_line(import_node):
                    filename = url_helpers.get_filename_from_path(filepath)
                    return 'has_multiple_imports_on_same_line', '{}:{}'.format(filename, import_node.lineno)
