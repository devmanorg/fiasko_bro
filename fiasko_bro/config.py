import os.path


VALIDATOR_SETTINGS = {
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
}

DEFAULT_BLACKLISTS = {
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

DEFAULT_WHITELISTS = {
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
