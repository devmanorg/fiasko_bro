from fiasko_bro.validators import has_more_commits_than_origin


def test_has_more_commits_than_origin_succeed_no_origin(test_repo):
    output = has_more_commits_than_origin(test_repo)
    assert output is None


def test_has_more_commits_than_origin_succeed_more_commits(test_repo, origin_repo):
    output = has_more_commits_than_origin(test_repo, origin_repo)
    assert output is None


def test_has_more_commits_than_origin_fail(origin_repo):
    expected_output = 'no_new_code', None
    output = has_more_commits_than_origin(origin_repo, origin_repo)
    assert output == expected_output
