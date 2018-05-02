from ..utils import code_helpers


def too_difficult_by_mccabe(project_folder, max_complexity, *args, **kwargs):
    violations = []
    for parsed_file in project_folder.get_parsed_py_files():
        violations += code_helpers.get_mccabe_violations_for_file(parsed_file.path, max_complexity)
    if violations:
        return ','.join(violations)


def code_too_nested(project_folder, tab_size, max_indentation_level, deep_nesting_paths_to_ignore, *args, **kwargs):
    """
        Looks at the number of spaces in the beginning and decides if the code is
        too nested.

        As a precondition, the code has to pass indent_not_multiple_of_tab_size.
    """
    for parsed_file in project_folder.get_parsed_py_files(whitelist=deep_nesting_paths_to_ignore):
        lines = parsed_file.content.split('\n')
        previous_line_indent = 0
        for line_number, line in enumerate(lines):
            indentation_spaces_amount = code_helpers.count_indentation_spaces(line, tab_size)
            if (
                indentation_spaces_amount > tab_size * max_indentation_level
                # make sure it's not a line continuation
                and indentation_spaces_amount - previous_line_indent == tab_size
            ):
                return parsed_file.get_name_with_line(line_number)
            previous_line_indent = indentation_spaces_amount
