

def has_more_commits_than_origin(solution_repo, original_repo=None, *args, **kwargs):
    if not original_repo:
        return
    # FIXME this check works incorrectly in case of
    # new commit in original repo after student forked it
    if solution_repo.count_commits() <= original_repo.count_commits():
        return 'no_new_code', None


def has_no_commit_messages_from_blacklist(solution_repo, blacklists, last_commits_to_check_amount, *args, **kwargs):
    blacklist = blacklists.get('has_no_commit_messages_from_blacklist', [])
    for commit in solution_repo.iter_commits('master', max_count=last_commits_to_check_amount):
        message = commit.message.lower().strip().strip('.\'"')
        if message in blacklist:
            return 'git_history_warning', ''
