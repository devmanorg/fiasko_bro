import os
import ast

import git


class LocalRepositoryInfo:
    def __init__(self, repository_path):
        self.path = repository_path
        self._repo = git.Repo(self.path)
        self._python_filenames, self._main_file_contents, self._ast_trees = (
            self._get_ast_trees(self.path)
        )

    def count_commits(self):
        return len(list(self._repo.iter_commits(paths=self.path)))

    def does_file_exist(self, filename):
        return os.path.isfile(os.path.join(self.path, filename))

    def _get_ast_trees(self, repository_path):
        filenames = []
        main_file_contents = []
        ast_trees = []
        for dirname, _, files in os.walk(repository_path, topdown=True):
            for file in files:
                if file.endswith('.py'):
                    filenames.append(os.path.join(dirname, file))
        for filename in filenames:
            with open(filename, 'r', encoding='utf-8') as file_handler:
                main_file_content = file_handler.read()
            try:
                tree = ast.parse(main_file_content)
                for node in ast.walk(tree):
                    for child in ast.iter_child_nodes(node):
                        child.parent = node
            except SyntaxError as e:
                print(e)
                tree = None
            main_file_contents.append(main_file_content)
            ast_trees.append(tree)
        return filenames, main_file_contents, ast_trees

    def get_ast_trees(self, with_filenames=False, with_file_content=False):
        if with_filenames:
            if with_file_content:
                return list(zip(self._python_filenames, self._main_file_contents, self._ast_trees))
            else:
                return list(zip(self._python_filenames, self._ast_trees))
        else:
            return list(self._ast_trees)
    
    def get_python_file_filenames(self):
        return self._python_filenames
    
    def get_file(self, filename):
        for dirname, _, files in os.walk(self.path, topdown=True):
            for file in files:
                if file == filename:
                    with open(os.path.join(dirname, file), encoding='utf-8') as file_handler:
                        return file_handler.read()
    
    def does_directory_exist(self, dirname_to_find):
        for dirname, dirs, _ in os.walk(self.path, topdown=True):
            if dirname == dirname_to_find or dirname_to_find in dirs:
                return True
        return False

    def iter_commits(self, *args, **kwargs):
        return self._repo.iter_commits(*args, **kwargs)
