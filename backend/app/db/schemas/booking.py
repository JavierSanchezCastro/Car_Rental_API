from pydantic import BaseModel, EmailStr, PositiveInt, UUID4, Field
from db.schemas.car import CarShow
from db.schemas.utils import FutureDateOneYear
from datetime import date
from typing import Annotated


class BookingBase(BaseModel):
    customer_name: str
    customer_email: EmailStr
    booking_date: date
    days: PositiveInt

class BookingShow(BookingBase):
    uuid: UUID4
    total_price: float
    end_booking_date: date
    car: CarShow

class BookingCreate(BookingBase):
    car_uuid: UUID4
    days: Annotated[PositiveInt, Field(le=5)]
    booking_date: FutureDateOneYear
