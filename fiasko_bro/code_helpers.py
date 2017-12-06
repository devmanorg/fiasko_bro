import pep8
import ast

from mccabe import _read, PathGraphingAstVisitor


def count_pep8_violations(repository_info):
    pep8style = pep8.StyleGuide(quiet=True)
    result = pep8style.check_files(repository_info.get_python_file_filenames())
    return result.total_errors


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
