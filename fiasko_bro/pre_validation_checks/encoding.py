import os

from ..utils.file_helpers import is_in_utf8


def file_not_in_utf8(project_path, directories_to_skip, *args, **kwargs):
    for root, dirs, filenames in os.walk(project_path):
        dirs[:] = [
            d for d in dirs
            if d not in directories_to_skip
        ]
        for name in filenames:
            if not is_in_utf8(os.path.join(root, name)):
                return name
