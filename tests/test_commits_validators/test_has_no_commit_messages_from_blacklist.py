from fiasko_bro.validators import has_no_commit_messages_from_blacklist
from fiasko_bro.code_validator import CodeValidator


def test_has_no_commit_messages_from_blacklist_fails(test_repo):
    expected_output = 'git_history_warning', ''
    last_commits_to_check_amount = CodeValidator._default_settings['last_commits_to_check_amount']
    output = has_no_commit_messages_from_blacklist(
        project_folder=test_repo,
        blacklists=CodeValidator.blacklists,
        last_commits_to_check_amount=last_commits_to_check_amount
    )
    assert output == expected_output


def test_has_no_commit_messages_from_blacklist_succeeds(origin_repo):
    last_commits_to_check_amount = CodeValidator._default_settings['last_commits_to_check_amount']
    output = has_no_commit_messages_from_blacklist(
        project_folder=origin_repo,
        blacklists=CodeValidator.blacklists,
        last_commits_to_check_amount=last_commits_to_check_amount
    )
    assert output is None
