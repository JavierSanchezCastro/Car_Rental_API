from fastapi import APIRouter
from api.utils import SessionDB
from db.daos.BookingDAO import BookingDAO
from pydantic import UUID4
from db.services.BookingService import BookingService
from db.schemas.booking import BookingCreate, BookingShow

router = APIRouter()

@router.get("/", response_model=list[BookingShow])
async def get_all(db: SessionDB):
    bookings = BookingDAO(db).get_all()
    return bookings

@router.get("/{uuid}", response_model=BookingShow)
async def get_by_uuid(uuid: UUID4, db: SessionDB):
    return BookingService.get_by_uuid(uuid=uuid, db=db)


@router.post("/", response_model=BookingShow)
async def create_booking(booking_info: BookingCreate, db: SessionDB):
    return BookingService.create(booking_info=booking_info, db=db)    
    