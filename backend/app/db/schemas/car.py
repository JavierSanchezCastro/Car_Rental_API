from pydantic import BaseModel
from db.models.Car import CarType
from pydantic import UUID4

class CarBase(BaseModel):
    brand: str
    model: str
    type: CarType
    year: int
    price_per_day: float
    is_available: bool


class CarShow(CarBase):
    uuid: UUID4