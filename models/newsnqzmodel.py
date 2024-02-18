from sqlalchemy import Column, TEXT, INT, DATETIME
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class NewsNQz(Base):
    __tablename__ = "newsnqz"
    id = Column(INT, nullable=False, autoincrement=True, primary_key=True)
    news_title = Column(TEXT)
    news_detail = Column(TEXT)
    news_image = Column(TEXT)
    quiz_title = Column(TEXT)
    quiz_type = Column(TEXT)
    quiz_choice = Column(TEXT)
    quiz_detail = Column(TEXT)
    quiz_description = Column(TEXT)
    quiz_answer = Column(TEXT)
    created_at = Column(DATETIME, nullable=False, default=datetime.datetime.now)
    updated_at = Column(DATETIME, nullable=False, default=datetime.datetime.now)
    deleted_at = Column(DATETIME)
