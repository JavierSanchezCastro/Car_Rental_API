from pydantic import BaseModel
from db.models.Car import CarType
from pydantic import UUID4

class CarBase(BaseModel):
    brand: str
    model: str
    type: CarType
    year: int
    price_per_day: float

class CarShow(CarBase):
    uuid: UUID4

class CarShow_MaxDays(CarBase):
    max_days: int
    #id: int
    uuid: UUID4