from typing import Annotated
from fastapi import APIRouter,HTTPException, Depends, status
from databases.basedb import EngineConn
from pydantic import BaseModel
from datetime import datetime

from models.usermodel import User, Diary
from routers.user import get_current_user

router = APIRouter()
engine = EngineConn()
session = engine.sessionmaker()


class NewDiary(BaseModel):
    title: str
    start_date: datetime
    end_date: datetime
    is_fullday: int
    detail: str
    icon: int


class DiaryUpdate(BaseModel):
    diary_id:int
    title: str
    start_date: datetime
    end_date: datetime
    is_fullday: int
    detail: str
    icon: int


class MessageResp(BaseModel):
    status: str = "success"
    message: str = "some messages"


class ListData(BaseModel):
    status: str = "success"
    data: list | None = None


@router.post("/insert", description="Insert diary",
             response_model=MessageResp)
async def insert_diary(current_user: Annotated[User, Depends(get_current_user)],
                      new_data: NewDiary):
    user_account = session.query(User).filter(User.id == current_user).first()
    if user_account is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        data = Diary(
            user_id=current_user,
            title=new_data.title,
            start_date=new_data.start_date,
            end_date=new_data.end_date,
            is_fullday=new_data.is_fullday,
            detail=new_data.detail,
            icon=new_data.icon
        )
        session.add(data)
        session.commit()
        session.close()
        res = MessageResp
        res.message = f"diary {new_data.title} added"
        return res
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Please check input and try again {e}",
        )


@router.get("/all",
            description="get all diary imported by user",
            response_model=ListData)
async def get_users_all_diary(current_user: Annotated[User, Depends(get_current_user)],):
    user_account = session.query(User).filter(User.id == current_user).first()
    if user_account is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        diarys = session.query(Diary).filter(Diary.user_id == current_user).all()
        return {
            "status": "success",
            "data": diarys
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please check input and try again",
        )



@router.get("/range", description="get diary between start and end")
async def get_users_diary_with_date(current_user: Annotated[User, Depends(get_current_user)],
                      startdate: datetime, enddate: datetime):
    user_account = session.query(User).filter(User.id == current_user).first()
    if user_account is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        diarys = session.query(Diary).filter(Diary.user_id == current_user,
                                             Diary.start_date < enddate,
                                             Diary.end_date > startdate).all()
        return {
            "status": "success",
            "data": diarys
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please check input and try again",
        )



@router.put("/update", description="update diary")
async def update_diary(current_user: Annotated[User, Depends(get_current_user)],
                      update_data: DiaryUpdate):
    user_account = session.query(User).filter(User.id == current_user).first()
    diary = session.query(Diary).filter(Diary.id == update_data.diary_id).first()

    if user_account is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        diary.title = update_data.title
        diary.start_date = update_data.start_date
        diary.end_date = update_data.end_date
        diary.is_fullday = update_data.is_fullday
        diary.detail = update_data.detail
        diary.icon = update_data.icon
        session.add(diary)
        session.commit()
        session.close()
        return {
            "status": "success",
            "message": f"diary {update_data.title} updated"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please check input and try again",
        )


@router.delete("/delete", description="delete diary")
async def remove_diary(current_user: Annotated[User, Depends(get_current_user)],
                      diaryid: int):
    user_account = session.query(User).filter(User.id == current_user).first()
    if user_account is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        session.query(Diary).filter(Diary.id == diaryid).delete()
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