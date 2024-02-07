from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import test, google, auth


tags_metadata = [
    {
        "name": "Auth",
        "description": "Oauth2 with jwt"
    },
    {
        "name": "Google Auth",
        "description": "Google Oauth2 authentication"
    },
    {
        "name": "Test",
        "description": "Examples and Test of basic apis"
    }
]

app = FastAPI(
    title='GDSC24_CHL_BE',
    description='2024 GDSC Backend',
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

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(google.router, prefix="/google", tags=["Google Auth"])
app.include_router(test.router, prefix="/test", tags=["Test"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)