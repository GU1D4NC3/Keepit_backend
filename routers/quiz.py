from typing import Annotated
from fastapi import APIRouter,HTTPException, Depends, status
from databases.basedb import EngineConn
from pydantic import BaseModel
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



@router.post("/insert", description="insert quiz (admin only)")
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


@router.delete("/delete", description="quiz removal (admin only)")
async def remove_quiz(current_user: Annotated[User, Depends(get_current_user)],
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


@router.put("/update" , description="quiz update (admin only)")
async def update_quiz(current_user: Annotated[User, Depends(get_current_user)],
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


@router.get("/random", description="get random quiz")
async def get_randomquiz():
    RandomQuiz = session.query(Quiz).order_by(text("RAND()")).limit(1)
    return {
        "status": "success",
        "data": RandomQuiz[0]
    }

@router.get("/id", description="get quiz with quiz id")
async def get_selected_quiz(id:int):
    RandomQuiz = session.query(Quiz).filter(Quiz.id == id).first()
    return {
        "status": "success",
        "data": RandomQuiz
    }