from sqlalchemy import Column, TEXT, INT
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class Quiz(Base):
    __tablename__ = "quiz"
    id = Column(INT, nullable=False, autoincrement=True, primary_key=True)
    title = Column(TEXT, nullable=False)
    desc = Column(TEXT, nullable=False)
    selections = Column(TEXT, nullable=False)
    ansno = Column(INT, nullable=False)
    created = Column(TEXT, default=datetime.datetime.now)