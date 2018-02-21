import os

from .. import url_helpers


def has_no_long_files(solution_repo, max_number_of_lines, *args, **kwargs):
    for file_path, file_content, _ in solution_repo.get_ast_trees(
        with_filenames=True,
        with_file_content=True
    ):
        number_of_lines = file_content.count('\n')
        if number_of_lines > max_number_of_lines:
            file_name = url_helpers.get_filename_from_path(file_path)
            return 'file_too_long', file_name


def are_tabs_used_for_indentation(solution_repo, *args, **kwargs):
    frontend_extensions = ['.html', '.css', '.js']
    relevant_extensions = frontend_extensions + ['.py']
    for filepath, file_content in solution_repo.get_source_file_contents(relevant_extensions):
        lines = [l for l in file_content.split('\n') if l]
        tabbed_lines_amount = len([l for l in lines if l.startswith('\t')])
        _, ext = os.path.splitext(filepath)
        filename = url_helpers.get_filename_from_path(filepath)
        is_frontend = ext in frontend_extensions
        if ext == '.py':
            # строки могут начинаться с таба в многострочной строке, поэтому такая эвристика
            if tabbed_lines_amount > len(lines) / 2:
                return 'tabs_used_for_indents', filename
        elif is_frontend and tabbed_lines_amount:
            return 'tabs_used_for_indents', filename


def has_no_encoding_declaration(solution_repo, whitelists, *args, **kwargs):
    whitelist = whitelists.get('has_no_encoding_declaration', [])
    for filepath, file_content, _ in solution_repo.get_ast_trees(
        with_filenames=True,
        with_file_content=True,
        whitelist=whitelist,
    ):
        first_line = file_content.strip('\n').split('\n')[0].strip().replace(' ', '')
        if first_line.startswith('#') and 'coding:utf-8' in first_line:
            filename = url_helpers.get_filename_from_path(filepath)
            return 'has_encoding_declarations', filename


def has_no_directories_from_blacklist(solution_repo, blacklists, *args, **kwargs):
    blacklist = blacklists.get('has_no_directories_from_blacklist', [])
    for dirname in blacklist:
        if solution_repo.does_directory_exist(dirname):
            return 'data_in_repo', dirname
