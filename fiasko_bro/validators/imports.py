from .. import ast_helpers


def has_no_star_imports(solution_repo, *args, **kwargs):
    for tree in solution_repo.get_ast_trees():
        if ast_helpers.is_tree_has_star_imports(tree):
            return 'has_star_import', ''


def has_no_local_imports(solution_repo, whitelists, *args, **kwargs):
    whitelist = whitelists.get('has_no_local_imports', [])
    for filename, tree in solution_repo.get_ast_trees(with_filenames=True, whitelist=whitelist):
        if ast_helpers.is_has_local_imports(tree):
            return 'has_local_import', ''
