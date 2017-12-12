import ast
import builtins
import os
import re

from . import ast_helpers
from . import code_helpers
from . import list_helpers
from . import url_helpers


def has_more_commits_than_origin(solution_repo, original_repo=None, *args, **kwargs):
    if not original_repo:
        return
    # FIXME this check works incorrectly in case of new commit in original repo after student forked it
    if solution_repo.count_commits() <= original_repo.count_commits():
        return 'no_new_code', None


def has_readme_file(solution_repo, readme_filename, *args, **kwargs):
    if not solution_repo.does_file_exist(readme_filename):
        return 'need_readme', 'нет %s' % readme_filename


def is_pep8_fine(solution_repo, allowed_max_pep8_violations, *args, **kwargs):
    violations_amount = code_helpers.count_pep8_violations(solution_repo)
    if violations_amount > allowed_max_pep8_violations:
        return 'pep8', '%s нарушений' % violations_amount


def has_changed_readme(solution_repo, readme_filename, original_repo=None, *args, **kwargs):
    if not original_repo:
        return
    original_readme_path = os.path.join(original_repo.path, readme_filename)
    solution_readme_path = os.path.join(solution_repo.path, readme_filename)
    try:
        with open(original_readme_path, encoding='utf-8') as original_handler:
            original_readme = original_handler.read()
    except FileNotFoundError:
        return
    try:
        with open(solution_readme_path, encoding='utf-8') as solution_handler:
            solution_readme = solution_handler.read()
        if solution_readme == original_readme:
            return 'need_readme', None
    except UnicodeDecodeError:
        return 'readme_not_utf_8', None


def has_no_syntax_errors(solution_repo, *args, **kwargs):
    for filename, tree in solution_repo.get_ast_trees(with_filenames=True):
        if tree is None:
            return 'syntax_error', 'в %s' % filename


def are_sources_in_utf(solution_repo, *args, **kwargs):
    try:
        solution_repo.get_ast_trees(with_filenames=True)
        solution_repo.get_file('requirements.txt')
    except UnicodeDecodeError:
        return 'sources_not_utf_8', None


def is_snake_case(solution_repo, whitelists, *args, **kwargs):
    whitelist = whitelists.get('is_snake_case', [])
    buildins_ = dir(builtins)
    for tree in solution_repo.get_ast_trees():
        names = ast_helpers.get_all_names_from_tree(tree)
        imported_names = ast_helpers.get_all_imported_names_from_tree(tree)
        defined_class_names = ast_helpers.get_all_class_definitions_from_tree(tree)
        namedtuples = ast_helpers.get_all_namedtuple_names(tree)
        names_with_uppercase = [n for n in names
                                if n.lower() != n and n.upper() != n
                                and n not in imported_names
                                and n not in defined_class_names
                                and n not in namedtuples
                                and n not in buildins_
                                and n not in whitelist]
        if names_with_uppercase:
            return 'camel_case_vars', 'переименуй, например, %s.' % ', '.join(names_with_uppercase[:3])


def is_mccabe_difficulty_ok(solution_repo, max_complexity, *args, **kwargs):
    violations = []
    for filename, _ in solution_repo.get_ast_trees(with_filenames=True):
        violations += code_helpers.get_mccabe_violations_for_file(filename, max_complexity)
    if violations:
        return 'mccabe_failure', ','.join(violations)


def has_no_encoding_declaration(solution_repo, *args, **kwargs):
    for _, file_content, _ in solution_repo.get_ast_trees(with_filenames=True, with_file_content=True):
        first_line = file_content.strip('\n').split('\n')[0].strip().replace(' ', '')
        if first_line.startswith('#') and 'coding:utf-8' in first_line:
            return 'has_encoding_declarations', ''


def has_no_star_imports(solution_repo, *args, **kwargs):
    for tree in solution_repo.get_ast_trees():
        if ast_helpers.is_tree_has_star_imports(tree):
            return 'has_star_import', ''


def has_no_local_imports(solution_repo, *args, **kwargs):
    for tree in solution_repo.get_ast_trees():
        if ast_helpers.is_has_local_imports(tree):
            return 'has_local_import', ''


def has_local_var_named_as_global(solution_repo, *args, **kwargs):
    for tree in solution_repo.get_ast_trees():
        bad_names = ast_helpers.get_local_vars_named_as_globals(tree)
        if bad_names:
            return 'has_locals_named_as_globals', 'например, %s' % (', '.join(bad_names))


