import os
import codecs
from fiasko_bro.config import VALIDATOR_SETTINGS


def has_no_bom(project_path, *args, **kwargs):
    for root, dirs, filenames in os.walk(project_path):
        dirs[:] = [
            d for d in dirs
            if d not in VALIDATOR_SETTINGS['directories_to_skip']
        ]
        for name in filenames:
            with open(os.path.join(root, name), 'rb') as file_handle:
                file_content = file_handle.read()
                if file_content.startswith(codecs.BOM_UTF8):
                    return 'has_bom', name
