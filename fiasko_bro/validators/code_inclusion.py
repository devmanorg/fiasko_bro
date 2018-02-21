from .. import code_helpers
from .. import url_helpers
from .. import file_helpers


def is_mccabe_difficulty_ok(solution_repo, max_complexity, *args, **kwargs):
    violations = []
    for filename, _ in solution_repo.get_ast_trees(with_filenames=True):
        violations += code_helpers.get_mccabe_violations_for_file(filename, max_complexity)
    if violations:
        return 'mccabe_failure', ','.join(violations)


def is_nesting_too_deep(solution_repo, tab_size, max_indentation_level, whitelists, *args, **kwargs):
    """
        Looks at the number of spaces in the beginning and decides if the code is
        too nested.

        As a precondition, the code has to pass has_indents_of_spaces.
    """
    whitelist = whitelists.get('is_nesting_too_deep', [])
    for file_path, file_content, _ in solution_repo.get_ast_trees(
        with_filenames=True,
        with_file_content=True,
        whitelist=whitelist
    ):
        lines = file_content.split('\n')
        previous_line_indent = 0
        for line_number, line in enumerate(lines):
            indentation_spaces_amount = code_helpers.count_indentation_spaces(line, tab_size)
            if (
                indentation_spaces_amount > tab_size * max_indentation_level
                # make sure it's not a line continuation
                and indentation_spaces_amount - previous_line_indent == tab_size
            ):
                file_name = url_helpers.get_filename_from_path(file_path)
                return 'too_nested', '{}:{}'.format(file_name, line_number)
            previous_line_indent = indentation_spaces_amount
