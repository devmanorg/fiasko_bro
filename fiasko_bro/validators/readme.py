import os
import re

from ..i18n import _


def has_readme_file(solution_repo, readme_filename, *args, **kwargs):
    if not solution_repo.does_file_exist(readme_filename):
        return 'need_readme', _('there is no %s') % readme_filename


def has_changed_readme(solution_repo, readme_filename, original_repo=None, *args, **kwargs):
    if not original_repo:
        return
    original_readme_path = os.path.join(original_repo.path, readme_filename)
    solution_readme_path = os.path.join(solution_repo.path, readme_filename)
    try:
        with open(original_readme_path, encoding='utf-8') as original_handler:
            original_readme = original_handler.read()
    except FileNotFoundError:
        return
    try:
        with open(solution_readme_path, encoding='utf-8') as solution_handler:
            solution_readme = solution_handler.read()
        if solution_readme == original_readme:
            return 'need_readme', None
    except UnicodeDecodeError:
        return 'readme_not_utf_8', None


def has_readme_in_single_language(solution_repo, readme_filename, min_percent_of_another_language, *args, **kwargs):
    raw_readme = solution_repo.get_file(readme_filename)
    readme_no_code = re.sub("\s```[#!A-Za-z]*\n[\s\S]*?\n```\s", '', raw_readme)
    clean_readme = re.sub("\[([^\]]+)\]\(([^)]+)\)", '', readme_no_code)
    ru_letters_amount = len(re.findall('[а-яА-Я]', clean_readme))
    en_letters_amount = len(re.findall('[a-zA-Z]', clean_readme))
    if not (ru_letters_amount + en_letters_amount):
        return
    another_language_percent = min([ru_letters_amount, en_letters_amount]) * 100
    another_language_percent /= (ru_letters_amount + en_letters_amount)
    if another_language_percent > min_percent_of_another_language:
        return 'bilingual_readme', ''
