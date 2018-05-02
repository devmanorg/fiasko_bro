from ..utils import list_helpers
from ..i18n import _


def requirements_not_frozen(project_folder, *args, **kwargs):
    requirements = project_folder.get_file('requirements.txt')
    if not requirements:
        return
    for requirement_line in requirements.split('\n'):
        if requirement_line and '==' not in requirement_line:
            return _('for example, %s') % requirement_line


def has_libs_from_stdlib_in_requirements(project_folder, *args, **kwargs):
    raw_requirements = project_folder.get_file('requirements.txt')
    if not raw_requirements:
        return

    stdlib_packages_in_requirements = []
    for requirement in raw_requirements.split('\n'):
        if _is_stdlib_requirement(requirement):
            stdlib_packages_in_requirements.append(requirement)

    if stdlib_packages_in_requirements:
        return ', '.join(stdlib_packages_in_requirements)


def _is_stdlib_requirement(raw_requirement_line):
    package_version_delimiters = {'<', '>', '==', '<=', '>='}
    stdlibs_list = list_helpers.get_stdlibs_list()

    package_name = None
    for delimiter in package_version_delimiters:
        if delimiter in raw_requirement_line:
            package_name = raw_requirement_line.split(delimiter)[0]
    if not package_name:
        package_name = raw_requirement_line
    return package_name in stdlibs_list
