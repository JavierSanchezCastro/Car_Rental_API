from sqlalchemy.orm import Session
from db.models.Car import Car
from db.daos.CarDAO import CarDAO
from pydantic import UUID4
from fastapi import status, HTTPException

class CarService:

    @staticmethod
    def get_by_uuid(uuid: UUID4, db: Session):
        car = CarDAO(db).get_by_uuid(uuid=uuid)
        if not car:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Car with uuid={uuid} not found")
        return car