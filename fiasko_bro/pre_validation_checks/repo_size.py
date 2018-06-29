import os

from ..utils import code_helpers, file_helpers


def repo_is_too_large(
    project_path,
    directories_to_skip,
    max_num_of_py_files,
    original_project_path=None,
    *args,
    **kwargs
):
    if code_helpers.is_repo_too_large(project_path, directories_to_skip, max_num_of_py_files):
        return ''
    if original_project_path:
        if code_helpers.is_repo_too_large(original_project_path, directories_to_skip, max_num_of_py_files):
            return ''


def file_too_long(project_path, max_number_of_lines, directories_to_skip, *args, **kwargs):
    for root, dirs, filenames in os.walk(project_path):
        dirs[:] = [
            d for d in dirs
            if d not in directories_to_skip
        ]
        for name in filenames:
            if name.endswith('.py'):
                path = '{}{}{}'.format(root, os.path.sep, name)
                if file_helpers.is_file_too_long(path, max_number_of_lines):
                    return name
