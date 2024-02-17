from datetime import datetime, timedelta, timezone
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any;
# from models.responsemodel import AccessToken
from models.usermodel import User
import requests
from jose import jwt
import configparser
from databases.basedb import EngineConn

config = configparser.ConfigParser()
config.read("config.ini")
google_conf = config["google"]
router = APIRouter()
engine = EngineConn()
session = engine.sessionmaker()

# Replace these with your own values from the Google Developer Console
GOOGLE_CLIENT_ID = google_conf["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = google_conf["GOOGLE_CLIENT_SECRET"]
GOOGLE_REDIRECT_URI = google_conf["GOOGLE_REDIRECT_URI"]
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
auth_conf = config["auth"]

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = auth_conf["SECRET_KEY"]
ALGORITHM = auth_conf["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = int(auth_conf["ACCESS_TOKEN_EXPIRE_MINUTES"])


def get_user(id):
    return session.query(User).filter(User.id == id).first()


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


class LoginPath(BaseModel):
    status: str = "success"
    url: str = "https://accounts.google.com/"


@router.get("/login",
            description="Get google login url",
            response_model=LoginPath)
async def login_google() -> Any:
    res = LoginPath()
    res.status = "success"
    res.url = f"{GOOGLE_AUTH_URL}?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
    return res


class AccessToken(BaseModel):
    status: str = "success"
    access_token: str = "abcde"


@router.get("/auth_backend",
            description="get google auth through redirect",
            response_model=AccessToken)
async def auth_get_google_token(code: str):
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    access_token = response.json().get("access_token")
    res = AccessToken()
    res.status = "success"
    res.access_token = access_token
    return res


class AuthWithToken(BaseModel):
    status: str = "success"
    is_registered: bool = True
    message: str = "success"
    access_token: str = "abcde"


@router.get("/auth_withtoken",
            description="verify google auth and get self authorization",
            response_model=AuthWithToken)
async def auth_google_token_verify(token: str):
    user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo",
                             headers={"Authorization": f"Bearer {token}"}).json()
    userdata = get_user(user_info["id"])
    if not userdata:
        data = User(id=user_info["id"],
                    email=user_info["email"],
                    name=user_info["name"],
                    picture=user_info["picture"])
        session.add(data)
        session.commit()
        session.close()
        userdata = (session.query(User)
                    .filter(user_info["id"] == User.id)
                    .first())
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    generated_token = create_access_token(
        data={"sub": user_info["id"]}, expires_delta=access_token_expires
    )
    response = AuthWithToken()
    response.status = "success"
    response.access_token = generated_token
    if userdata.mom_name:
        response.is_registered = True
        response.message = f"Welcome {userdata.mom_name}"
    else:
        response.is_registered = False
        response.message = "Require registeration process "
    return response
