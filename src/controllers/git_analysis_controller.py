from flask import Flask, request, abort

from src.services.git_analysis_service import get_repository_status, get_analysis_by_author

app = Flask(__name__)

@app.route('/analisador-git', methods=['POST'])
def git_analysis():
    user = request.args.get('usuario')
    repository = request.args.get('repositorio')
    if user is None:
        abort(400, description="User cannot be None")
    if repository is None:
        abort(400, description="User cannot be None")
    return get_repository_status(user, repository)

@app.route('/analisador-git/buscar', methods=['GET'])
def buscar_medias_de_commit():
    authors = request.args.getlist('autor')
    return get_analysis_by_author(authors)
