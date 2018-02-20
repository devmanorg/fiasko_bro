import builtins

from .. import ast_helpers
from ..i18n import _


def has_variables_from_blacklist(solution_repo, whitelists, blacklists, *args, **kwargs):
    whitelist = whitelists.get('has_variables_from_blacklist', [])
    blacklist = blacklists.get('has_variables_from_blacklist', [])
    for filename, tree in solution_repo.get_ast_trees(with_filenames=True, whitelist=whitelist):
        names = ast_helpers.get_all_defined_names(tree)
        bad_names = names.intersection(blacklist)
        if bad_names:
            return 'bad_titles', ', '.join(bad_names)


def has_local_var_named_as_global(solution_repo, whitelists, max_indentation_level, *args, **kwargs):
    whitelist = whitelists.get('has_local_var_named_as_global', [])
    for filename, tree in solution_repo.get_ast_trees(with_filenames=True, whitelist=whitelist):
        bad_names = ast_helpers.get_local_vars_named_as_globals(tree, max_indentation_level)
        if bad_names:
            message = _('for example, %s') % (', '.join(bad_names))
            return 'has_locals_named_as_globals', message


def has_no_short_variable_names(solution_repo, minimum_name_length, whitelists, *args, **kwargs):
    whitelist = whitelists.get('has_no_short_variable_names', [])
    short_names = []
    for tree in solution_repo.get_ast_trees():
        names = ast_helpers.get_all_defined_names(tree)
        short_names += [n for n in names
                        if len(n) < minimum_name_length and n not in whitelist]
    if short_names:
        return 'bad_titles', ', '.join(list(set(short_names)))


def is_snake_case(solution_repo, whitelists, *args, **kwargs):
    whitelist = whitelists.get('is_snake_case', [])
    right_assignment_whitelist = whitelists.get('right_assignment_for_snake_case', [])
    buildins_ = dir(builtins)
    for tree in solution_repo.get_ast_trees():
        names = ast_helpers.get_all_names_from_tree(tree)
        whitelisted_names = ast_helpers.get_names_from_assignment_with(
            tree,
            right_assignment_whitelist
        )
        imported_names = ast_helpers.get_all_imported_names_from_tree(tree)
        defined_class_names = ast_helpers.get_all_class_definitions_from_tree(tree)
        namedtuples = ast_helpers.get_all_namedtuple_names(tree)
        names_with_uppercase = [n for n in names
                                if n.lower() != n and n.upper() != n
                                and n not in imported_names
                                and n not in defined_class_names
                                and n not in namedtuples
                                and n not in buildins_
                                and n not in whitelist
                                and n not in whitelisted_names]
        if names_with_uppercase:
            message = _(
                'for example, rename the following: %s'
            ) % ', '.join(names_with_uppercase[:3])
            return 'camel_case_vars', message


def has_no_variables_that_shadow_default_names(solution_repo, *args, **kwargs):
    buildins_ = dir(builtins)
    for tree in solution_repo.get_ast_trees():
        names = ast_helpers.get_all_defined_names(tree, with_static_class_properties=False)
        bad_names = names.intersection(buildins_)
        if bad_names:
            return 'title_shadows', ', '.join(bad_names)
