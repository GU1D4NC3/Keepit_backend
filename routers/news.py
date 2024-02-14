from typing import Annotated
from fastapi import APIRouter,HTTPException, Depends, status
from databases.basedb import EngineConn
from pydantic import BaseModel
from datetime import datetime, date
from sqlalchemy import text

from models.newsmodel import News
from models.usermodel import User
from routers.user import get_current_user

router = APIRouter()
engine = EngineConn()
session = engine.sessionmaker()


class NewNews(BaseModel):
    title: str
    detail: str
    created: datetime
    info: str

class UpdateNews(BaseModel):
    news_id: int
    title: str
    detail: str
    created: datetime
    info: str



@router.post("/insert", description="뉴스 추가 기능 (관리자 전용)")
async def insert_news(current_user: Annotated[User, Depends(get_current_user)],
                      new_data: NewNews):
    user_account = session.query(User).filter(User.id == current_user).first()
    if user_account is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        data = News(
            title=new_data.title,
            detail=new_data.detail,
            created=new_data.created,
            info=new_data.info,
        )
        session.add(data)
        session.commit()
        session.close()
        return {
            "status": "success",
            "message": f"News {new_data.title} added"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Please check input and try again {e}",
        )


@router.delete("/delete", description="뉴스 제거 기능 (관리자 전용)")
async def remove_news(current_user: Annotated[User, Depends(get_current_user)],
                      newsid: int):
    user_account = session.query(User).filter(User.id == current_user).first()
    if user_account is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        session.query(News).filter(News.id == newsid).delete()
        session.commit()
        return {
            "status": "success",
            "message": f"diary deleted"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please check input and try again",
        )


@router.put("/update", description="뉴스 수정 기능 (관리자 전용)")
async def update_News(current_user: Annotated[User, Depends(get_current_user)],
                      update_data: UpdateNews):
    user_account = session.query(User).filter(User.id == current_user).first()
    news = session.query(News).filter(News.id == update_data.news_id).first()

    if user_account is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        news.title = update_data.title
        news.detail = update_data.detail
        news.created = update_data.created
        news.info = update_data.info
        session.add(news)
        session.commit()
        session.close()
        return {
            "status": "success",
            "message": f"News {update_data.title} updated"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please check input and try again",
        )


@router.get("/random", description="랜덤한 뉴스 하나를 불러옴")
async def get_random_news():
    RandomNews = session.query(News).order_by(text("RAND()")).limit(1)
    return {
        "status": "success",
        "data": RandomNews[0]
    }

@router.get("/id", description="News ID 로 하나를 불러옴")
async def get_selected_news(id:int):
    SelectedNews = session.query(News).filter(News.id == id).first()
    return {
        "status": "success",
        "data": SelectedNews
    }

@router.get("/date", description="해당 날짜의 뉴스를 가져옴")
async def get_date_news(date: date):
    SelectedNews = session.query(News).filter(text(f"date(created) = '{date}'")).all()
    return {
        "status": "success",
        "data": SelectedNews
    }

@router.get("/range", description="날짜범위내의 뉴스를 가져옴")
async def get_date_news(start: date, end: date):
    SelectedNews = session.query(News).filter(text(f"date(created) >='{start}' and date(created) <='{end}'")).all()
    return {
        "status": "success",
        "data": SelectedNews
    }