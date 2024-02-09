from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import test, google, user, diary


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
        "name": "Test",
        "description": "Examples and Test of basic apis"
    }
]

app = FastAPI(
    title='Momsaeng Backend',
    description='2024 GDSC chellenge Momsaeng Backend',
    summary="",
    version="0.0.1",
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

app.include_router(test.router, prefix="/test", tags=["Test"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)