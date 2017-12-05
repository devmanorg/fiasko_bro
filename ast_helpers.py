import ast
import os
import re

from helpers import flat
from mccabe import _read, PathGraphingAstVisitor


def get_all_names_from_tree(tree):
    return list({node.id for node in ast.walk(tree) if isinstance(node, ast.Name)})


def get_all_namedtuple_names(tree):
    nametuples_names = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        if not isinstance(node.value, ast.Call):
            continue
        if hasattr(node.value.func, 'id') and node.value.func.id == 'namedtuple':
            nametuples_names.append(node.targets[0].id)
    return nametuples_names


def get_all_imported_names_from_tree(tree):
    imported_names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            for name in node.names:
                imported_name = name.asname or name.name
                imported_names.append(imported_name)
    return set(imported_names)


def get_all_class_definitions_from_tree(tree):
    return {node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)}


def get_mccabe_violations_for_file(filepath, max_complexity):
    code = _read(filepath)
    tree = compile(code, filepath, "exec", ast.PyCF_ONLY_AST)
    visitor = PathGraphingAstVisitor()
    visitor.preorder(tree, visitor)

    violations = []
    for graph in visitor.graphs.values():
        if graph.complexity() >= max_complexity:
            complex_function_name = graph.entity
            if complex_function_name.startswith('If '):
                complex_function_name = 'if __name__ == "__main__"'
            violations.append(complex_function_name)
    return violations


def is_tree_has_star_imports(tree):
    import_names = [node.names[0].name for node in ast.walk(tree)
                    if isinstance(node, ast.ImportFrom) and node.names]
    return '*' in import_names


def is_has_local_imports(tree):
    imports = [n for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) or isinstance(n, ast.Import)]
    for import_node in imports:
        if not import_node.col_offset:
            continue
        if isinstance(import_node.parent, ast.If) and not import_node.parent.col_offset:
            continue
        return True
    return False


def get_assigned_vars(tree, names_only=True):
    assigned_items = flat([n.targets for n in ast.walk(tree) if isinstance(n, ast.Assign)])
    if names_only:
        return {getattr(n, 'id', None) for n in assigned_items if n.col_offset > 0}
    else:
        return assigned_items


def get_iter_vars_from_for_loops(tree):
    for_nodes = [n for n in ast.walk(tree) if isinstance(n, ast.For) or isinstance(n, ast.comprehension)]
    try:
        iter_var_names = {n.target.id for n in for_nodes}
    except AttributeError:
        iter_var_names = {}
    return iter_var_names


def get_defined_function_names(tree):
    return {n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}


def get_local_vars_named_as_globals(tree):
    assigned_items = get_assigned_vars(tree, names_only=False)
    nonglobal_names = [getattr(n, 'id', None) for n in assigned_items if n.col_offset > 0]
    return [n for n in nonglobal_names if n and re.search('[a-zA-Z]', n) and n.upper() == n]


def get_vars_from_fuction_definitions(tree):
    func_defs = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    arg_names = flat([[a.arg for a in fd.args.args]for fd in func_defs])
    return set(arg_names)


def uses_module(tree, module_name):
    imports = [node for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) or isinstance(node, ast.Import)]
    for _import in imports:
        imported_names = [n.name for n in _import.names]
        import_from = getattr(_import, 'module', None)
        if import_from == module_name or module_name in imported_names:
            return True
    return False


def find_method_calls(tree, attr_name):
    attributes = [node for node in ast.walk(tree) if isinstance(node, ast.Attribute)]
    return attr_name in {a.attr for a in attributes}


def get_all_defined_names(tree):
    names = get_assigned_vars(tree)
    names.update(get_iter_vars_from_for_loops(tree))
    names.update(get_vars_from_fuction_definitions(tree))
    names.update(get_defined_function_names(tree))  # TODO: добавить классы и методы в проверку
    return set([n for n in names if n])


def get_closest_definition(node):
    definitions_classes = ast.ClassDef, ast.FunctionDef
    current_node = node
    while hasattr(current_node, 'parent'):
        if isinstance(current_node, definitions_classes):
            return current_node
        current_node = current_node.parent
