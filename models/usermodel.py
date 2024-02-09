from sqlalchemy import Column, TEXT, INT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(INT, nullable=False, primary_key=True)
    email = Column(TEXT, nullable=False)
    name = Column(TEXT, nullable=False)
    picture = Column(TEXT)
    locale = Column(TEXT)
    mom_name = Column(TEXT)
    baby_name = Column(TEXT)
    preg_date = Column(TEXT)
    birth = Column(TEXT)
    detail = Column(TEXT)


class Diary(Base):
    __tablename__ = "diary"
    id = Column(INT, nullable=False, primary_key=True, autoincrement=True)
    user_id = Column(TEXT, nullable=False)
    title = Column(TEXT, nullable=False)
    start_date = Column(TEXT, nullable=False)
    end_date = Column(TEXT)
    is_fullday = Column(INT)
    detail = Column(TEXT)
    icon = Column(INT)