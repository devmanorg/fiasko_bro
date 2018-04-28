import shutil

import git


def initialize_repo(repo_path):
    repo = git.Repo.init(repo_path)
    repo.index.add(['.'])
    repo.index.commit('Initial commit')


def remove_repo(repo_path):
    git_folder_path = '{}/.git'.format(repo_path)
    shutil.rmtree(git_folder_path)
