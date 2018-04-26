from ..utils import ast_helpers, url_helpers


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
