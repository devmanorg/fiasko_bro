import os
import codecs


def file_has_bom(project_path, directories_to_skip, *args, **kwargs):
    for root, dirs, filenames in os.walk(project_path):
        dirs[:] = [
            d for d in dirs
            if d not in directories_to_skip
        ]
        for name in filenames:
            with open(os.path.join(root, name), 'rb') as file_handle:
                file_content = file_handle.read(3)  # we don't need to read the whole file
                if file_content.startswith(codecs.BOM_UTF8):
                    return name
