from sqlalchemy import Column, TEXT, INT, BIGINT, JSON, FLOAT
from sqlalchemy.ext.declarative import declarative_base
import datetime
Base = declarative_base()


class Food(Base):
    __tablename__ = "food_data"
    id = Column(INT, nullable=False, autoincrement=True, primary_key=True)
    title = Column(TEXT, nullable=False)
    calories = Column(FLOAT)
    protein = Column(FLOAT)
    carbohydrates = Column(FLOAT)
    fat = Column(FLOAT)
    fiber = Column(FLOAT)
    vitamin_C = Column(FLOAT)
    potassium = Column(FLOAT)
    calcium = Column(FLOAT)
    iron = Column(FLOAT)


class EatAmount(Base):
    __tablename__ = "eat_amount"
    id = Column(INT, nullable=False, autoincrement=True, primary_key=True)
    user_id = Column(INT, nullable=False)
    food_title = Column(TEXT, nullable=False)
    amount = Column(INT)
    timestamp = Column(TEXT, default=datetime.datetime.now)
    calories = Column(FLOAT)
    protein = Column(FLOAT)
    carbohydrates = Column(FLOAT)
    fat = Column(FLOAT)
    fiber = Column(FLOAT)
    vitamin_c = Column(FLOAT)
    potassium = Column(FLOAT)
    calcium = Column(FLOAT)
    iron = Column(FLOAT)