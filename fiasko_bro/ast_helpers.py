import ast
import re
from itertools import filterfalse

from .list_helpers import flat


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


def is_static_class_field(name_node):
    try:
        return isinstance(name_node.parent.parent, ast.ClassDef)
    except AttributeError:
        return False


def get_assigned_vars(tree, names_only=True, with_static_class_properties=True):
    assigned_items = flat([n.targets for n in ast.walk(tree) if isinstance(n, ast.Assign)])
    if not with_static_class_properties:
        assigned_items = [i for i in assigned_items if not is_static_class_field(i)]
    if names_only:
        return {getattr(n, 'id', None) for n in assigned_items if n.col_offset > 0}
    else:
        return assigned_items

def is_class_attribute(assigned_item):
    if not hasattr(assigned_item, 'parent'):
        return False
    if not hasattr(assigned_item.parent, 'parent'):
        return False
    return isinstance(assigned_item.parent.parent, ast.ClassDef)


def get_assigned_names_excluding_class_attributes(tree):
    assigned_items = get_assigned_vars(tree, names_only=False)
    return {
        getattr(node, 'id', None) for node in filterfalse(is_class_attribute, assigned_items)
    }


def get_iter_vars_from_for_loops(tree):
    for_nodes = [n for n in ast.walk(tree) if isinstance(n, ast.For) or isinstance(n, ast.comprehension)]
    try:
        iter_var_names = {n.target.id for n in for_nodes}
    except AttributeError:
        iter_var_names = {}
    return iter_var_names


def get_defined_function_names(tree):
    return {n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}


def get_local_vars_named_as_globals(tree, max_depth):
    assigned_items = get_assigned_vars(tree, names_only=False)
    nonglobal_names = [getattr(n, 'id', None) for n in assigned_items if n.col_offset > 0]
    local_vars_named_as_globals = []
    for assigned_item in assigned_items:
        if getattr(assigned_item, 'id', None) in nonglobal_names:
            current_item = assigned_item
            for _ in range(max_depth):  # prevents the user from making this loop excessively long
                if not hasattr(current_item, 'parent') or isinstance(current_item.parent, ast.Module):
                    break
                if not isinstance(current_item.parent, (ast.ClassDef, ast.Assign, ast.If)):
                    local_vars_named_as_globals.append(assigned_item.id)
                    break
                current_item = current_item.parent
    return [n for n in local_vars_named_as_globals if n and re.search('[a-zA-Z]', n) and n.upper() == n]


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


def get_all_defined_names(tree, with_static_class_properties=True):
    names = get_assigned_vars(tree, with_static_class_properties=with_static_class_properties)
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


def get_base_assign_value_name(node):
    """
        Base.foo().bar --> 'Base'
    """
    current_node = node
    while True:
        if isinstance(current_node, ast.Attribute):
            current_node = current_node.value
        elif isinstance(current_node, ast.Call):
            current_node = current_node.func
        else:
            break
    return getattr(current_node, 'id', None)


def get_names_from_assignment_with(tree, right_assignment_whitelist):
    result_names = []
    for assignment in [n for n in ast.walk(tree) if isinstance(n, ast.Assign)]:
        base_assign_value_name = get_base_assign_value_name(assignment.value)
        if base_assign_value_name in right_assignment_whitelist:
            result_names += [t.id for t in assignment.targets]
    return result_names
