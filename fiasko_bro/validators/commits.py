

def has_more_commits_than_origin(project_folder, original_project_folder=None, *args, **kwargs):
    if not original_project_folder:
        return
    if not project_folder.repo or not original_project_folder.repo:
        return
    # FIXME this check works incorrectly in case of
    # new commit in original repo after student forked it
    if project_folder.repo.count_commits() <= original_project_folder.repo.count_commits():
        return 'no_new_code', None


def has_no_commit_messages_from_blacklist(project_folder, blacklists, last_commits_to_check_amount, *args, **kwargs):
    if not project_folder.repo:
        return
    blacklist = blacklists.get('has_no_commit_messages_from_blacklist', [])
    for commit in project_folder.repo.iter_commits('master', max_count=last_commits_to_check_amount):
        message = commit.message.lower().strip().strip('.\'"')
        if message in blacklist:
            return 'git_history_warning', message
