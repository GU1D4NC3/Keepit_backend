from sqlalchemy import Column, TEXT, INT, DATETIME, FLOAT
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class Hospital(Base):
    __tablename__ = "map_hospital"
    id = Column(INT, nullable=False, autoincrement=True, primary_key=True)
    name = Column(TEXT)
    type = Column(TEXT)
    area = Column(TEXT)
    address = Column(TEXT)
    pos_x = Column(FLOAT)
    pos_y = Column(FLOAT)
    phone = Column(TEXT)
