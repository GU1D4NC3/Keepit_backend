from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
import requests
from jose import jwt
from auth.jwt import create_access_token, verify_access_token
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
account = config["google"]
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Replace these with your own values from the Google Developer Console
GOOGLE_CLIENT_ID = account["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = account["GOOGLE_CLIENT_SECRET"]
GOOGLE_REDIRECT_URI = account["GOOGLE_REDIRECT_URI"]
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"

@router.get("/login")
async def login_google():
    return {
        "stauts": "success",
        "url": f"{GOOGLE_AUTH_URL}?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
    }


@router.get("/auth")
async def auth_google(code: str):
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
    user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {access_token}"})
    return {
        "stauts": "success",
        "user_data": user_info.json()
    }


@router.get("/token")
async def get_token(token: str = Depends(oauth2_scheme)):
    return jwt.decode(token, GOOGLE_CLIENT_SECRET, algorithms=["HS256"])
