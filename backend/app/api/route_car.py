from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from api.utils import SessionDB
from db.daos.CarDAO import CarDAO
from pydantic import UUID4
from db.services.CarService import CarService
from db.schemas.car import CarShow, CarShow_MaxDays
from db.schemas.booking import BookingShow
from db.schemas.utils import FutureDateOneYear

router = APIRouter()

@router.get("/", response_model=list[CarShow])
async def get_all(db: SessionDB):
    cars = CarDAO(db).get_all()
    return cars


@router.get("/available", response_model=list[CarShow_MaxDays])
async def get_available(date: FutureDateOneYear, db: SessionDB):
    return CarService.get_availables(date_selected=date, db=db)


@router.get("/available/image", response_model=list[CarShow])
async def get_available_image(db: SessionDB):
    image_bytes = CarService.get_availables_image(db)
    return StreamingResponse(image_bytes, media_type="image/png")


@router.get("/{uuid}", response_model=CarShow)
async def get_by_uuid(uuid: UUID4, db: SessionDB):
    return CarService.get_by_uuid(uuid=uuid, db=db)


@router.get("/{uuid}/bookings", response_model=list[BookingShow])
async def get_car_bookings(uuid: UUID4, db: SessionDB):
    return CarService.get_by_uuid(uuid=uuid, db=db).bookings_future