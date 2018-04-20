from fiasko_bro import defaults
from fiasko_bro.validators import commit_messages_from_blacklist


def test_commit_messages_from_blacklist_fails(test_repo):
    expected_output = 'win'
    last_commits_to_check_amount = defaults.VALIDATION_PARAMETERS['last_commits_to_check_amount']
    bad_commit_messages = defaults.VALIDATION_PARAMETERS['bad_commit_messages']
    output = commit_messages_from_blacklist(
        project_folder=test_repo,
        bad_commit_messages=bad_commit_messages,
        last_commits_to_check_amount=last_commits_to_check_amount
    )
    assert output == expected_output


def test_commit_messages_from_blacklist_succeeds(origin_repo):
    last_commits_to_check_amount = defaults.VALIDATION_PARAMETERS['last_commits_to_check_amount']
    bad_commit_messages = defaults.VALIDATION_PARAMETERS['bad_commit_messages']
    output = commit_messages_from_blacklist(
        project_folder=origin_repo,
        bad_commit_messages=bad_commit_messages,
        last_commits_to_check_amount=last_commits_to_check_amount
    )
    assert output is None
