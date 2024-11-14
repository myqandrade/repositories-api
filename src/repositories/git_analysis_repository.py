import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.models.git_analysis_result import GitAnalysisResult, Base

db_path = 'src/database/git_analysis_results.db'

os.makedirs(os.path.dirname(db_path), exist_ok=True)

engine = create_engine('sqlite:///git_analysis_results.db')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


def save_analysis_result(result):
    session = Session()
    session.add(result)
    session.commit()
    session.close()

def search_analysis_by_author(author):
    session = Session()
    result = session.query(GitAnalysisResult).filter(GitAnalysisResult.author.ilike(f"%{author}%")).all()
    print(result)
    session.close()
    return result