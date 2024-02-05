from fastapi import APIRouter, Depends, HTTPException, status
from auth.jwt import create_access_token, verify_access_token
from databases.basedb import EngineConn
from models.users import User

router = APIRouter()
engine = EngineConn()
session = engine.sessionmaker()


@router.post("/login")
async def login(body: User) -> dict:
    existing_user = session.get(User, body.email)
    try:
        if existing_user:
            access_token = create_access_token(body.email, body.exp)
        else:
            session.add(body)
            session.commit()
            session.refresh(body)
            access_token = create_access_token(body.email, body.exp)
        return {
            "status": "success",
            "access_token": access_token,
            "token_type": "Bearer"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Bad Parameter {e}",
        )


@router.get("/whoami")
async def login(token) -> dict:
    existing_user = verify_access_token(token)
    try:
        return {
            "status": "success",
            "data": existing_user,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Bad Parameter {e}",
        )
