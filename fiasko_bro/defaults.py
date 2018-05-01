import os.path
from collections import OrderedDict
from types import MappingProxyType

from . import pre_validation_checks
from . import validators


VALIDATION_PARAMETERS = MappingProxyType(
    {
        'readme_filename': 'README.md',
        'allowed_max_pep8_violations': 5,
        'max_complexity': 7,
        'minimum_name_length': 2,
        'min_percent_of_another_language': 30,
        'last_commits_to_check_amount': 5,
        'tab_size': 4,
        'functions_with_docstrings_percent_limit': 80,
        'max_pep8_line_length': 100,
        'max_number_of_lines': 200,
        'max_indentation_level': 4,
        'max_num_of_py_files': 100,
        'directories_to_skip': frozenset(
            [
                'build',
                'dist',
                '.git',
            ]
        ),
        'bad_variable_names': frozenset(
            [
                'list',
                'lists',
                'input',
                'cnt',
                'data',
                'name',
                'load',
                'value',
                'object',
                'file',
                'result',
                'item',
                'num',
                'info',
                'n',
            ]
        ),
        'bad_commit_messages': frozenset(
            [
                'win',
                'commit',
                'commit#1',
                'fix',
                'minor edits',
                'update',
                'done',
                'first commit',
                'start',
                'refactor',
                '!',
                'bug fix',
                'corrected',
                'add files via upload',
                'test',
                'fixed',
                'minor bugfix',
                'minor bugfixes',
                'finished',
                'first commit',
                'fixes',
                '',
            ]
        ),
        'data_directories': frozenset(
            [
                '.idea',
                '__pycache__',
                '.vscode',
            ]
        ),
        'valid_short_variable_names': frozenset(
            [
                'a',
                'b',
                'c',
                'x',
                'y',
                'x1',
                'x2',
                'y1',
                'y2',
                '_',
            ]
        ),
        'valid_calls_with_constants': frozenset(
            [
                'pow',
                'exit',
                'round',
                'range',
                'enumerate',
                'time',
                'itemgetter',
                'get',
                'group',
                'replace',
                'combinations',
                'seek',
            ]
        ),
        'valid_non_snake_case_left_hand_values': frozenset(
            [
                # from sqlalchemy.sqlalchemy.orm.sessionmaker
                'Session',
                # from sqlalchemy.ext.automap
                'Base',
                'User',
                'Order',
                'Address',
            ]
        ),
        'valid_non_snake_case_right_hand_values': frozenset(
            [
                'Base',
            ]
        ),
        'functions_allowed_to_have_exit_calls': frozenset(
            [
                'main',
            ]
        ),
        'pep8_paths_to_ignore': frozenset(
            [
                '{sep}migrations{sep}'.format(sep=os.path.sep),
                '{sep}alembic{sep}'.format(sep=os.path.sep),
                'manage.py',
            ]
        ),
        'encoding_declarations_paths_to_ignore': frozenset(
            [
                '{sep}migrations{sep}'.format(sep=os.path.sep),
            ]
        ),
        'local_imports_paths_to_ignore': frozenset(
            [
                'manage.py',
            ]
        ),
        'local_var_named_as_global_paths_to_ignore': frozenset(
            [
                'settings.py',
            ]
        ),
        'bad_variables_paths_to_ignore': frozenset(
            [
                'apps.py',
            ]
        ),
        'extra_dockstrings_paths_to_ignore': frozenset(
            [
                '{sep}migrations{sep}'.format(sep=os.path.sep),
                '{sep}alembic{sep}'.format(sep=os.path.sep),
            ]
        ),
        'deep_nesting_paths_to_ignore': frozenset(
            [
                '{sep}migrations{sep}'.format(sep=os.path.sep),
                '{sep}alembic{sep}'.format(sep=os.path.sep),
                'manage.py',
                'settings.py',
            ]
        ),
    }
)

PRE_VALIDATION_CHECKS = MappingProxyType(
    OrderedDict(
        {
            'encoding': (
                pre_validation_checks.are_sources_in_utf,
            ),
            'size': (
                pre_validation_checks.are_repos_too_large,
            ),
            'bom': (
                pre_validation_checks.has_no_bom,
            ),
        }
    )
)

ERROR_VALIDATOR_GROUPS = MappingProxyType(
    OrderedDict(
        {
            'commits': (
                validators.has_more_commits_than_origin,
            ),
            'readme': (
                validators.has_readme_file,
            ),
            'syntax': (
                validators.has_no_syntax_errors,
            ),
            'general': (
                validators.has_no_directories_from_blacklist,
                validators.is_pep8_fine,
                validators.has_changed_readme,
                validators.is_snake_case,
                validators.is_mccabe_difficulty_ok,
                validators.has_no_encoding_declaration,
                validators.has_no_star_imports,
                validators.has_no_local_imports,
                validators.has_local_var_named_as_global,
                validators.has_variables_from_blacklist,
                validators.has_no_short_variable_names,
                validators.has_no_range_from_zero,
                validators.are_tabs_used_for_indentation,
                validators.has_no_try_without_exception,
                validators.has_frozen_requirements,
                validators.has_no_vars_with_lambda,
                validators.has_no_calls_with_constants,
                validators.has_readme_in_single_language,
                validators.has_no_urls_with_hardcoded_arguments,
                validators.has_no_nonpythonic_empty_list_validations,
                validators.has_no_extra_dockstrings,
                validators.has_no_exit_calls_in_functions,
                validators.has_no_libs_from_stdlib_in_requirements,
                validators.has_no_lines_ends_with_semicolon,
                validators.not_validates_response_status_by_comparing_to_200,
                validators.has_no_mutable_default_arguments,
                validators.has_no_slices_starts_from_zero,
                validators.has_no_cast_input_result_to_str,
                validators.has_no_return_with_parenthesis,
                validators.has_no_long_files,
                validators.is_nesting_too_deep,
                validators.has_no_string_literal_sums,
            ),
        }
    )
)

WARNING_VALIDATOR_GROUPS = MappingProxyType(
    {
        'commits': (
            validators.has_no_commit_messages_from_blacklist,
        ),
        'syntax': (
            validators.has_indents_of_spaces,
            validators.has_no_variables_that_shadow_default_names,
        ),
    }
)

for name in WARNING_VALIDATOR_GROUPS:
    assert name in ERROR_VALIDATOR_GROUPS.keys()
