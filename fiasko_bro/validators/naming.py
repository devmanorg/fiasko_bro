import builtins

from ..utils import ast_helpers
from ..i18n import _


def has_variables_from_blacklist(project_folder, bad_variables_paths_to_ignore, bad_variable_names, *args, **kwargs):
    for parsed_file in project_folder.get_parsed_py_files(whitelist=bad_variables_paths_to_ignore):
        names = ast_helpers.get_all_defined_names(parsed_file.ast_tree)
        bad_names = names.intersection(bad_variable_names)
        if bad_names:
            return 'bad_titles', ', '.join(bad_names)


def has_local_var_named_as_global(project_folder, local_var_named_as_global_paths_to_ignore, max_indentation_level, *args, **kwargs):
    for parsed_file in project_folder.get_parsed_py_files(whitelist=local_var_named_as_global_paths_to_ignore):
        bad_names = ast_helpers.get_local_vars_named_as_globals(parsed_file.ast_tree, max_indentation_level)
        if bad_names:
            message = _('for example, %s') % (', '.join(bad_names))
            return 'has_locals_named_as_globals', message


def has_no_short_variable_names(project_folder, minimum_name_length, valid_short_variable_names, *args, **kwargs):
    short_names = []
    for parsed_file in project_folder.get_parsed_py_files():
        names = ast_helpers.get_all_defined_names(parsed_file.ast_tree)
        short_names += [n for n in names
                        if len(n) < minimum_name_length and n not in valid_short_variable_names]
    if short_names:
        return 'bad_titles', ', '.join(list(set(short_names)))


def is_snake_case(project_folder, valid_non_snake_case_left_hand_values, valid_non_snake_case_right_hand_values, *args, **kwargs):
    buildins_ = dir(builtins)
    for parsed_file in project_folder.get_parsed_py_files():
        names = ast_helpers.get_all_names_from_tree(parsed_file.ast_tree)
        whitelisted_names = ast_helpers.get_names_from_assignment_with(
            parsed_file.ast_tree,
            valid_non_snake_case_right_hand_values
        )
        imported_names = ast_helpers.get_all_imported_names_from_tree(parsed_file.ast_tree)
        defined_class_names = ast_helpers.get_all_class_definitions_from_tree(parsed_file.ast_tree)
        namedtuples = ast_helpers.get_all_namedtuple_names(parsed_file.ast_tree)
        names_with_uppercase = [n for n in names
                                if n.lower() != n and n.upper() != n
                                and n not in imported_names
                                and n not in defined_class_names
                                and n not in namedtuples
                                and n not in buildins_
                                and n not in valid_non_snake_case_left_hand_values
                                and n not in whitelisted_names]
        if names_with_uppercase:
            message = _(
                'for example, rename the following: %s'
            ) % ', '.join(names_with_uppercase[:3])
            return 'camel_case_vars', message


def has_no_variables_that_shadow_default_names(project_folder, *args, **kwargs):
    buildins_ = dir(builtins)
    for parsed_file in project_folder.get_parsed_py_files():
        names = ast_helpers.get_all_defined_names(parsed_file.ast_tree, with_static_class_properties=False)
        bad_names = names.intersection(buildins_)
        if bad_names:
            return 'title_shadows', ', '.join(bad_names)
