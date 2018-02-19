def has_no_bom(solution_repo, *args, **kwargs):
    bom = '\ufeff'
    for _, file_content, _ in solution_repo.get_ast_trees(
        with_filenames=True,
        with_file_content=True
    ):
        if file_content.startswith(bom):
            return 'has_bom', ''

    requirements = solution_repo.get_file('requirements.txt')
    if requirements and requirements.startswith(bom):
        return 'has_bom', ''
