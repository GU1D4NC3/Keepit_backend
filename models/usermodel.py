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