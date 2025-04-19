from fastapi import APIRouter
from api.utils import SessionDB
from db.daos.CarDAO import CarDAO
from pydantic import UUID4
from api.utils import SessionDB
from db.services.CarService import CarService

router = APIRouter()

@router.get("/")
async def get_all(db: SessionDB):
    universities = CarDAO(db).get_all()
    return universities

@router.get("/{uuid}")
async def get_by_uuid(uuid: UUID4, db: SessionDB):
    return CarService.get_by_uuid(uuid=uuid, db=db)