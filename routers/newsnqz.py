from typing import Annotated
from fastapi import APIRouter,HTTPException, Depends, status
from databases.basedb import EngineConn
from pydantic import BaseModel
from datetime import datetime, date
from sqlalchemy import text

from models.newsnqzmodel import NewsNQz
from models.usermodel import User
from routers.user import get_current_user

router = APIRouter()
engine = EngineConn()
session = engine.sessionmaker()


class NewNQ(BaseModel):
    id: int
    news_title: str
    news_detail: str
    news_image: str
    quiz_title: str
    quiz_type: str
    quiz_choice: str
    quiz_detail: str
    quiz_description: str
    quiz_answer: str


class UpdateNQ(BaseModel):
    news_id: int
    title: str
    detail: str
    updated: datetime
    info: str



@router.post("/update",
             description="insert news or update if exist")
async def insert_nq(data: NewNQ):
    try:
        existing_item = session.query(NewsNQz).filter(NewsNQz.id == data.id).first()
        if existing_item:
            # update if duplicated item exist
            existing_item.news_title = data.news_title
            existing_item.news_detail = data.news_detail
            existing_item.news_image = data.news_image
            existing_item.quiz_title = data.quiz_title
            existing_item.quiz_type = data.quiz_type
            existing_item.quiz_choice = data.quiz_choice
            existing_item.quiz_detail = data.quiz_detail
            existing_item.quiz_description = data.quiz_description
            existing_item.quiz_answer = data.quiz_answer
            existing_item.updated_at = datetime.now()
            existing_item.deleted_at = None
            session.add(existing_item)
            session.commit()
            session.close()
            return {
                "status": "success",
                "message": f"News {data.id} {data.news_title} updated",
                "updated_at": f"{datetime.now()}"
            }
    except Exception as e:
        raise {
            "status": "failed",
            "message": f"Please check input {e}"
        }
    session.flush()
    new_data = NewsNQz(
        id=data.id,
        news_title=data.news_title,
        news_detail=data.news_detail,
        news_image=data.news_image,
        quiz_title=data.quiz_title,
        quiz_type=data.quiz_type,
        quiz_choice=data.quiz_choice,
        quiz_detail=data.quiz_detail,
        quiz_description=data.quiz_description,
        quiz_answer=data.quiz_answer,
    )
    session.add(new_data)
    try:
        session.commit()
        session.close()
        return {
            "status": "success",
            "message": f"News {data.id} {data.news_title} added",
            "updated_at": f"{datetime.now()}"
        }
    except:
        session.rollback()
        session.close()
        raise {
            "status": "failed",
            "message": f"Please check input"
        }


@router.delete("/delete", description="delete news(admin only)")
async def insert_nq(news_id:int):
    try:
        existing_item = session.query(NewsNQz).filter(NewsNQz.id == news_id).first()
        if existing_item:
            existing_item.deleted_at = datetime.now()
            session.commit()
            return {
                "status": "success",
                "message": f"News {existing_item.id} {existing_item.news_title} deleted"
            }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Please check input and try again {e}",
        )


@router.get("/random", description="get random news")
async def get_random_news():
    RandomNews = (session.query(NewsNQz).filter(text("deleted_at is null"))
                  .order_by(text("RAND()")).limit(1))
    session.close()
    return {
        "status": "success",
        "data": RandomNews[0]
    }

@router.get("/id", description="get news with News ID")
async def get_selected_news(id:int):
    SelectedNews = session.query(NewsNQz).filter(NewsNQz.id == id).first()
    session.close()
    return {
        "status": "success",
        "data": SelectedNews
    }

@router.get("/date", description="get news with updated date")
async def get_date_news(date: date=date.today()):
    SelectedNews = (session.query(NewsNQz)
                    .filter(text(f"deleted_at is null and date(updated_at) = '{date}'")).all())
    session.close()
    return {
        "status": "success",
        "data": SelectedNews
    }

@router.get("/range", description="get news with updated date in range")
async def get_date_news(start: date=date.today(), end: date=date.today()):
    SelectedNews = (session.query(NewsNQz)
                    .filter(text(f"deleted_at is null and date(updated_at) >='{start}' and date(updated_at) <='{end}'")).all())
    session.close()
    return {
        "status": "success",
        "data": SelectedNews
    }