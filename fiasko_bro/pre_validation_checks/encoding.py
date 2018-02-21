import os

from ..file_helpers import is_in_utf8


def are_sources_in_utf(path_to_repo, *args, **kwargs):
    for root, dirs, filenames in os.walk(path_to_repo):
        for name in filenames:
            if not is_in_utf8(os.path.join(root, name)):
                return 'sources_not_utf_8', name
