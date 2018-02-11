from .. import list_helpers
from ..i18n import _


def has_frozen_requirements(solution_repo, *args, **kwargs):
    requirements = solution_repo.get_file('requirements.txt')
    if not requirements:
        return
    for requirement_line in requirements.split('\n'):
        if requirement_line and '==' not in requirement_line:
            return 'unfrozen_requirements', _('for example, %s') % requirement_line


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
