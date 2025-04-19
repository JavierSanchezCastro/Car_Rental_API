from pydantic import BaseModel, EmailStr, PositiveInt
from db.models.Car import CarType
from datetime import date

class BookingBase(BaseModel):
    car_id: int
    customer_name: str
    customer_email: EmailStr
    booking_date: date
    days: PositiveInt

class BookingShow(BookingBase):
    total_price: float

class BookingCreate(BookingBase):
    pass
