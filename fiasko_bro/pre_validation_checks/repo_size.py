from .. import code_helpers


def are_repos_too_large(path_to_repo, max_num_of_py_files, path_to_original_repo=None, *args, **kwargs):
    if code_helpers.is_repo_too_large(path_to_repo, max_num_of_py_files):
        return 'Repo is too large', ''
    if path_to_original_repo:
        if code_helpers.is_repo_too_large(path_to_original_repo, max_num_of_py_files):
            return 'Repo is too large', ''
