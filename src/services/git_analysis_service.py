from datetime import datetime

from flask import request

from src.client.github_client import get_repository_by_user_repository
from src.models.git_analysis_result import GitAnalysisResult
from src.repositories.git_analysis_repository import save_analysis_result, search_analysis_by_author


def get_repository_status(user, repository):
    repo = get_repository_by_user_repository(user, repository)

    commits_por_desenvolvedor = {}

    for commit in repo.iter_commits():

        autor = commit.author.name

        if autor not in commits_por_desenvolvedor:
            commits_por_desenvolvedor[autor] = 1

        else:
            commits_por_desenvolvedor[autor] += 1

    dias_por_desenvolvedor = {}

    for commit in repo.iter_commits():

        autor = commit.author.name
        data_commit = commit.committed_datetime.date()

        if autor not in dias_por_desenvolvedor:
            dias_por_desenvolvedor[autor] = {data_commit}

        else:
            dias_por_desenvolvedor[autor].add(data_commit)

    for autor, commits in commits_por_desenvolvedor.items():
        dias = len(dias_por_desenvolvedor[autor])
        media_commits_por_dia = commits / dias
        message = f'{autor} realizou {commits} commits com uma média de {media_commits_por_dia:.2f} commits por dia.<br>'

        analysis = GitAnalysisResult()
        analysis.author = autor
        analysis.analyze_date = datetime.now()
        analysis.average_commits = media_commits_por_dia
        analysis.repository_url = repo.remotes.origin.url
        analysis.repository_name = repository

        save_analysis_result(analysis)

    return message

def get_analysis_by_author(authors):
    resultados = []
    for author in authors:
        analysis = search_analysis_by_author(author)
        for registro in analysis:
            resultados.append(f'{registro.author} possui uma média de {registro.average_commits:.2f} commits por dia.')

    resultados_nao_duplicados = set(resultados)
    return "<br>".join(resultados_nao_duplicados)