def has_variables_from_blacklist(solution_repo, blacklists, *args, **kwargs):
    blacklist = blacklists.get('has_variables_from_blacklist', [])
    for tree in solution_repo.get_ast_trees():
        names = ast_helpers.get_all_defined_names(tree)
        bad_names = names.intersection(blacklist)
        if bad_names:
            return 'bad_titles', ', '.join(bad_names)


def has_no_short_variable_names(solution_repo, minimum_name_length, whitelists, *args, **kwargs):
    whitelist = whitelists.get('has_no_short_variable_names', [])
    short_names = []
    for tree in solution_repo.get_ast_trees():
        names = ast_helpers.get_all_defined_names(tree)
        short_names += [n for n in names if len(n) < minimum_name_length and n not in whitelist]
    if short_names:
        return 'bad_titles', ', '.join(list(set(short_names)))


def are_tabs_used_for_indentation(solution_repo, *args, **kwargs):
    for filepath, file_content, _ in solution_repo.get_ast_trees(with_filenames=True, with_file_content=True):
        lines = [l for l in file_content.split('\n') if l]
        tabbed_lines_amount = len([l for l in lines if l.startswith('\t')])
        _, ext = os.path.splitext(filepath)
        is_frontend = ext in ('.html', '.css', '.js')
        if ext == '.py':
            # строки могут начинаться с таба в многострочной строке, поэтому такая эвристика
            if tabbed_lines_amount > len(lines) / 2:
                return 'tabs_used_for_indents', ''
        elif is_frontend and tabbed_lines_amount:
            return 'tabs_used_for_indents', ''


def has_no_try_without_exception(solution_repo, *args, **kwargs):
    exception_type_to_catch = 'Exception'
    for tree in solution_repo.get_ast_trees():
        tryes = [node for node in ast.walk(tree) if isinstance(node, ast.ExceptHandler)]
        for try_except in tryes:
            if try_except.type is None:
                return 'broad_except', ''
            if isinstance(try_except.type, ast.Name) and try_except.type.id == exception_type_to_catch:
                return 'broad_except', '%s – слишком широкий тип исключений; укажи подробнее, какую ошибку ты ловишь' % exception_type_to_catch


def has_frozen_requirements(solution_repo, *args, **kwargs):
    requirements = solution_repo.get_file('requirements.txt')
    if not requirements:
        return
    for requirement_line in requirements.split('\n'):
        if requirement_line and '==' not in requirement_line:
            return 'unfrozen_requirements', 'например, %s' % requirement_line


def has_no_directories_from_blacklist(solution_repo, blacklists, *args, **kwargs):
    blacklist = blacklists.get('has_no_directories_from_blacklist', [])
    for dirname in blacklist:
        if solution_repo.does_directory_exist(dirname):
            return 'data_in_repo', ''


def has_no_vars_with_lambda(solution_repo, *args, **kwargs):
    for tree in solution_repo.get_ast_trees():
        assigns = [n for n in ast.walk(tree) if isinstance(n, ast.Assign)]
        for assign in assigns:
            if isinstance(assign.value, ast.Lambda):
                return 'named_lambda', ''


def has_no_calls_with_constants(solution_repo, whitelists, *args, **kwargs):
    whitelist = whitelists.get('has_no_calls_with_constants')
    for filepath, tree in solution_repo.get_ast_trees(with_filenames=True):
        if 'tests' in filepath:  # tests can have constants in asserts
            continue
        calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)]
        for call in calls:
            if isinstance(ast_helpers.get_closest_definition(call), ast.ClassDef):  # for case of id = db.String(256)
                continue
            attr_to_get_name = 'id' if hasattr(call.func, 'id') else 'attr'
            function_name = getattr(call.func, attr_to_get_name, None)
            if not function_name or function_name in whitelist:
                continue
            for arg in call.args:
                if isinstance(arg, ast.Num):
                    return 'magic_numbers', 'например, %s' % arg.n


def has_readme_in_single_language(solution_repo, readme_filename, min_percent_of_another_language, *args, **kwargs):
    raw_readme = solution_repo.get_file(readme_filename)
    readme_no_code = re.sub("```[#!a-z]*\n[\s\S]*?\n```", '', raw_readme)
    clean_readme = re.sub("\[([^\]]+)\]\(([^)]+)\)", '', readme_no_code)
    ru_letters_amount = len(re.findall('[а-яА-Я]', clean_readme))
    en_letters_amount = len(re.findall('[a-zA-Z]', clean_readme))
    if not (ru_letters_amount + en_letters_amount):
        return
    another_language_percent = min([ru_letters_amount, en_letters_amount]) / (ru_letters_amount + en_letters_amount) * 100
    if another_language_percent > min_percent_of_another_language:
        return 'bilingual_readme', ''


