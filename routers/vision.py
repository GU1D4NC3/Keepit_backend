from fastapi import APIRouter,HTTPException, Depends, status
from databases.basedb import EngineConn
from libs import vision
router = APIRouter()
engine = EngineConn()
session = engine.sessionmaker()


@router.get("/test")
async def basic_get():
    try:
        output = vision.run_quickstart()
        return {
            "stauts": "success",
            "data": {
                "labels": output
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Please check input and try again {e}",
        )


@router.get("/get_label")
async def basic_get(image: str):
    try:
        output = vision.detect_image(image)
        return {
            "stauts": "success",
            "data": {
                "labels": output
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Please check input and try again {e}",
        )