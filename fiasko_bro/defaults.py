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
        (
            (
                'repo_size',
                (
                    pre_validation_checks.repo_is_too_large,
                ),
            ),
            (
                'encoding',
                (
                    pre_validation_checks.file_not_in_utf8,
                ),
            ),
            (
                'bom',
                (
                    pre_validation_checks.file_has_bom,
                ),
            ),
            (
                'file_size',
                (
                    pre_validation_checks.file_too_long,
                ),
            ),
        )
    )
)

ERROR_VALIDATOR_GROUPS = MappingProxyType(
    OrderedDict(
        (
            (
                'commits',
                (
                    validators.no_more_commits_than_origin,
                ),
            ),
            (
                'readme',
                (
                    validators.no_readme_file,
                ),
            ),
            (
                'syntax',
                (
                    validators.syntax_error,
                ),
            ),
            (
                'general',
                (
                    validators.data_in_repo,
                    validators.too_many_pep8_violations,
                    validators.readme_not_changed,
                    validators.camel_case_variable_name,
                    validators.too_difficult_by_mccabe,
                    validators.encoding_declaration,
                    validators.star_import,
                    validators.local_import,
                    validators.has_local_var_named_as_global,
                    validators.has_variables_from_blacklist,
                    validators.short_variable_name,
                    validators.range_starting_from_zero,
                    validators.tabs_used_for_indentation,
                    validators.except_block_class_too_broad,
                    validators.requirements_not_frozen,
                    validators.variable_assignment_with_lambda,
                    validators.call_with_constants,
                    validators.bilingual_readme,
                    validators.urls_with_hardcoded_get_parameters,
                    validators.nonpythonic_empty_list_validation,
                    validators.extra_docstrings,
                    validators.exit_call_in_function,
                    validators.has_libs_from_stdlib_in_requirements,
                    validators.line_ends_with_semicolon,
                    validators.validates_response_status_by_comparing_to_200,
                    validators.mutable_default_arguments,
                    validators.slice_starts_from_zero,
                    validators.casts_input_result_to_str,
                    validators.return_with_parenthesis,
                    validators.code_too_nested,
                    validators.string_literal_sum,
                    validators.has_pdb_breakpoint,
                    validators.has_multiple_imports_on_same_line,
                ),
            ),
        )
    )
)

WARNING_VALIDATOR_GROUPS = MappingProxyType(
    {
        'commits': (
            validators.commit_messages_from_blacklist,
        ),
        'syntax': (
            validators.indent_not_multiple_of_tab_size,
            validators.variables_that_shadow_default_names,
        ),
    }
)

for name in WARNING_VALIDATOR_GROUPS:
    assert name in ERROR_VALIDATOR_GROUPS.keys()
