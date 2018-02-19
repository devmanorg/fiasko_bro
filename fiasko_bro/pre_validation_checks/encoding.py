import os


def are_sources_in_utf(path_to_repo, *args, **kwargs):
    for root, dirs, filenames in os.walk(path_to_repo):
        for name in filenames:
            if name.endswith('.py') or name.endswith('.txt'):
                try:
                    with open((os.path.join(root, name)), mode='r', encoding='utf-8') as file_handle:
                        file_handle.read()
                except UnicodeDecodeError:
                    return 'sources_not_utf_8', None
