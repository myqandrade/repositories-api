import json
import os
import shutil

import git


def get_repository_by_user_repository(user, repository):
    repo_url = f'https://github.com/{user}/{repository}.git'

    # Define o diretório local
    repo_dir = 'diretorio_local_repositorio'

    # Remove o repositório se já existir
    if os.path.exists(repo_dir):
        shutil.rmtree(repo_dir)

    # Clona o repositório
    repo = git.Repo.clone_from(repo_url, repo_dir)

    return repo