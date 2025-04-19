from fastapi import APIRouter
from api.utils import SessionDB
from db.daos.CarDAO import CarDAO
from pydantic import UUID4
from api.utils import SessionDB
from db.services.CarService import CarService
from db.schemas.car import CarShow

router = APIRouter()

@router.get("/", response_model=list[CarShow])
async def get_all(db: SessionDB):
    cars = CarDAO(db).get_all()
    return cars

@router.get("/available", response_model=list[CarShow])
async def get_available(db: SessionDB):
    cars = CarDAO(db).get_available()
    return cars

@router.get("/unavailable", response_model=list[CarShow])
async def get_unavailable(db: SessionDB):
    cars = CarDAO(db).get_unavailable()
    return cars

@router.get("/{uuid}", response_model=CarShow)
async def get_by_uuid(uuid: UUID4, db: SessionDB):
    return CarService.get_by_uuid(uuid=uuid, db=db)