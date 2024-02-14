from sqlalchemy import Column, TEXT, INT
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class News(Base):
    __tablename__ = "news"
    id = Column(INT, nullable=False, autoincrement=True, primary_key=True)
    title = Column(TEXT, nullable=False)
    detail = Column(TEXT, nullable=False)
    created = Column(TEXT, nullable=False, default=datetime.datetime.now)
    info = Column(TEXT, nullable=False)
