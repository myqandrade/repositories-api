import os
import shutil
from datetime import datetime

import git
from flask import request
from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker

from src.models.git_analysis_result import Base, GitAnalysisResult

engine = create_engine('sqlite:///git_analysis_results.db')

def get_repository_status():
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    usuario = request.args.get('usuario')
    repositorio = request.args.get('repositorio')

    # verifica se algum dos parâmetros é está vazio
    if usuario is None:
        raise ValueError("Usuario nao pode ser none")
    if repositorio is None:
        raise ValueError("Repositorio nao pode ser none")

    repo_url = f'https://github.com/{usuario}/{repositorio}.git'

    # Define o diretório local
    repo_dir = 'diretorio_local_repositorio'

    # Remove o repositório se já existir
    if os.path.exists(repo_dir):
        shutil.rmtree(repo_dir)

    # Clona o repositório
    repo = git.Repo.clone_from(repo_url, repo_dir)

    # Inicializa dicionário para armazenar os commits por desenvolvedor
    commits_por_desenvolvedor = {}

    # Itera pelo histórico de commit
    for commit in repo.iter_commits():
        # Obtem o nome do autor
        autor = commit.author.name

        # Se o autor não estiver no dicionário inicia com 1
        if autor not in commits_por_desenvolvedor:
            commits_por_desenvolvedor[autor] = 1
        # Incrementa mais um ao autor
        else:
            commits_por_desenvolvedor[autor] += 1

    # Inicializa o dicionário para armazenar o número de dias
    dias_por_desenvolvedor = {}

    # Itera pelo histórico de commits
    for commit in repo.iter_commits():
        # Obtem o nome do autor
        autor = commit.author.name
        data_commit = commit.committed_datetime.date()

        # If the author name is not in the dictionary, add it and set the value to the commit date
        # Se o nome do autor não estiver no dicionário, adiciona e coloca a data de commit
        if autor not in dias_por_desenvolvedor:
            dias_por_desenvolvedor[autor] = {data_commit}
        # Adiciona mais commits ao set de datas do autor
        else:
            dias_por_desenvolvedor[autor].add(data_commit)

    response = ''

    # Retorna o total de commits e a média de commits por dia por desenvolvedor
    for autor, commits in commits_por_desenvolvedor.items():
        dias = len(dias_por_desenvolvedor[autor])
        media_commits_por_dia = commits / dias
        response += f'{autor} realizou {commits} commits com uma média de {media_commits_por_dia:.2f} commits por dia.<br>'

        # Cria todas as tabelas se não existir
        Base.metadata.create_all(engine)

        # Cria um novo GitAnalysisResult para persistir no banco
        result = GitAnalysisResult()
        result.author = autor
        result.analyze_date = datetime.now()
        result.average_commits = media_commits_por_dia
        result.repository_url = repo_url
        result.repository_name = repositorio

        # Adiciona o objeto GitAnalysisResult na transação e fazer o commit no banco
        session.add(result)
        session.commit()

        # Fecha a conexão com o banco
        session.close()

    return response

def get_commits_average():
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    autor1 = request.args.get('autor1')
    autor2 = request.args.get('autor2')
    autor3 = request.args.get('autor3')
    autores = [autor1, autor2, autor3]

    resultados = []
    for autor in autores:
        for registro in session.query(GitAnalysisResult).filter(GitAnalysisResult.author.ilike(f"%{autor}%")).all():
            resultados.append(f'{registro.author} possui uma média de {registro.average_commits:.2f} commits por dia.')

    resultados_nao_duplicados = set(resultados)
    return "<br>".join(resultados_nao_duplicados)