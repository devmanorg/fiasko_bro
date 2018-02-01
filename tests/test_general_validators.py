import unittest

import git

from fiasko_bro import validators
from fiasko_bro.repository_info import LocalRepositoryInfo


class TestHasChangedReadme(unittest.TestCase):

    def setUp(self):
        test_repo_dir = 'test_fixtures/general_repo'
        origin_repo_dir = 'test_fixtures/general_repo_origin'
        git.Repo.init(test_repo_dir)
        git.Repo.init(origin_repo_dir)
        self.test_repo = LocalRepositoryInfo(test_repo_dir)
        self.origin_repo = LocalRepositoryInfo(origin_repo_dir)

    def test_readme_changed_succeeds(self):
        output = validators.has_changed_readme(
            solution_repo=self.test_repo,
            readme_filename='changed_readme.md',
            original_repo=self.origin_repo,
        )
        self.assertIsNone(output)

    def test_readme_changed_fails(self):
        expected_output = 'need_readme', None
        output = validators.has_changed_readme(
            solution_repo=self.test_repo,
            readme_filename='unchanged_readme.md',
            original_repo=self.origin_repo,
        )
        self.assertEqual(output, expected_output)


if __name__ == '__main__':
    unittest.main()
