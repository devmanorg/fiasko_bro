from collections import OrderedDict
import logging

from . import validators
from . import pre_validation_checks
from .repository_info import LocalRepositoryInfo
from . import config


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def validate_repo(path_to_repo, path_to_original_repo=None, **kwargs):
    code_validator = CodeValidator()
    return code_validator.validate(path_to_repo, path_to_original_repo, **kwargs)


class CodeValidator:
    blacklists = config.DEFAULT_BLACKLISTS

    whitelists = config.DEFAULT_WHITELISTS

    _default_settings = config.VALIDATOR_SETTINGS

    pre_validation_checks = {
        'encoding': [
            pre_validation_checks.are_sources_in_utf
        ],
        'size': [
            pre_validation_checks.are_repos_too_large
        ]
    }

    error_validator_groups = OrderedDict(
        [
            (
                'commits',
                [validators.has_more_commits_than_origin],
            ),
            (
                'readme',
                [validators.has_readme_file],
            ),
            (
                'bom',
                [validators.has_no_bom],
            ),
            (
                'syntax',
                [validators.has_no_syntax_errors],
            ),
            (
                'general',
                [
                    validators.has_no_directories_from_blacklist,
                    validators.is_pep8_fine,
                    validators.has_changed_readme,
                    validators.is_snake_case,
                    validators.is_mccabe_difficulty_ok,
                    validators.has_no_encoding_declaration,
                    validators.has_no_star_imports,
                    validators.has_no_local_imports,
                    validators.has_local_var_named_as_global,
                    validators.has_variables_from_blacklist,
                    validators.has_no_short_variable_names,
                    validators.has_no_range_from_zero,
                    validators.are_tabs_used_for_indentation,
                    validators.has_no_try_without_exception,
                    validators.has_frozen_requirements,
                    validators.has_no_vars_with_lambda,
                    validators.has_no_calls_with_constants,
                    validators.has_readme_in_single_language,
                    validators.has_no_urls_with_hardcoded_arguments,
                    validators.has_no_nonpythonic_empty_list_validations,
                    validators.has_no_extra_dockstrings,
                    validators.has_no_exit_calls_in_functions,
                    validators.has_no_libs_from_stdlib_in_requirements,
                    validators.has_no_lines_ends_with_semicolon,
                    validators.not_validates_response_status_by_comparing_to_200,
                    validators.has_no_mutable_default_arguments,
                    validators.has_no_slices_starts_from_zero,
                    validators.has_no_cast_input_result_to_str,
                    validators.has_no_return_with_parenthesis,
                    validators.has_no_long_files,
                    validators.is_nesting_too_deep,
                    validators.has_no_string_literal_sums,
                ],
            ),
        ]
    )

    warning_validator_groups = {
        'commits': [
            validators.has_no_commit_messages_from_blacklist,
        ],
        'syntax': [
            validators.has_indents_of_spaces,
            validators.has_no_variables_that_shadow_default_names,
        ]
    }

    for name in warning_validator_groups:
        assert name in error_validator_groups.keys()

    def __init__(self, **kwargs):
        self.validator_arguments = dict(self._default_settings)
        self.validator_arguments.update(kwargs)

    @staticmethod
    def _is_successful_validation(validation_result):
        return not isinstance(validation_result, tuple)

    def _run_validator_group(self, group, arguments):
        errors = []
        for validator in group:
            validation_result = validator(**arguments)
            if not self._is_successful_validation(validation_result):
                errors.append(validation_result)
        return errors

    def _run_warning_validators_until(self, failed_error_group_name, arguments):
        """Gets warnings up until but not including the failed group"""
        warnings = []
        for error_group_name in self.error_validator_groups.keys():
            if error_group_name == failed_error_group_name:
                return warnings
            warnings += self._run_validator_group(
                self.warning_validator_groups.get(error_group_name, []),
                arguments
            )
        return warnings

    def run_validator_group(self, group, add_warnings=False, *args, **kwargs):
        errors = []
        for error_group_name, error_group in group.items():
            errors += self._run_validator_group(
                error_group,
                self.validator_arguments
            )
        if add_warnings and errors:
            errors += self._run_warning_validators_until(
                error_group_name,
                self.validator_arguments
            )
            return errors
        return errors

    def get_syntax_errors_in_repos(self, solution_repo, original_repo=None):
        syntax_errors = validators.has_no_syntax_errors(solution_repo)
        if syntax_errors:
            return [syntax_errors]
        if original_repo:
            syntax_errors = validators.has_no_syntax_errors(original_repo)
            if syntax_errors:
                return [syntax_errors]

    def validate(self, repo_path, original_repo_path=None, check_repo_size=True, **kwargs):
        self.validator_arguments.update(kwargs)
        self.validator_arguments['path_to_repo'] = repo_path
        self.validator_arguments['original_repo_path'] = original_repo_path
        self.validator_arguments['whitelists'] = self.whitelists
        self.validator_arguments['blacklists'] = self.blacklists
        pre_validation_errors = self.run_validator_group(self.pre_validation_checks)
        if pre_validation_errors:
            return pre_validation_errors
        self.validator_arguments['solution_repo'] = LocalRepositoryInfo(repo_path)
        if original_repo_path:
            self.validator_arguments['original_repo'] = LocalRepositoryInfo(original_repo_path)
        syntax_errors = self.get_syntax_errors_in_repos(
            self.validator_arguments['solution_repo'],
            self.validator_arguments.get('original_repo', None)
        )
        if syntax_errors:
            return syntax_errors
        return self.run_validator_group(self.error_validator_groups, add_warnings=True)
