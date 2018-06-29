import os
import re

from ..i18n import _


def no_readme_file(project_folder, readme_filename, *args, **kwargs):
    if not project_folder.does_file_exist(readme_filename):
        return _('there is no %s') % readme_filename


def readme_not_changed(project_folder, readme_filename, original_project_folder=None, *args, **kwargs):
    if not original_project_folder:
        return
    original_readme_path = os.path.join(original_project_folder.path, readme_filename)
    solution_readme_path = os.path.join(project_folder.path, readme_filename)
    try:
        with open(original_readme_path, encoding='utf-8') as original_handler:
            original_readme = original_handler.read()
    except FileNotFoundError:
        return
    with open(solution_readme_path, encoding='utf-8') as solution_handler:
        solution_readme = solution_handler.read()
    if solution_readme == original_readme:
        return ''


def bilingual_readme(project_folder, readme_filename, min_percent_of_another_language, *args, **kwargs):
    raw_readme = project_folder.get_file(readme_filename)
    readme_no_code = re.sub(r'\s```[#!A-Za-z]*\n[\s\S]*?\n```\s', '', raw_readme)
    clean_readme = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', '', readme_no_code)
    ru_letters_amount = len(re.findall(r'[а-яА-Я]', clean_readme))
    en_letters_amount = len(re.findall(r'[a-zA-Z]', clean_readme))
    if not (ru_letters_amount + en_letters_amount):
        return
    another_language_percent = min([ru_letters_amount, en_letters_amount]) * 100
    another_language_percent /= (ru_letters_amount + en_letters_amount)
    if another_language_percent > min_percent_of_another_language:
        return ''
