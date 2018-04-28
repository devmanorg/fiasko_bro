import git

def initialize_repo(repo_path):
    repo = git.Repo.init(repo_path)
    repo.index.add(['.'])
    repo.index.commit('Initial commit')
