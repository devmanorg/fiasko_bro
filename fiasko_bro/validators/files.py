import os

from .. import url_helpers


def long_file(project_folder, max_number_of_lines, *args, **kwargs):
    for parsed_file in project_folder.get_parsed_py_files():
        number_of_lines = parsed_file.content.count('\n')
        if number_of_lines > max_number_of_lines:
            return parsed_file.name


def tabs_used_for_indentation(project_folder, directories_to_skip, *args, **kwargs):
    frontend_extensions = ['.html', '.css', '.js']
    relevant_extensions = frontend_extensions + ['.py']
    files_info = project_folder.get_source_file_contents(relevant_extensions, directories_to_skip)
    if not files_info:
        return
    for filepath, file_content in files_info:
        lines = [l for l in file_content.split('\n') if l]
        tabbed_lines_amount = len([l for l in lines if l.startswith('\t')])
        _, ext = os.path.splitext(filepath)
        filename = url_helpers.get_filename_from_path(filepath)
        is_frontend = ext in frontend_extensions
        if ext == '.py':
            # строки могут начинаться с таба в многострочной строке, поэтому такая эвристика
            if tabbed_lines_amount > len(lines) / 2:
                return filename
        elif is_frontend and tabbed_lines_amount:
            return filename


def encoding_declaration(project_folder, encoding_declarations_paths_to_ignore, *args, **kwargs):
    for parsed_file in project_folder.get_parsed_py_files(whitelist=encoding_declarations_paths_to_ignore):
        first_line = parsed_file.content.strip('\n').split('\n')[0].strip().replace(' ', '')
        if first_line.startswith('#') and 'coding:utf-8' in first_line:
            return parsed_file.name


def data_in_repo(project_folder, data_directories, *args, **kwargs):
    for dirname in data_directories:
        if project_folder.does_directory_exist(dirname):
            return dirname
