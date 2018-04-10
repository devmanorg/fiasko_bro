from . import defaults
from .repository_info import ProjectFolder


def _is_successful_validation(validation_result):
    return not isinstance(validation_result, tuple)


def _run_validator_group(group, arguments):
    errors = []
    for validator in group:
        validation_result = validator(**arguments)
        if not _is_successful_validation(validation_result):
            errors.append(validation_result)
    return errors


def _run_validators_with_group_names(validator_groups, group_names, validator_arguments):
    errors = []
    for group_name in group_names:
        errors += _run_validator_group(
            validator_groups.get(group_name, []),
            validator_arguments
        )
    return errors


def run_validator_group(validator_group, validator_arguments, post_error_validator_group=None):
    successful_group_names = []
    for group_name, group in validator_group.items():
        errors = _run_validator_group(group, validator_arguments)
        if errors:
            if post_error_validator_group:
                errors += _run_validators_with_group_names(
                    post_error_validator_group,
                    group_names=successful_group_names,
                    validator_arguments=validator_arguments
                )
            return errors
        successful_group_names.append(group_name)
    return []


def _construct_validator_arguments(project_path, **kwargs):
    validator_arguments = {
        'project_path': project_path,
        'whitelists': defaults.WHITELISTS,
        'blacklists': defaults.BLACKLISTS,
    }
    validator_arguments.update(defaults.VALIDATOR_SETTINGS)
    validator_arguments.update(kwargs)
    return validator_arguments


def validate(project_path, original_project_path=None, **kwargs):
    pre_validation_checks = kwargs.pop('pre_validation_checks', None) or defaults.PRE_VALIDATION_CHECKS
    error_validator_groups = kwargs.pop('error_validator_groups', None)
    warning_validator_groups = kwargs.pop('warning_validator_groups', None)
    if not error_validator_groups:
        error_validator_groups = defaults.ERROR_VALIDATOR_GROUPS
        # use default warning groups only with default error groups
        if not warning_validator_groups:
            warning_validator_groups = defaults.WARNING_VALIDATOR_GROUPS
    validator_arguments = _construct_validator_arguments(
        project_path,
        original_project_path=original_project_path,
        **kwargs
    )

    pre_validation_errors = run_validator_group(pre_validation_checks, validator_arguments)
    if pre_validation_errors:
        return pre_validation_errors

    validator_arguments['project_folder'] = ProjectFolder(
        project_path,
        directories_to_skip=validator_arguments['directories_to_skip']
    )
    if original_project_path:
        validator_arguments['original_project_folder'] = ProjectFolder(
            original_project_path,
            directories_to_skip=validator_arguments['directories_to_skip']
        )
    return run_validator_group(
        validator_group=error_validator_groups,
        validator_arguments=validator_arguments,
        post_error_validator_group=warning_validator_groups
    )

