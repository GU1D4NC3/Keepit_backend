from fastapi import APIRouter
from databases.basedb import EngineConn
from models.test_model import Test
from sqlalchemy import text
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()
engine = EngineConn()
session = engine.sessionmaker()


@router.get("/test")
async def basic_get():
    return {"message": "Hello World"}


@router.get("/time")
async def db_time():
    sql = "SELECT now() as time"
    return session.execute(text(sql)).mappings().fetchall()


@router.get("/utcnow")
async def utc_int():
    return {
        "status": "success",
        "data": datetime.utcnow().timestamp()
    }


@router.get("/demotable")
async def basic_table_getter():
    return session.query(Test).all()


@router.post("/demotable")
async def basic_table_getter(title: str):
    data = Test(title=title)
    session.add(data)
    session.commit()
    session.refresh(data)
    return data


@router.get("/demotable_filter")
async def basic_table_getter_with_filter(id):
    basic_table = session.query(Test).filter(Test.id == id).first()
    return basic_table


class Item(BaseModel):
    title: str


@router.post("/postbodytest")
async def basic_post(item: Item):
    return item


@router.post("/postparamtest")
async def basic_post_with_param(title: str):
    return {"title": title}
