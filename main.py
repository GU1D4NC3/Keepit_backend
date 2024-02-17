from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import google, user, diary, vision, quiz, news
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'googlekey.json'
tags_metadata = [
    {
        "name": "Google Auth",
        "description": "Google Oauth2 authentication"
    },
    {
        "name": "User management",
        "description": "Personal information and Onboarding"
    },
    {
        "name": "Diary",
        "description": "Diary CRUD"
    },
    {
        "name": "Google Vision",
        "description": "Google Vision AI Api"
    },
    {
        "name": "Quiz",
        "description": "Quiz data api"
    },
    {
        "name": "News",
        "description": "News data api"
    }
]

app = FastAPI(
    title='MomGround Backend',
    description='2024 GDSC chellenge MomGround Backend',
    summary="",
    version="0.1.1",
    openapi_tags=tags_metadata,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(google.router, prefix="/google", tags=["Google Auth"])
app.include_router(user.router, prefix="/user", tags=["User management"])
app.include_router(diary.router, prefix="/diary", tags=["Diary"])
app.include_router(vision.router, prefix="/vision", tags=["Google Vision"])
app.include_router(quiz.router, prefix="/quiz", tags=["Quiz"])
app.include_router(news.router, prefix="/news", tags=["News"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)