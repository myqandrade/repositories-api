from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class GitAnalysisResult(Base):
    __tablename__ = 'git_analysis_results'

    id = Column(Integer, primary_key=True)
    author = Column(String)
    analyze_date = Column(DateTime)
    average_commits = Column(Float)
    repository_url = Column(String)
    repository_name = Column(String)