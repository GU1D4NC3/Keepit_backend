import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import test


tags_metadata = [
    {
        "name":"Auth",
        "description":"Login and authorization"
    },
    {
        "name":"Test",
        "description":"Examples and Test of basic apis"
    },
    {
        "name":"Finance"
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

app.include_router(test.testrouter)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0")