from fiasko_bro import defaults
from fiasko_bro.validators import has_no_commit_messages_from_blacklist


def test_has_no_commit_messages_from_blacklist_fails(test_repo):
    expected_output = 'git_history_warning', 'win'
    last_commits_to_check_amount = defaults.VALIDATION_PARAMETERS['last_commits_to_check_amount']
    output = has_no_commit_messages_from_blacklist(
        project_folder=test_repo,
        blacklists=defaults.BLACKLISTS,
        last_commits_to_check_amount=last_commits_to_check_amount
    )
    assert output == expected_output


def test_has_no_commit_messages_from_blacklist_succeeds(origin_repo):
    last_commits_to_check_amount = defaults.VALIDATION_PARAMETERS['last_commits_to_check_amount']
    output = has_no_commit_messages_from_blacklist(
        project_folder=origin_repo,
        blacklists=defaults.BLACKLISTS,
        last_commits_to_check_amount=last_commits_to_check_amount
    )
    assert output is None
