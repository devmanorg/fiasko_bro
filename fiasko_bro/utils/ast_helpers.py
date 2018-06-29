import ast
import re
from itertools import filterfalse

from .list_helpers import flat


def get_nodes_of_type(root_node, type_or_types):
    return [n for n in ast.walk(root_node) if isinstance(n, type_or_types)]


def get_unique_node_names_of_types(root_node, type_or_types):
    return {node.name for node in ast.walk(root_node) if isinstance(node, type_or_types)}


def get_all_imports(root):
    return get_nodes_of_type(root, (ast.ImportFrom, ast.Import))


def get_all_names_from_tree(tree):
    if tree is None:
        return []
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


def get_all_import_names_mentioned_in_import(tree):
    import_names = []
    imports = get_all_imports(tree)
    for import_node in imports:
        if isinstance(import_node, ast.ImportFrom):
            import_names.append(import_node.module)
        elif isinstance(import_node, ast.Import):
            import_names += [import_object.name for import_object in import_node.names]
    return import_names


def is_multiple_imports_on_one_line(node):
    return isinstance(node, ast.Import) and len(node.names) > 1


def get_all_imported_names_from_tree(tree):
    imported_names = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.ImportFrom):
            continue
        for name in node.names:
            imported_name = name.asname or name.name
            imported_names.append(imported_name)
    return set(imported_names)


def get_all_class_definitions_from_tree(tree):
    return get_unique_node_names_of_types(tree, ast.ClassDef)


def is_tree_has_star_imports(tree):
    import_names = [node.names[0].name for node in ast.walk(tree)
                    if isinstance(node, ast.ImportFrom) and node.names]
    return '*' in import_names


def is_has_local_imports(tree):
    imports = get_all_imports(tree)
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
    for_nodes = get_nodes_of_type(tree, (ast.For, ast.comprehension))
    try:
        iter_var_names = {n.target.id for n in for_nodes}
    except AttributeError:
        iter_var_names = {}
    return iter_var_names


def get_defined_function_names(tree):
    return get_unique_node_names_of_types(tree, ast.FunctionDef)


def get_nonglobal_items_from_assigned_items(assigned_items, potentially_bad_names, max_depth):
    nonglobal_items = []
    for assigned_item in assigned_items:
        if getattr(assigned_item, 'id', None) not in potentially_bad_names:
            continue
        if is_nonglobal_item(assigned_item, max_depth):
            nonglobal_items.append(assigned_item.id)
    return nonglobal_items


def is_nonglobal_item(node, max_indentation_depth):
    current_item = node
    # prevents the user from making this loop excessively long
    for _ in range(max_indentation_depth):
        if (
                not hasattr(current_item, 'parent') or
                isinstance(current_item.parent, ast.Module)
        ):
            break
        if not isinstance(current_item.parent, (ast.ClassDef, ast.Assign, ast.If)):
            return True
        current_item = current_item.parent
    return False


def get_local_vars_named_as_globals(tree, max_indentation_depth):
    assigned_items = get_assigned_vars(tree, names_only=False)
    nonglobal_names = [getattr(n, 'id', None) for n in assigned_items if n.col_offset > 0]
    potentially_bad_names = [n for n in nonglobal_names
                             if n and re.search('[a-zA-Z]', n) and n.upper() == n]
    local_vars_named_as_globals = get_nonglobal_items_from_assigned_items(
        assigned_items,
        potentially_bad_names,
        max_indentation_depth
    )
    return local_vars_named_as_globals


def get_vars_from_fuction_definitions(tree):
    func_defs = get_nodes_of_type(tree, ast.FunctionDef)
    arg_names = flat([[a.arg for a in fd.args.args]for fd in func_defs])
    return set(arg_names)


def uses_module(tree, module_name):
    imports = get_all_imports(tree)
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
    names.update(get_defined_function_names(tree))  # TODO: add class and methods names
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
    for assignment in get_nodes_of_type(tree, ast.Assign):
        base_assign_value_name = get_base_assign_value_name(assignment.value)
        if base_assign_value_name in right_assignment_whitelist:
            result_names += [t.id for t in assignment.targets]
    return result_names


def is_call_has_constants(call, caller_whitelist):
    if isinstance(get_closest_definition(call), ast.ClassDef):
        return False  # for case of id = db.String(256)
    attr_to_get_name = 'id' if hasattr(call.func, 'id') else 'attr'
    function_name = getattr(call.func, attr_to_get_name, None)
    if not function_name or function_name in caller_whitelist:
        return False
    for arg in call.args:
        if isinstance(arg, ast.Num):
            return True
    return False


def is_node_offset_fine(node, lines_offsets, node_types_to_validate, tab_size):
    if not hasattr(node, 'parent'):
        return True
    node_line = getattr(node, 'lineno', None)
    parent_line = getattr(node.parent, 'lineno', None)
    if node_line is None or parent_line is None:
        return True
    node_offset = lines_offsets[node_line]
    parent_offset = lines_offsets[parent_line]
    return not (
        node_line != parent_line and node_offset > parent_offset and
        node_offset - parent_offset != tab_size and
        isinstance(node.parent, node_types_to_validate)
    )


def has_exit_calls(function_definition):
    calls = [c for c in ast.walk(function_definition)
             if isinstance(c, ast.Call) and hasattr(c, 'func')]
    has_plain_exit_calls = any(
        [c.func.id == 'exit' for c in calls if isinstance(c.func, ast.Name)]
    )
    has_sys_exit_calls = any(
        [hasattr(c.func.value, 'id') and
         c.func.value.id == 'sys' and
         c.func.attr == 'exit' for c in calls if isinstance(c.func, ast.Attribute)]
    )
    return has_plain_exit_calls or has_sys_exit_calls


def is_str_call_of_input(call):
    function_name = getattr(call.func, 'id', None)
    if not hasattr(call, 'parent') or not hasattr(call.parent, 'func'):
        return False
    parent_function_name = getattr(call.parent.func, 'id', None)
    if function_name == 'input' and parent_function_name == 'str':
        return True
    return False


def is_funcdef_has_arguments_of_types(funcdef, mutable_types):
    for default in getattr(funcdef.args, 'defaults', []):
        if isinstance(default, mutable_types):
            return True
    return False


def is_tree_has_slices_from_zero(tree):
    for slice in get_nodes_of_type(tree, ast.Slice):
        if slice.step is None and isinstance(slice.lower, ast.Num) and slice.lower.n == 0:
            return True
    return False
