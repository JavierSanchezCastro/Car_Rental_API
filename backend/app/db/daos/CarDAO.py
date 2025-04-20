from sqlalchemy.orm import Session
from db.daos.BaseDAO import BaseDAO
from db.models.Car import Car
from pydantic import UUID4
from sqlalchemy import select, not_

class CarDAO(BaseDAO):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_by_uuid(self, uuid: UUID4) -> Car | None:
        query = select(Car).where(Car.uuid == str(uuid))
        car = self.session.scalar(query)
        return car
    
    def get_all(self) -> list[Car]:
        query = select(Car)
        cars = self.session.scalars(query).all()
        return cars

    def create(self, car_data: dict) -> Car:
        car = Car(**car_data)
        self.session.add(car)
        self.session.commit()
        self.session.refresh(car)
        return car