def has_no_range_from_zero(solution_repo, *args, **kwargs):
    for tree in solution_repo.get_ast_trees():
        calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)]
        for call in calls:
            if getattr(call.func, 'id', None) == 'range' and call.args and len(call.args) == 2 and isinstance(call.args[0], ast.Num) and call.args[0].n == 0:
                return 'manual_zero_in_range', ''


def has_no_urls_with_hardcoded_arguments(solution_repo, *args, **kwargs):
    for tree in solution_repo.get_ast_trees():
        strings = [n.s for n in ast.walk(tree) if isinstance(n, ast.Str)]
        for string in strings:
            if url_helpers.is_url_with_params(string):
                return 'hardcoded_get_params', ''


def has_no_nonpythonic_empty_list_validations(solution_repo, *args, **kwargs):
    for tree in solution_repo.get_ast_trees():
        ifs_compare_tests = [n.test for n in ast.walk(tree) if
                             isinstance(n, ast.If) and isinstance(n.test, ast.Compare)]
        for compare in ifs_compare_tests:
            # validates if `len(s) >/== 0` pattern
            if (len(compare.ops) == 1 and
                isinstance(compare.left, ast.Call) and
                hasattr(compare.left, 'func') and
                hasattr(compare.left.func, 'id') and
                compare.left.func.id == 'len' and
                isinstance(compare.ops[0], (ast.Gt, ast.Eq)) and
                isinstance(compare.comparators[0], ast.Num) and
                compare.comparators[0].n == 0
            ):
                return 'nonpythonic_empty_list_validation', ''


def has_no_extra_dockstrings(solution_repo, functions_with_docstrings_percent_limit, *args, **kwargs):
    for tree in solution_repo.get_ast_trees():
        defs = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        if not defs:
            continue

        docstrings = [ast.get_docstring(d) for d in defs if ast.get_docstring(d) is not None]
        if len(docstrings) / len(defs) * 100 > functions_with_docstrings_percent_limit:
            return 'extra_comments', ''


def has_no_commit_messages_from_blacklist(solution_repo, blacklists, last_commits_to_check_amount, *args, **kwargs):
    blacklist = blacklists.get('has_no_commit_messages_from_blacklist', [])
    for commit in solution_repo.iter_commits('master', max_count=last_commits_to_check_amount):
        message = commit.message.lower().strip().strip('.\'"')
        if message in blacklist:
            return 'git_history_warning', ''


def has_no_libs_from_stdlib_in_requirements(solution_repo, *args, **kwargs):
    package_version_delimiters = {'<', '>', '==', '<=', '>='}
    stdlibs_list = list_helpers.get_stdlibs_list()
    raw_requirements = solution_repo.get_file('requirements.txt')
    if not raw_requirements:
        return

    stdlib_packages_in_requirements = []
    for requirement in raw_requirements.split('\n'):
        package_name = None
        for delimiter in package_version_delimiters:
            if delimiter in requirement:
                package_name = requirement.split(delimiter)[0]
        if not package_name:
            package_name = requirement
        if package_name in stdlibs_list:
            stdlib_packages_in_requirements.append(package_name)

    if stdlib_packages_in_requirements:
        return 'stdlib_in_requirements', ', '.join(stdlib_packages_in_requirements)


def has_no_exit_calls_in_functions(solution_repo, whitelists, *args, **kwargs):
    whitelist = whitelists.get('has_no_exit_calls_in_functions', [])
    for tree in solution_repo.get_ast_trees():
        defs = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        for function_definition in defs:
            if function_definition.name in whitelist:
                continue
            calls = [c for c in ast.walk(function_definition) if isinstance(c, ast.Call) and hasattr(c, 'func')]
            has_exit_calls = any([c.func.id == 'exit' for c in calls if isinstance(c.func, ast.Name)])
            has_sys_exit_calls = any([hasattr(c.func.value, 'id') and c.func.value.id == 'sys' and c.func.attr == 'exit' for c in calls if isinstance(c.func, ast.Attribute)])
            if has_exit_calls or has_sys_exit_calls:
                return 'has_exit_calls_in_function', function_definition.name


def has_no_bom(solution_repo, *args, **kwargs):
    bom = '\ufeff'
    for _, file_content, _ in solution_repo.get_ast_trees(with_filenames=True, with_file_content=True):
        if file_content.startswith(bom):
            return 'has_bom', ''

    requirements = solution_repo.get_file('requirements.txt')
    if requirements and requirements.startswith(bom):
        return 'has_bom', ''


