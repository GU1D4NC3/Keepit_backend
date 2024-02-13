from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends
from databases.basedb import EngineConn
from libs import vision
from sqlalchemy import text
from models.food import Food, EatAmount
from models.usermodel import User
from routers.user import get_current_user
from datetime import datetime
from pydantic import BaseModel
router = APIRouter()
engine = EngineConn()
session = engine.sessionmaker()


@router.get("/test", description="미리 저장된 테스트 이미지로 데이터를 추출합니다")
async def test():
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


@router.get("/get_label", description="image 에 사진 데이터를 넣어 라벨을 전부 추출합니다.")
async def get_label(image: str):
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

@router.get("/is_label", description="추출된 라벨이 DB 에 있는 항목인지 검증합니다")
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


@router.get("/image_labels", description="이미지를 통해 라벨을 추출하고, DB 의 라벨과 비교하여 있으면 해당 항목을 꺼내옵니다")
async def image_labels(image:str):
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
    amount: str


@router.post("/add_eat", description="추출된(검증된) 라벨을 넣고, 섭취 양을 넣습니다.")
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

@router.get("/eat_history_all", description="섭취된 기록을 전부 가져옵니다.")
async def eat_history_all(current_user: Annotated[User, Depends(get_current_user)]):
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

@router.get("/eat_history_date", description="특정 날짜의 섭취 기록을 가져옵니다")
async def eat_history_date(current_user: Annotated[User, Depends(get_current_user)], date: datetime):
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

@router.get("/eat_history_term", description="특정 기간의 섭취 기록을 가져옵니다")
async def eat_history_term(current_user: Annotated[User, Depends(get_current_user)], start_date: datetime, end_date:datetime):
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