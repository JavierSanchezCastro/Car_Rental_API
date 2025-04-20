from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Numeric, Date, ForeignKey
from db.models.Base import Base
from datetime import date
from pydantic import EmailStr

class Booking(Base):
    car_id: Mapped[int] = mapped_column(ForeignKey("car.id"))
    customer_name: Mapped[str] = mapped_column(String(100), nullable=False)
    customer_email: Mapped[EmailStr] = mapped_column(String(100), nullable=False)
    booking_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_booking_date: Mapped[date] = mapped_column(Date, nullable=False)
    days: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    total_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    car: Mapped["Car"] = relationship("Car", back_populates="bookings")