def has_indents_of_spaces(solution_repo, tab_size, *args, **kwargs):
    """
        Иногда при парсинге дерева col_offset считается неправильно,
        так что эта проверка может быть только предупреждением.
    """
    node_types_to_validate = (ast.For, ast.If, ast.FunctionDef, ast.With)
    for _, file_content, tree in solution_repo.get_ast_trees(with_filenames=True, with_file_content=True):
        lines_offsets = [None]
        for line in file_content.split('\n'):
            lines_offsets.append(len(line) - len(line.lstrip(' ')))
        for node in ast.walk(tree):
            if not hasattr(node, 'parent'):
                continue
            node_line = getattr(node, 'lineno', None)
            parent_line = getattr(node.parent, 'lineno', None)
            if node_line is None or parent_line is None:
                continue
            node_offset = lines_offsets[node_line]
            parent_offset = lines_offsets[parent_line]
            if (
                node_line != parent_line and node_offset > parent_offset and
                node_offset - parent_offset != tab_size and isinstance(node.parent, node_types_to_validate)
            ):
                return 'indent_not_four_spaces', 'например, строка %s' % node.lineno


def has_no_lines_ends_with_semicolon(solution_repo, *args, **kwargs):
    for _, file_content, tree in solution_repo.get_ast_trees(with_filenames=True, with_file_content=True):
        total_lines_with_semicolons = len([1 for l in file_content.split('\n') if l.endswith(';') and not l.startswith('#')])
        # TODO: check docstrings for semicolons
        string_nodes = [n for n in ast.walk(tree) if isinstance(n, ast.Str)]
        semicolons_in_string_constants_amount = sum([n.s.count(';') for n in string_nodes])
        if total_lines_with_semicolons > semicolons_in_string_constants_amount:
            return 'has_semicolons', ''


def not_validates_response_status_by_comparing_to_200(solution_repo, *args, **kwargs):
    for tree in solution_repo.get_ast_trees():
        for compare in [n for n in ast.walk(tree) if isinstance(n, ast.Compare)]:
            # validates blah.status_code == 200
            if (len(compare.ops) != 1 or not isinstance(compare.ops[0], ast.Eq)
                or len(compare.comparators) != 1 or not isinstance(compare.comparators[0], ast.Num)
                or compare.comparators[0].n != 200
                or not isinstance(compare.left, ast.Attribute)
                or compare.left.attr != 'status_code'
            ):
                continue
            return 'compare_response_status_to_200', ''


def has_no_mutable_default_arguments(solution_repo, *args, **kwargs):
    funcdef_types = (ast.FunctionDef, )
    mutable_types = (ast.List, ast.Dict)
    for tree in solution_repo.get_ast_trees():
        for funcdef in [n for n in ast.walk(tree) if isinstance(n, funcdef_types)]:
            for default in getattr(funcdef.args, 'defaults', []):
                if isinstance(default, mutable_types):
                    return 'mutable_default_arguments', ''


def has_no_slices_starts_from_zero(solution_repo, *args, **kwargs):
    for tree in solution_repo.get_ast_trees():
        for slice in [n for n in ast.walk(tree) if isinstance(n, ast.Slice)]:
            if slice.step is None and isinstance(slice.lower, ast.Num) and slice.lower.n == 0:
                return 'slice_starts_from_zero', ''


def has_no_variables_that_shadow_default_names(solution_repo, *args, **kwargs):
    buildins_ = dir(builtins)
    for tree in solution_repo.get_ast_trees():
        names = ast_helpers.get_all_defined_names(
            tree,
            include_class_attributes=False
        )
        bad_names = names.intersection(buildins_)
        if bad_names:
            return 'title_shadows', ', '.join(bad_names)


def has_no_return_with_parenthesis(solution_repo, *args, **kwargs):
    for _, file_content, tree in solution_repo.get_ast_trees(with_filenames=True, with_file_content=True):
        file_content = file_content.split('\n')
        return_lines = [n.lineno for n in ast.walk(tree) if isinstance(n, ast.Return)]
        for line_num in return_lines:
            line = file_content[line_num - 1]
            if line.count('return') == 1 and 'return(' in line or 'return (' in line:
                return 'return_with_parenthesis', 'строка %s' % line_num


def has_no_cast_input_result_to_str(solution_repo, *args, **kwargs):
    for tree in solution_repo.get_ast_trees():
        calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)]
        for call in calls:
            function_name = getattr(call.func, 'id', None)
            if not hasattr(call, 'parent') or not hasattr(call.parent, 'func'):
                continue
            parent_function_name = getattr(call.parent.func, 'id', None)
            if function_name == 'input' and parent_function_name == 'str':
                return 'str_conversion_of_input_result', ''
