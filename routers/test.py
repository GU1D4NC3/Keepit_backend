from fastapi import APIRouter
from databases.basedb import engineconn
from models.test_model import Test
from sqlalchemy import text
from pydantic import BaseModel

testrouter = APIRouter(
    prefix="/tests",
    tags=["Test"]
)

engine = engineconn()
session = engine.sessionmaker()


@testrouter.get("/test")
async def basic_get():
    return {"message": "Hello World"}


@testrouter.get("/time")
async def db_time():
    sql = "SELECT now() as time"
    return session.execute(text(sql)).mappings().fetchall()


@testrouter.get("/demotable")
async def basic_table_getter():
    return session.query(Test).all()


@testrouter.post("/demotable")
async def basic_table_getter(title: str):
    data = Test(title=title)
    session.add(data)
    session.commit()
    session.refresh(data)
    return data


@testrouter.get("/demotable_filter")
async def basic_table_getter(id):
    basic_table = session.query(Test).filter(Test.id == id).first()
    return basic_table


class Item(BaseModel):
    title: str


@testrouter.post("/postbodytest")
async def basic_table_getter(item: Item):
    return item


@testrouter.post("/postparamtest")
async def basic_table_getter(title: str):
    return {"title": title}
