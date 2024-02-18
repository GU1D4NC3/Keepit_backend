from typing import Annotated
from fastapi import APIRouter,HTTPException, Depends, status
from databases.basedb import EngineConn
from pydantic import BaseModel
from datetime import datetime, date
from sqlalchemy import text

from models.hospitalmodel import Hospital
from models.usermodel import User
from routers.user import get_current_user

router = APIRouter()
engine = EngineConn()
session = engine.sessionmaker()

class NewHospital(BaseModel):
    id: int
    name: str
    type: str
    area: str
    address: str
    pos_x: float
    pos_y: float
    phone: str


@router.post("/update",
             description="insert news or update if exist")
async def insert_nq(data: NewHospital):
    try:
        existing_item = session.query(NewHospital).filter(NewHospital.id == data.id).first()
        if existing_item:
            # update if duplicated item exist
            existing_item.name = data.name
            existing_item.type = data.type
            existing_item.area = data.area
            existing_item.address = data.address
            existing_item.pos_x = data.pos_x
            existing_item.pos_y = data.pos_y
            existing_item.phone = data.phone
            session.add(existing_item)
            session.commit()
            session.close()
            return {
                "status": "success",
                "message": f"{data.name} updated",
                "updated_at": f"{datetime.now()}"
            }
    except Exception as e:
        raise {
            "status": "failed",
            "message": f"Please check input {e}"
        }
    session.flush()
    new_data = Hospital(
        id=data.id,
        name=data.name,
        type=data.type,
        area=data.area,
        address=data.address,
        pos_x=data.pos_x,
        pos_y=data.pos_y,
        phone=data.phone,
    )
    session.add(new_data)
    try:
        session.commit()
        session.close()
        return {
            "status": "success",
            "message": f"{data.name} added",
            "updated_at": f"{datetime.now()}"
        }
    except:
        session.rollback()
        session.close()
        raise {
            "status": "failed",
            "message": f"Please check input"
        }