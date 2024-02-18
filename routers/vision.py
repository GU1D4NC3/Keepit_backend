from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends
from databases.basedb import EngineConn
from libs import vision
from sqlalchemy import text
from models.foodmodel import Food, EatAmount
from models.usermodel import User
from routers.user import get_current_user
from datetime import datetime, date
from pydantic import BaseModel
router = APIRouter()
engine = EngineConn()
session = engine.sessionmaker()


@router.get("/test", description="extract labels with test image")
async def test(current_user: Annotated[User, Depends(get_current_user)]):
    user_account = session.query(User).filter(User.id == current_user).first()
    if user_account is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        output = vision.run_quickstart()
        return {
            "stauts": "success",
            "data": {
                "labels": output
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Please check input and try again {e}",
        )


@router.get("/image/raw", description="get raw labels through vision ai")
async def get_label(current_user: Annotated[User, Depends(get_current_user)], image: str):
    user_account = session.query(User).filter(User.id == current_user).first()
    if user_account is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        output = vision.detect_image(image)
        return {
            "stauts": "success",
            "data": {
                "labels": output
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Please check input and try again {e}",
        )

@router.get("/labelcheck", description="check label through database")
async def label_check(label: str):
    try:
        basic_table = session.query(Food).filter(Food.title == label).first()
        if basic_table:
            return {
                "stauts": "success",
                "data": basic_table
            }
        else:
            return {
                "stauts": "fail",
                "data": "nodata"
            }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Please check input and try again {e}",
        )


@router.get("/image/labels", description="extract rawlabel, compair with db, bring labels which already stored")
async def image_labels(current_user: Annotated[User, Depends(get_current_user)], image: str):
    user_account = session.query(User).filter(User.id == current_user).first()
    if user_account is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        output = vision.detect_image(image)
        labeled = []
        for label in output:
            label_item = session.query(Food).filter(Food.title == label).first()
            if label_item:
                labeled.append(label_item)
        return {
            "stauts": "success",
            "data": {
                "exist_labels": labeled,
                "all_detected": output
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Please check input and try again {e}",
        )


class EatFood(BaseModel):
    label: str
    amount: float


@router.post("/eat/add", description="insert label with eat amount")
async def add_eat(current_user: Annotated[User, Depends(get_current_user)], eatfood: EatFood):
    label = eatfood.label
    amount = eatfood.amount
    try:
        item = session.query(Food).filter(Food.title == label).first()
        print(item.title)
        data = EatAmount(user_id=current_user,
                         food_title=item.title,
                         amount=amount,
                         calories=item.calories*amount,
                         protein=item.protein*amount,
                         carbohydrates=item.carbohydrates*amount,
                         fat=item.fat*amount,
                         fiber=item.fiber*amount,
                         vitamin_c=item.vitamin_C*amount,
                         potassium=item.potassium*amount,
                         calcium=item.calcium*amount,
                         iron=item.iron*amount)
        session.add(data)
        session.commit()
        session.close()
        return {
            "stauts": "success"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Please check input and try again {e}",
        )

@router.delete("/eat/delete", description="delete eat data")
async def remove_diary(current_user: Annotated[User, Depends(get_current_user)], id: int):
    user_account = session.query(User).filter(User.id == current_user).first()
    if user_account is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        session.query(EatAmount).filter(EatAmount.id == id,
                                        EatAmount.user_id == current_user).delete()
        session.commit()
        return {
            "status": "success",
            "message": f"Eat History deleted"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please check input and try again",
        )


@router.get("/eat/all", description="bring all eat record of user")
async def eat_history_all(current_user: Annotated[User, Depends(get_current_user)]):
    user_account = session.query(User).filter(User.id == current_user).first()
    if user_account is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        item = session.query(EatAmount).filter(EatAmount.user_id == current_user).all()
        return {
            "stauts": "success",
            "data": item
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Please check input and try again {e}",
        )

@router.get("/eat/date", description="bing eat data with date")
async def eat_history_date(current_user: Annotated[User, Depends(get_current_user)], date: date = date.today()):
    user_account = session.query(User).filter(User.id == current_user).first()
    if user_account is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        sql = (f"SELECT * FROM msdb.eat_amount "
               f"where user_id = '{current_user}' and "
               f"date(timestamp) = date({date});")
        item = session.execute(text(sql)).mappings().fetchall()
        return {
            "stauts": "success",
            "data": item
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Please check input and try again {e}",
        )

@router.get("/eat/range", description="get eat data with date range")
async def eat_history_term(current_user: Annotated[User, Depends(get_current_user)],
                           start_date: date=date.today(),
                           end_date: date=date.today()):
    user_account = session.query(User).filter(User.id == current_user).first()
    if user_account is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        sql = (f"SELECT * FROM msdb.eat_amount "
               f"where user_id = '{current_user}' "
               f"and date(timestamp) >= date({start_date}) "
               f"and date(timestamp) <= date({end_date});")
        item = session.execute(text(sql)).mappings().fetchall()
        return {
            "stauts": "success",
            "data": item
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Please check input and try again {e}",
        )