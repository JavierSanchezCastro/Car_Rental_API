
from api import route_car
from api import route_booking
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(route_car.router, prefix="/car", tags=["Car"])
api_router.include_router(route_booking.router, prefix="/booking", tags=["Booking"])
