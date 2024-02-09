from fastapi import Request, Depends, APIRouter, HTTPException, status
from databases.basedb import EngineConn
from models.usermodel import User
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from jose import jwt, JWTError
from typing import Annotated
import configparser
from datetime import date
router = APIRouter()
engine = EngineConn()
session = engine.sessionmaker()
security = HTTPBearer()

config = configparser.ConfigParser()
config.read("config.ini")
auth_conf = config["auth"]
SECRET_KEY = auth_conf["SECRET_KEY"]
ALGORITHM = auth_conf["ALGORITHM"]


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        print(credentials)
        if credentials:
            print(credentials.credentials)
            verified = self.verify_jwt(credentials.credentials)
            return verified

    def verify_jwt(self, jwtoken: str) -> bool:
        try:
            payload = jwt.decode(jwtoken, SECRET_KEY, algorithms=[ALGORITHM])
        except:
            payload = None
        if payload:
            return payload
        else:
            return False


async def get_current_user(payload: Annotated[str, Depends(JWTBearer())]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if payload is None:
        raise credentials_exception
    return payload["sub"]


class Onboarding(BaseModel):
    mom_name: str
    baby_name: str
    preg_date: date
    birth: date
    detail: str


@router.get("/userdata")
async def update_todo(current_user: Annotated[User, Depends(get_current_user)]):
    try:
        user_account = session.query(User).filter(User.id == current_user).first()
        return {
            "status": "success",
            "data": {
                "email": user_account.email,
                "name": user_account.name,
                "locale": user_account.locale,
                "birth": user_account.birth,
                "picture": user_account.picture,
                "mom_name": user_account.mom_name,
                "baby_name": user_account.baby_name,
                "preg_date": user_account.preg_date,
                "detail": user_account.detail,
            }
        }
    except:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        return credentials_exception

@router.post("/onboarding")
async def update_todo(current_user: Annotated[User, Depends(get_current_user)],
                      onboardingdata: Onboarding):
    user_account = session.query(User).filter(User.id == current_user).first()

    if user_account is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        user_account.mom_name = onboardingdata.mom_name
        user_account.baby_name = onboardingdata.baby_name
        user_account.preg_date = onboardingdata.preg_date
        user_account.birth = onboardingdata.birth
        user_account.detail = onboardingdata.detail
        session.add(user_account)
        session.commit()
        session.close()
        return {
            "status": "success",
            "message": "onboarding updated"
        }
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please check input and try again",
        )


@router.post("/userdata/update")
async def update_todo(current_user: Annotated[User, Depends(get_current_user)],
                      onboardingdata: Onboarding):
    user_account = session.query(User).filter(User.id == current_user).first()

    if user_account is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        user_account.name = onboardingdata.name
        user_account.picture = onboardingdata.picture
        user_account.locale = onboardingdata.locale
        user_account.mom_name = onboardingdata.mom_name
        user_account.baby_name = onboardingdata.baby_name
        user_account.preg_date = onboardingdata.preg_date
        user_account.birth = onboardingdata.birth
        user_account.detail = onboardingdata.detail
        session.add(user_account)
        session.commit()
        session.close()
        return {
            "status": "success",
            "message": "userdata updated"
        }
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please check input and try again",
        )