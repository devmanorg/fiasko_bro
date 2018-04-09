from .. import code_helpers


def are_repos_too_large(
    project_path,
    directories_to_skip,
    max_num_of_py_files,
    original_project_path=None,
    *args,
    **kwargs
):
    if code_helpers.is_repo_too_large(project_path, directories_to_skip, max_num_of_py_files):
        return 'Repo is too large', ''
    if original_project_path:
        if code_helpers.is_repo_too_large(original_project_path, directories_to_skip, max_num_of_py_files):
            return 'Repo is too large', ''
