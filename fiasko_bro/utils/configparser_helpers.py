import os

import configparser


def extract_fiasko_config_from_cfg_file(cfg_file_path, section_name='fiasko_bro'):
    if not os.path.exists(cfg_file_path):
        return {}
    config = configparser.ConfigParser()
    config.read(cfg_file_path)
    if not config.has_section(section_name):
        return {}
    return _process_section_to_dict_config(config[section_name])


def _process_section_to_dict_config(config_section):
    config_processors = {
        'readme_filename': lambda x: x,
        'allowed_max_pep8_violations': int,
        'max_complexity': int,
        'minimum_name_length': int,
        'min_percent_of_another_language': int,
        'last_commits_to_check_amount': int,
        'tab_size': int,
        'functions_with_docstrings_percent_limit': int,
        'max_pep8_line_length': int,
        'max_number_of_lines': int,
        'max_indentation_level': int,
        'max_num_of_py_files': int,
        'directories_to_skip': lambda x: x.split(',')
    }
    result_config = {}
    for param_name, param_processor in config_processors.items():
        if param_name not in config_section:
            continue
        result_config[param_name] = param_processor(config_section[param_name])
    return result_config
