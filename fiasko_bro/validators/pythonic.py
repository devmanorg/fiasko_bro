import ast

from ..utils import ast_nodes_validators
from ..utils import ast_helpers, code_helpers, url_helpers
from ..i18n import _


def too_many_pep8_violations(
    project_folder,
    allowed_max_pep8_violations,
    max_pep8_line_length,
    pep8_paths_to_ignore,
    *args,
    **kwargs
):
    violations_amount = code_helpers.count_pep8_violations(
        project_folder,
        max_line_length=max_pep8_line_length,
        path_whitelist=pep8_paths_to_ignore
    )
    if violations_amount > allowed_max_pep8_violations:
        return _('%s PEP8 violations') % violations_amount


def range_starting_from_zero(project_folder, *args, **kwargs):
    for parsed_file in project_folder.get_parsed_py_files():
        calls = ast_helpers.get_nodes_of_type(parsed_file.ast_tree, ast.Call)
        for call in calls:
            if (
                getattr(call.func, 'id', None) == 'range' and call.args and
                len(call.args) == 2 and isinstance(call.args[0], ast.Num) and
                call.args[0].n == 0
            ):
                return parsed_file.get_name_with_line(call.lineno)


def except_block_class_too_broad(project_folder, *args, **kwargs):
    exception_type_to_catch = 'Exception'
    for parsed_file in project_folder.get_parsed_py_files():
        tryes = [node for node in ast.walk(parsed_file.ast_tree) if isinstance(node, ast.ExceptHandler)]
        for try_except in tryes:
            if try_except.type is None:
                return ''
            if (
                isinstance(try_except.type, ast.Name) and
                try_except.type.id == exception_type_to_catch
            ):
                message = _(
                    '%s class is too broad; use a more specific exception type'
                ) % exception_type_to_catch
                return message


def variable_assignment_with_lambda(project_folder, *args, **kwargs):
    for parsed_file in project_folder.get_parsed_py_files():
        assigns = ast_helpers.get_nodes_of_type(parsed_file.ast_tree, ast.Assign)
        for assign in assigns:
            if isinstance(assign.value, ast.Lambda):
                return '{}:{}'.format(parsed_file.name, assign.lineno)


def urls_with_hardcoded_get_parameters(project_folder, *args, **kwargs):
    for parsed_file in project_folder.get_parsed_py_files():
        string_nodes = [n for n in ast.walk(parsed_file.ast_tree) if isinstance(n, ast.Str)]
        for string_node in string_nodes:
            if url_helpers.is_url_with_params(string_node.s):
                return '{}:{}'.format(parsed_file.name, string_node.lineno)


def nonpythonic_empty_list_validation(project_folder, *args, **kwargs):
    for parsed_file in project_folder.get_parsed_py_files():
        ifs_compare_tests = [n.test for n in ast.walk(parsed_file.ast_tree) if
                             isinstance(n, ast.If) and isinstance(n.test, ast.Compare)]
        for compare in ifs_compare_tests:
            if ast_nodes_validators.is_len_compared_to_zero(compare):
                return parsed_file.get_name_with_line(compare.lineno)


def exit_call_in_function(project_folder, functions_allowed_to_have_exit_calls, *args, **kwargs):
    for parsed_file in project_folder.get_parsed_py_files():
        defs = ast_helpers.get_nodes_of_type(parsed_file.ast_tree, ast.FunctionDef)
        for function_definition in defs:
            if function_definition.name in functions_allowed_to_have_exit_calls:
                continue
            if ast_helpers.has_exit_calls(function_definition):
                return function_definition.name


def validates_response_status_by_comparing_to_200(project_folder, *args, **kwargs):
    for parsed_file in project_folder.get_parsed_py_files():
        for compare in ast_helpers.get_nodes_of_type(parsed_file.ast_tree, ast.Compare):
            if ast_nodes_validators.is_status_code_compared_to_200(compare):
                return parsed_file.get_name_with_line(compare.lineno)


def mutable_default_arguments(project_folder, *args, **kwargs):
    funcdef_types = (ast.FunctionDef, )
    mutable_types = (ast.List, ast.Dict)
    for parsed_file in project_folder.get_parsed_py_files():
        for funcdef in ast_helpers.get_nodes_of_type(parsed_file.ast_tree, funcdef_types):
            if ast_helpers.is_funcdef_has_arguments_of_types(funcdef, mutable_types):
                return parsed_file.get_name_with_line(funcdef.lineno)


def slice_starts_from_zero(project_folder, *args, **kwargs):
    for parsed_file in project_folder.get_parsed_py_files():
        if ast_helpers.is_tree_has_slices_from_zero(parsed_file.ast_tree):
            return parsed_file.name


def casts_input_result_to_str(project_folder, *args, **kwargs):
    for parsed_file in project_folder.get_parsed_py_files():
        calls = ast_helpers.get_nodes_of_type(parsed_file.ast_tree, ast.Call)
        for call in calls:
            if ast_helpers.is_str_call_of_input(call):
                return parsed_file.get_name_with_line(call.lineno)


def string_literal_sum(project_folder, *args, **kwargs):
    for parsed_file in project_folder.get_parsed_py_files():
        for node in ast.walk(parsed_file.ast_tree):
            if (
                    isinstance(node, ast.BinOp) and
                    isinstance(node.op, ast.Add) and
                    isinstance(node.left, ast.Str) and
                    isinstance(node.right, ast.Str)
               ):
                    return parsed_file.get_name_with_line(node.lineno)


def call_with_constants(project_folder, valid_calls_with_constants, *args, **kwargs):
    for parsed_file in project_folder.get_parsed_py_files():
        if 'tests' in parsed_file.path:  # tests can have constants in asserts
            continue
        calls = ast_helpers.get_nodes_of_type(parsed_file.ast_tree, ast.Call)
        for call in calls:
            if ast_helpers.is_call_has_constants(call, valid_calls_with_constants):
                return '{}:{}'.format(parsed_file.name, call.lineno)
