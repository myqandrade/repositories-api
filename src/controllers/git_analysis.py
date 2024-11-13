from flask import Flask

from src.services.git_analysis_service import get_repository_status, get_commits_average

app = Flask(__name__)

@app.route('/analisador-git', methods=['GET'])
def git_analysis():
    return get_repository_status()


@app.route('/analisador-git/buscar', methods=['GET'])
def buscar_medias_de_commit():
    return get_commits_average()
