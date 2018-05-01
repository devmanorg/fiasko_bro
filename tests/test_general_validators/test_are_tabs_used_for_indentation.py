from fiasko_bro import validators
from fiasko_bro import defaults


def test_are_tabs_used_for_indentation_fails_for_different_types(test_repo):
    directories_to_skip = defaults.VALIDATION_PARAMETERS['directories_to_skip']
    extensions = {'py', 'js', 'css', 'html'}
    for extension in extensions:
        expected_output = 'tabs_used_for_indents', 'tabs.{}'.format(extension)
        files_to_ignore = extensions - {extension}
        output = validators.are_tabs_used_for_indentation(
            project_folder=test_repo,
            directories_to_skip=directories_to_skip.union(files_to_ignore)
        )
        assert output == expected_output
