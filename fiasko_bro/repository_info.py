import os
import ast
import copy

import git

from fiasko_bro.config import VALIDATOR_SETTINGS
from . import file_helpers


class LocalRepositoryInfo:
    def __init__(self, repository_path):
        self.path = repository_path
        self._repo = git.Repo(self.path)
        self._python_filenames, self._main_file_contents, self._ast_trees = (
            self._get_ast_trees()
        )

    def count_commits(self):
        return len(list(self._repo.iter_commits()))

    def does_file_exist(self, filename):
        return os.path.isfile(os.path.join(self.path, filename))

    def get_source_file_contents(self, extension_list):
        file_paths = []
        file_contents = []
        for dirname, directories_list, filenames in os.walk(self.path, topdown=True):
            directories_list[:] = [
                d for d in directories_list
                if d not in VALIDATOR_SETTINGS['directories_to_skip']
            ]
            for filename in filenames:
                extension = os.path.splitext(filename)[1]
                if extension in extension_list:
                    file_paths.append(os.path.join(dirname, filename))
        for file_path in file_paths:
            with open(file_path, 'r', encoding='utf-8') as file_handler:
                file_contents.append(file_handler.read())
        source_file_contents = list(zip(file_paths, file_contents))
        return source_file_contents

    def _get_ast_trees(self):
        py_files = list(zip(*self.get_source_file_contents(['.py']))) or [(), ()]
        filenames, main_file_contents = py_files
        ast_trees = []
        for file_content in main_file_contents:
            try:
                tree = ast.parse(file_content)
            except SyntaxError as e:
                tree = None
            if tree:
                self._set_parents(tree)
            ast_trees.append(tree)
        return filenames, main_file_contents, ast_trees

    def get_ast_trees(self, with_filenames=False, with_file_content=False, whitelist=None, return_none=False):
        ast_trees_copy = copy.deepcopy(self._ast_trees)
        all_items = zip(self._python_filenames, self._main_file_contents, ast_trees_copy)
        filtered_items = self.filter_file_paths(all_items, whitelist)
        if return_none:
            filtered_items = [r for r in filtered_items]
        else:
            filtered_items = [r for r in filtered_items if r[2] is not None]

        if with_filenames:
            if with_file_content:
                return filtered_items
            else:
                return [(f, t) for (f, c, t) in filtered_items]
        else:
            return [t for t in ast_trees_copy if t is not None]

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

    @staticmethod
    def filter_file_paths(all_items, whitelist):
        if not whitelist:
            return all_items
        filtered_items = []
        for file_name, file_content, ast_tree in all_items:
            if not file_helpers.is_filename_in_whitelist(file_name, whitelist):
                filtered_items.append(
                    (file_name, file_content, ast_tree)
                )
        return filtered_items

    @staticmethod
    def _set_parents(tree):
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                child.parent = node
