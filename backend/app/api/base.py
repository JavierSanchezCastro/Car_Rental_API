
from api import route_car
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(route_car.router, prefix="/car", tags=["Car"])
