import shutil

import git


def initialize_repo(repo_path, ignore_gitignore=False):
    arguments = ['.']
    if ignore_gitignore:
        arguments.append('-f')  # needed to ensure the global gitignore does not disrupt the test
    repo = git.Repo.init(repo_path)
    repo.git.add(arguments)
    repo.index.commit('Initial commit')


def remove_repo(repo_path):
    git_folder_path = '{}/.git'.format(repo_path)
    shutil.rmtree(git_folder_path, ignore_errors=True)
