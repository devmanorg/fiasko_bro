import os.path
from collections import OrderedDict

from . import pre_validation_checks
from . import validators


VALIDATION_PARAMETERS = {
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
    'directories_to_skip': [
        'build',
        'dist',
    ]
}

BLACKLISTS = {
    'has_variables_from_blacklist': [
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
    ],
    'has_no_commit_messages_from_blacklist': [
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
    ],
    'has_no_directories_from_blacklist': [
        '.idea',
        '__pycache__',
        '.vscode',
    ],
}

WHITELISTS = {
    'has_no_short_variable_names': [
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
    ],
    'has_no_calls_with_constants': [
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
    ],
    'is_snake_case': [
        # from sqlalchemy.sqlalchemy.orm.sessionmaker
        'Session',
        # from sqlalchemy.ext.automap
        'Base',
        'User',
        'Order',
        'Address',
    ],
    'right_assignment_for_snake_case': [
        'Base',
    ],
    'has_no_exit_calls_in_functions': [
        'main',
    ],
    'is_pep8_fine': [
        '{sep}migrations{sep}'.format(sep=os.path.sep),
        '{sep}alembic{sep}'.format(sep=os.path.sep),
        'manage.py',
    ],
    'has_no_encoding_declaration': [
        '{sep}migrations{sep}'.format(sep=os.path.sep),
    ],
    'has_no_local_imports': [
        'manage.py',
    ],
    'has_local_var_named_as_global': [
        'settings.py',
    ],
    'has_variables_from_blacklist': [
        'apps.py',
    ],
    'has_no_extra_dockstrings_whitelist': [
        '{sep}migrations{sep}'.format(sep=os.path.sep),
        '{sep}alembic{sep}'.format(sep=os.path.sep),
    ],
    'is_nesting_too_deep': [
        '{sep}migrations{sep}'.format(sep=os.path.sep),
        '{sep}alembic{sep}'.format(sep=os.path.sep),
        'manage.py',
        'settings.py',
    ],
}

PRE_VALIDATION_CHECKS = {
    'encoding': [
        pre_validation_checks.are_sources_in_utf
    ],
    'size': [
        pre_validation_checks.are_repos_too_large
    ],
    'bom': [
        pre_validation_checks.has_no_bom
    ]
}

ERROR_VALIDATOR_GROUPS = OrderedDict(
    [
        (
            'commits',
            [validators.has_more_commits_than_origin],
        ),
        (
            'readme',
            [validators.has_readme_file],
        ),
        (
            'syntax',
            [validators.has_no_syntax_errors],
        ),
        (
            'general',
            [
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
            ],
        ),
    ]
)

WARNING_VALIDATOR_GROUPS = {
    'commits': [
        validators.has_no_commit_messages_from_blacklist,
    ],
    'syntax': [
        validators.has_indents_of_spaces,
        validators.has_no_variables_that_shadow_default_names,
    ]
}

for name in WARNING_VALIDATOR_GROUPS:
    assert name in ERROR_VALIDATOR_GROUPS.keys()
