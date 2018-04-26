from ..utils import url_helpers


def has_no_long_files(solution_repo, max_number_of_lines, *args, **kwargs):
    for file_path, file_content, _ in solution_repo.get_ast_trees(
        with_filenames=True,
        with_file_content=True
    ):
        number_of_lines = file_content.count('\n')
        if number_of_lines > max_number_of_lines:
            file_name = url_helpers.get_filename_from_path(file_path)
            return 'file_too_long', file_name
