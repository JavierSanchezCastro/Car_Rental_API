from sqlalchemy.orm import Session
from db.daos.BaseDAO import BaseDAO
from db.models.Booking import Booking
from pydantic import UUID4
from sqlalchemy import select

class BookingDAO(BaseDAO):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_by_uuid(self, uuid: UUID4) -> Booking | None:
        query = select(Booking).where(Booking.uuid == uuid.bytes)
        booking = self.session.scalar(query)
        return booking
    
    def get_all(self) -> list[Booking]:
        query = select(Booking)
        bookings = self.session.scalars(query).all()
        return bookings

    def create(self, booking_data: dict) -> Booking:
        booking = Booking(**booking_data)
        self.session.add(booking)
        self.session.commit()
        self.session.refresh(booking)
        return booking
