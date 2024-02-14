from typing import Annotated
from fastapi import APIRouter,HTTPException, Depends, status
from databases.basedb import EngineConn
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import text

from models.quizmodel import Quiz
from models.usermodel import User
from routers.user import get_current_user

router = APIRouter()
engine = EngineConn()
session = engine.sessionmaker()


class NewQuiz(BaseModel):
    title: str
    desc: str
    selections: str
    ansno: int


class UpdateQuiz(BaseModel):
    quiz_id:int
    title: str
    desc: str
    selections: str
    ansno: int



@router.post("/insert", description="퀴즈 추가 기능 (관리자 전용)")
async def insert_quiz(current_user: Annotated[User, Depends(get_current_user)],
                      new_data: NewQuiz):
    user_account = session.query(User).filter(User.id == current_user).first()
    if user_account is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        data = Quiz(
            title=new_data.title,
            desc=new_data.desc,
            selections=new_data.selections,
            ansno=new_data.ansno,
        )
        session.add(data)
        session.commit()
        session.close()
        return {
            "status": "success",
            "message": f"Quiz {new_data.title} added"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Please check input and try again {e}",
        )


@router.delete("/delete", description="퀴즈 제거 기능")
async def remove_diary(current_user: Annotated[User, Depends(get_current_user)],
                      quizid: int):
    user_account = session.query(User).filter(User.id == current_user).first()
    if user_account is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        session.query(Quiz).filter(Quiz.id == quizid).delete()
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


@router.put("/update" , description="퀴즈 수정 기능 (관리자 전용)")
async def update_diary(current_user: Annotated[User, Depends(get_current_user)],
                      update_data: UpdateQuiz):
    user_account = session.query(User).filter(User.id == current_user).first()
    quiz = session.query(Quiz).filter(Quiz.id == update_data.quiz_id).first()

    if user_account is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        quiz.title = update_data.title
        quiz.desc = update_data.desc
        quiz.selections = update_data.selections
        quiz.ansno = update_data.ansno
        session.add(quiz)
        session.commit()
        session.close()
        return {
            "status": "success",
            "message": f"Quiz {update_data.title} updated"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please check input and try again",
        )


@router.get("/random", description="랜덤한 퀴즈 하나를 불러옴")
async def get_users_all_diary():
    RandomQuiz = session.query(Quiz).order_by(text("RAND()")).limit(1)
    return {
        "status": "success",
        "data": RandomQuiz[0]
    }

@router.get("/id", description="Quiz ID 로 하나를 불러옴")
async def get_selected_quiz(id:int):
    RandomQuiz = session.query(Quiz).filter(Quiz.id == id).first()
    return {
        "status": "success",
        "data": RandomQuiz
    }