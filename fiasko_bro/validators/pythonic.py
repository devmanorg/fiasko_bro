import ast

from .. import ast_nodes_validators
from .. import ast_helpers
from .. import code_helpers
from .. import url_helpers
from ..i18n import _


def is_pep8_fine(solution_repo, allowed_max_pep8_violations,
                 max_pep8_line_length, whitelists, *args, **kwargs):
    whitelist = whitelists.get('is_pep8_fine', [])
    violations_amount = code_helpers.count_pep8_violations(
        solution_repo,
        max_line_length=max_pep8_line_length,
        path_whitelist=whitelist
    )
    if violations_amount > allowed_max_pep8_violations:
        return 'pep8', _('%s PEP8 violations') % violations_amount


def has_no_range_from_zero(solution_repo, *args, **kwargs):
    for tree in solution_repo.get_ast_trees():
        calls = ast_helpers.get_nodes_of_type(tree, ast.Call)
        for call in calls:
            if (
                getattr(call.func, 'id', None) == 'range' and call.args and
                len(call.args) == 2 and isinstance(call.args[0], ast.Num) and
                call.args[0].n == 0
            ):
                return 'manual_zero_in_range', ''


def has_no_try_without_exception(solution_repo, *args, **kwargs):
    exception_type_to_catch = 'Exception'
    for tree in solution_repo.get_ast_trees():
        tryes = [node for node in ast.walk(tree) if isinstance(node, ast.ExceptHandler)]
        for try_except in tryes:
            if try_except.type is None:
                return 'broad_except', ''
            if (
                isinstance(try_except.type, ast.Name) and
                try_except.type.id == exception_type_to_catch
            ):
                message = _(
                    '%s class is too broad; use a more specific exception type'
                ) % exception_type_to_catch
                return 'broad_except', message


def has_no_vars_with_lambda(solution_repo, *args, **kwargs):
    for tree in solution_repo.get_ast_trees():
        assigns = ast_helpers.get_nodes_of_type(tree, ast.Assign)
        for assign in assigns:
            if isinstance(assign.value, ast.Lambda):
                return 'named_lambda', ''


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
            if ast_nodes_validators.is_len_compared_to_zero(compare):
                return 'nonpythonic_empty_list_validation', ''


def has_no_exit_calls_in_functions(solution_repo, whitelists, *args, **kwargs):
    whitelist = whitelists.get('has_no_exit_calls_in_functions', [])
    for tree in solution_repo.get_ast_trees():
        defs = ast_helpers.get_nodes_of_type(tree, ast.FunctionDef)
        for function_definition in defs:
            if function_definition.name in whitelist:
                continue
            if ast_helpers.has_exit_calls(function_definition):
                return 'has_exit_calls_in_function', function_definition.name


def not_validates_response_status_by_comparing_to_200(solution_repo, *args, **kwargs):
    for tree in solution_repo.get_ast_trees():
        for compare in ast_helpers.get_nodes_of_type(tree, ast.Compare):
            if ast_nodes_validators.is_status_code_compared_to_200(compare):
                return 'compare_response_status_to_200', ''


def has_no_mutable_default_arguments(solution_repo, *args, **kwargs):
    funcdef_types = (ast.FunctionDef, )
    mutable_types = (ast.List, ast.Dict)
    for tree in solution_repo.get_ast_trees():
        for funcdef in ast_helpers.get_nodes_of_type(tree, funcdef_types):
            if ast_helpers.is_funcdef_has_arguments_of_types(funcdef, mutable_types):
                return 'mutable_default_arguments', ''


def has_no_slices_starts_from_zero(solution_repo, *args, **kwargs):
    for tree in solution_repo.get_ast_trees():
        if ast_helpers.is_tree_has_slices_from_zero(tree):
            return 'slice_starts_from_zero', ''


def has_no_cast_input_result_to_str(solution_repo, *args, **kwargs):
    for tree in solution_repo.get_ast_trees():
        calls = ast_helpers.get_nodes_of_type(tree, ast.Call)
        for call in calls:
            if ast_helpers.is_str_call_of_input(call):
                return 'str_conversion_of_input_result', ''


def has_no_string_literal_sums(solution_repo, *args, **kwargs):
    for file_path, tree in solution_repo.get_ast_trees(with_filenames=True):
        for node in ast.walk(tree):
            if (
                    isinstance(node, ast.BinOp) and
                    isinstance(node.op, ast.Add) and
                    isinstance(node.left, ast.Str) and
                    isinstance(node.right, ast.Str)
               ):
                    file_name = url_helpers.get_filename_from_path(file_path)
                    return 'has_string_sum', '{}: {}'.format(file_name, node.lineno)


def has_no_calls_with_constants(solution_repo, whitelists, *args, **kwargs):
    whitelist = whitelists.get('has_no_calls_with_constants')
    for filepath, tree in solution_repo.get_ast_trees(with_filenames=True):
        if 'tests' in filepath:  # tests can have constants in asserts
            continue
        calls = ast_helpers.get_nodes_of_type(tree, ast.Call)
        for call in calls:
            if ast_helpers.is_call_has_constants(call, whitelist):
                return 'magic_numbers', _('line %s') % call.lineno
