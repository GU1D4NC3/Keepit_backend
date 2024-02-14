from sqlalchemy import Column, TEXT, INT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Test(Base):
    __tablename__ = "test"
    id = Column(INT, nullable=False, autoincrement=True, primary_key=True)
    title = Column(TEXT, nullable=False)