from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "user"
    email: str = Field(primary_key=True)
    username: str
    exp: int


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
