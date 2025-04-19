from pydantic import BaseModel
from db.models.Car import CarType

class CarBase(BaseModel):
    brand: str
    model: str
    type: CarType
    year: str
    price_per_day: str
    is_available: bool


class CarShow(CarBase):
    pass